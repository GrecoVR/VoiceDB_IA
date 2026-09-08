from Backend.Database.config import conectar_db

def obtener_autos():
    conexion = conectar_db()
    cursor = conexion.cursor(dictionary=True)

    query = "SELECT * FROM auto ORDER BY precio ASC"
    cursor.execute(query)

    autos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return autos