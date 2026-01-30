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

# Initialize Dropbox client with access token
accessToken = os.getenv("DROPBOX_ACCESS_TOKEN")
dbx = dropbox.Dropbox(accessToken)

# Define Dropbox file paths
dbxPathTarjetas = "/Tarjetas-2026-01-05.csv"
dbxPathClientes = "/Clientes-2026-01-05.csv"

# Define local download path
localPath = "downloadedFiles"

## Download files from dropbox
downloadFile(dbx, dbxPathTarjetas, f"{localPath}/Tarjetas-2026-01-05.csv") # Comment to avoid downloading cards file
downloadFile(dbx, dbxPathClientes, f"{localPath}/Clientes-2026-01-05.csv") # Comment to avoid downloading clients file

# Read CSV files into DataFrames
dfClients = pd.read_csv(f"{localPath}/Clientes-2026-01-05.csv", sep=";", encoding='latin1', dtype=str, engine='python')
dfCards = pd.read_csv(f"{localPath}/Tarjetas-2026-01-05.csv", sep=";", encoding='latin1', dtype=str, engine='python')

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
