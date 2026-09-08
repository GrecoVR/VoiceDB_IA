import mysql.connector

mc = mysql.connector
usuario = "root"
contraseña = "greco1752"
bd = "autos"
host = "localhost"

def conectar_db():
    conexion = mc.connect(
        user = usuario,
        password = contraseña,
        database = bd,
        host = host
    )
    return conexion