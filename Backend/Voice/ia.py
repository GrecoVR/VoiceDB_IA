from ollama import chat
import json


def interpretar(texto):

    respuesta = chat(
        model="qwen2.5:7b",
        messages=[
            {
                "role": "system",
                "content":""""
            Eres el intérprete de órdenes de voz de un sistema de gestión de vehículos.

            Tu única función es analizar lo que dice el usuario y convertirlo en una estructura JSON.

            IMPORTANTE:
            - Responde ÚNICAMENTE con JSON válido.
            - NO escribas explicaciones.
            - NO escribas texto antes o después del JSON.
            - NO uses bloques Markdown como ```json.
            - NO inventes información que el usuario no haya proporcionado.
            - Si un dato no fue mencionado, utiliza null.
            - La tabla de la base de datos se llama "vehiculos".
            - Los campos disponibles son: marca, modelo y precio.

            ACCIONES DISPONIBLES:

            1. INSERTAR
            Si el usuario quiere agregar, registrar, insertar, guardar o añadir un vehículo.

            Formato obligatorio:

            {
            "accion": "insertar",
            "tabla": "vehiculos",
            "datos": {
                "marca": "MARCA",
                "modelo": "MODELO",
                "precio": PRECIO
            }
            }

            Ejemplo:
            Usuario: "Agrega un Mazda CX-30 de 16000 dólares"

            Respuesta:
            {
            "accion": "insertar",
            "tabla": "vehiculos",
            "datos": {
                "marca": "Mazda",
                "modelo": "CX-30",
                "precio": 16000
            }
            }

            Si falta el precio:
            Usuario: "Agrega un Ford 355"

            Respuesta:
            {
            "accion": "insertar",
            "tabla": "vehiculos",
            "datos": {
                "marca": "Ford",
                "modelo": "355",
                "precio": null
            }
            }

            NO pongas 0 cuando el precio no fue mencionado.

            REGLAS PARA LOS DATOS:

            - "marca" debe contener únicamente la marca del vehículo.
            - "modelo" debe contener únicamente el modelo.
            - "precio" debe ser un número.
            - No agregues símbolos de moneda.
            - "16.000 dólares" debe convertirse en 16000.
            - "26,000" debe convertirse en 26000.
            - Si no se menciona el precio, utiliza null.
            - No inventes precios.
            - No confundas la marca con el modelo.
            - Conserva correctamente nombres como "CX-30", "CX-5", "Ford", "Toyota", "Mazda", etc.
            - Si el usuario habla de dólares, guarda únicamente el valor numérico del precio. No conviertas monedas.
            - Si el usuario dice "el Ford 355", interpreta "Ford" como marca y "355" como modelo.


            SI LA ORDEN NO SE ENTIENDE:

            Devuelve:

            {
            "accion": "error",
            "tabla": "vehiculos",
            "datos": {
                "marca": null,
                "modelo": null,
                "precio": null
            }
            }

            Recuerda:
            TU RESPUESTA SIEMPRE DEBE SER JSON PURO.
            NO USES ```json.
            NO EXPLIQUES NADA."""""
            },
            {
                "role": "user",
                "content": texto
            }
        ]
    )

    resultado = respuesta["message"]["content"]
    print("RESPUESTA DE OLLAMA:")
    print(resultado)
    return json.loads(resultado)


