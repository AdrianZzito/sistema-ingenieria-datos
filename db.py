import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = db.cursor()

def insertClient(clientData):
    sql = "INSERT INTO clients (cod_cliente, nombre, apellido1, apellido2, dni, correo, telefono) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (
        clientData.get("cod_cliente"),
        clientData.get("nombre"),
        clientData.get("apellido1"),
        clientData.get("apellido2"),
        clientData.get("dni"),
        clientData.get("correo"),
        clientData.get("telefono")
    )
    cursor.execute(sql, val)
    db.commit()

def insertCard(cardData):
    sql = "INSERT INTO tarjetas (cod_cliente_tarjeta, numero_tarjeta, fecha_exp, cvv) VALUES (%s, %s, %s, %s)"
    val = (
        cardData.get("cod_cliente"),
        cardData.get("numero_tarjeta"),
        cardData.get("fecha_exp"),
        cardData.get("cvv")
    )
    cursor.execute(sql, val)
    db.commit()