from Backend.Database.config import conectar_db
import mysql.connector

def insertar_datos(marca, modelo, precio):
    conexion = conectar_db()
    cursor = conexion.cursor()

    query = "INSERT INTO auto (marca, modelo, precio) VALUES (%s, %s, %s)"
    valores = (marca, modelo, precio)
    try:
        cursor.execute(query, valores)
        conexion.commit()
    except mysql.connector.IntegrityError:
        conexion.rollback()
    finally:
        cursor.close()
        conexion.close()
