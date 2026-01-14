import dropbox
from dotenv import load_dotenv
import os
from dropboxAuth import downloadFile
from etl import *
import pandas as pd

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
downloadFile(dbx, dbxPathTarjetas, f"{localPath}/Tarjetas-2026-01-05.csv")
downloadFile(dbx, dbxPathClientes, f"{localPath}/Clientes-2026-01-05.csv")

# Read CSV files into DataFrames
dfClients = pd.read_csv(f"{localPath}/Clientes-2026-01-05.csv", sep=";", encoding='latin1', dtype=str, engine='python')

# Get client headers
clientHeaders = dfClients.columns[0].split(";")
#print(clientHeaders[0])

# NORMALIZERS
CLIENT_NORMALIZERS = {
    "nombre": normCapital,
    "apellido1": normCapital,
    "apellido2": normCapital,
    "dni": normDNI,
    "correo": normEmail,
    "telefono": normPhone,
}

CARD_NORMALIZERS = {
    "numero_tarjeta": normCardNumber,
    "cvv": normCVV,
}

# Get main file content
for col in dfClients.items():

    # Get individual rows
    for content in col[1]:

        # Split row by sep into array
        fields = content.split(";")
        #print(fields)

        # Get each field and normalize
        for field in fields:
            #print(clientHeaders[i])
            print(field)

            #print(out)

        # TODO: Normalize fields into object

        # TODO: Insert into DB

        break
