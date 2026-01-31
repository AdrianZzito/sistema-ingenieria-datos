import dropbox
from dotenv import load_dotenv
import os
from dropboxAuth import downloadFile
from etl import *
import pandas as pd
from db import insertClient, insertCard
import mysql.connector
import re

# Load environment variables
load_dotenv()

# Initialize Dropbox client with refresh token
refreshToken = os.getenv("DROPBOX_REFRESH_TOKEN")
dbx = dropbox.Dropbox(
    oauth2_refresh_token=refreshToken,
    app_key=os.getenv("DROPBOX_APP_KEY"),
    app_secret=os.getenv("DROPBOX_APP_SECRET")
)

# File pattern
reTarjetas = re.compile(r"^Tarjetas-\d{4}-\d{2}-\d{2}\.csv$")
reClientes = re.compile(r"^Clientes-\d{4}-\d{2}-\d{2}\.csv$")

# List Dropbox files
entries = dbx.files_list_folder("").entries

# Search for files matching the patterns
tarjetas = next(e.name for e in entries if reTarjetas.match(e.name))
clientes = next(e.name for e in entries if reClientes.match(e.name))

# Define Dropbox file paths
dbxPathTarjetas = f"/{tarjetas}"
dbxPathClientes = f"/{clientes}"

# Define local download path
localPath = "downloadedFiles"
localTarjetas = f"{localPath}/{tarjetas}"
localClientes = f"{localPath}/{clientes}"

# Delete old files in local download directory
for file in os.listdir(localPath):
    if file.endswith(".csv"):
        os.remove(os.path.join(localPath, file))

## Download files from dropbox
downloadFile(dbx, dbxPathTarjetas, localTarjetas) # Comment to avoid downloading cards file
downloadFile(dbx, dbxPathClientes, localClientes) # Comment to avoid downloading clients file

# Read CSV files into DataFrames
dfClients = pd.read_csv(localClientes, sep=";", encoding='latin1', dtype=str, engine='python')
dfCards = pd.read_csv(localTarjetas, sep=";", encoding='latin1', dtype=str, engine='python')

# Get client headers
clientHeaders = dfClients.columns[0].split(";")
cardHeaders = dfCards.columns[0].split(";")

# NORMALIZERS
CLIENT_NORMALIZERS = {
    "cod_cliente": normCapital,
    "nombre": normCapital,
    "apellido1": normCapital,
    "apellido2": normCapital,
    "dni": normDNI,
    "correo": normEmail,
    "telefono": normPhone,
}

CARD_NORMALIZERS = {
    "cod_cliente": normCapital,
    "numero_tarjeta": normCardNumber,
    "fecha_exp": normCapital,
    "cvv": normCVV,
}

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = db.cursor()

nameRegex = r"^(?!.*\d).+$"

def etl(file: pd.DataFrame, dfName):
    # Get main file content
    for col in file.items():

        # Get individual rows
        for content in col[1]:

            # Split row by sep into array
            fields = content.split(";")
            #print(fields)

            i = 0
            client = {}
            card = {}

            validRow = True

            # Get each field and normalize
            for field in fields:
                # print(clientHeaders[i]) Print headers
                # print(field) Print field before normalization

                # Get normalizer function
                if dfName == "dfClients":
                    normFn = CLIENT_NORMALIZERS[clientHeaders[i]]
                else:
                    normFn = CARD_NORMALIZERS[cardHeaders[i]]

                # Check is name field is valid
                if dfName == "dfClients" and clientHeaders[i] == "nombre":
                    if not re.fullmatch(nameRegex, field):
                        validRow = False
                        break
                    else:
                        validRow = True

                # Normalize field
                normField = normFn(field)

                # print(f"Normalized field: {normField}") Print field after normalization

                # Assign normalized field to client or card dictionary
                if dfName == "dfClients":
                    client[clientHeaders[i]] = normField
                else:
                    card[cardHeaders[i]] = normField
                
                """
                if dfName == "dfClients":
                    print(f"Normalized client data: {client}")
                else:
                    print(f"Normalized card data: {card}")
                """

                # Increment index
                i += 1
            
            # Skip invalid rows
            if not validRow:
                print(f"Invalid row detected: {fields}")
                continue
            
            # Insert into database
            if dfName == "dfClients":
                insertClient(client)
            else:
                insertCard(card)
    
    if dfName == "dfClients":
        print("Client ETL process completed.")
    else:
        print("Card ETL process completed.")

# ETL process for clients
etl(dfClients, "dfClients")

# ETL process for cards
etl(dfCards, "dfCards")
