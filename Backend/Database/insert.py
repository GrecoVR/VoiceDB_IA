from Backend.Database.config import conectar_db
import mysql.connector

def insertar_datos(marca, modelo, precio):
    conexion = conectar_db()
    cursor = conexion.cursor()
    try:
        query_verificar = "SELECT id FROM auto WHERE marca = %s AND modelo = %s"
        cursor.execute(query_verificar, (marca, modelo))

        if cursor.fetchone():
            print("El auto ya existe")
            return False
            
        query_insertar = "INSERT INTO auto (marca, modelo, precio) VALUES (%s, %s, %s)"
        valores = (marca, modelo, precio)
    
        cursor.execute(query_insertar, valores)
        conexion.commit()
        return True
    except mysql.connector.Error as error:
        conexion.rollback()
        print("Error:", error)
        return False
    finally:
        cursor.close()
        conexion.close()
