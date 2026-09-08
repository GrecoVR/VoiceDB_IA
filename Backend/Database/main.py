from Backend.Database.insert import insertar_datos
from Backend.Database.select import obtener_autos


def ejecutar_sql(datos):

    accion = datos["accion"]
    info_auto = datos.get("datos", {})

    if accion == "insertar":
        se_pudo_insertar = insertar_datos(info_auto["marca"], info_auto["modelo"], info_auto["precio"])

        if se_pudo_insertar:
            return {
                        "interpretacion": datos,
                        "resultado": True,
                        "base_datos": "Operación realizada con éxito"
                    }
        else:
            return {
                        "interpretacion": datos,
                        "resultado": False,
                        "base_datos": "El auto ya esta registrado"
                    }
    else:
        return {
                    "interpretacion": datos,
                    "resultado": False,
                    "base_datos": "Acción no reconocida"
                }

def consultar_listado_autos():
    return obtener_autos()