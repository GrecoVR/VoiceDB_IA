from Backend.Database.insert import insertar_datos
from Backend.Database.select import obtener_autos


def ejecutar_sql(datos):

    accion = datos["accion"]
    informacion = datos.get("datos", {})

    if accion == "insertar":
        insertar_datos(informacion["marca"], informacion["modelo"], informacion["precio"])
        return {
                    "interpretacion": datos,
                    "base_datos": "Operación realizada con éxito"
                }
    elif accion == "eliminar":
        print("No es posible ejecutar la accion por comando de voz")
        return {
                    "interpretacion": datos,
                    "base_datos": "Operacion no realizada. No es posible ejecutar la accion por comando de voz"
                }
    else:
        return {
                    "interpretacion": datos,
                    "base_datos": "Acción no reconocida"
                }

def consultar_listado_autos():
    return obtener_autos()