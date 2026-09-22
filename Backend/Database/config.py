import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

mc = mysql.connector
usuario = os.getenv("DB_USER")
contraseña = os.getenv("DB_PASSWORD")
bd = os.getenv("DB_NAME")
host = os.getenv("DB_HOST")
puerto = os.getenv("DB_PORT")

def conectar_db():
    conexion = mc.connect(
        user = usuario,
        password = contraseña,
        database = bd,
        host = host,
        port = puerto
    )
    return conexion

