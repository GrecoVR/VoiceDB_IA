from Backend.Database.config import conectar_db


def eliminar_datos(id_auto):

    conexion = conectar_db()
    cursor = conexion.cursor()

    query = """
        DELETE FROM auto
        WHERE id = %s
    """

    cursor.execute(query, (id_auto,))

    conexion.commit()

    filas_eliminadas = cursor.rowcount

    cursor.close()
    conexion.close()

    return filas_eliminadas