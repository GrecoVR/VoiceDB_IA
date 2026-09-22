from Backend.Database.config import conectar_db


def eliminar_datos(id_auto):

    conexion = conectar_db()
    cursor = conexion.cursor()

    query_eliminar = "DELETE FROM auto WHERE id = %s"

    cursor.execute(query_eliminar, (id_auto,))

    conexion.commit()

    fila_eliminada = cursor.rowcount

    cursor.close()
    conexion.close()

    return fila_eliminada

