from Backend.Voice.audio_texto import grabar_audio, convertir_a_texto
from Backend.Voice.ia import interpretar
from Backend.Database.main import ejecutar_sql

def procesar_audio():
    grabar_audio()

    texto = convertir_a_texto()

    if texto:
        resultado = interpretar(texto)
        if resultado:
            resultado_sql = ejecutar_sql(resultado)
            return resultado_sql
    return None