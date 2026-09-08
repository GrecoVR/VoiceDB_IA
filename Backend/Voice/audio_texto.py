import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
import numpy as np


def grabar_audio():
    frecuencia = 44100
    duracion = 10
    ganancia = 2.0

    print("Habla ahora...")

    audio = sd.rec(
        int(duracion * frecuencia),
        samplerate=frecuencia,
        channels=1,
        dtype="int16",
        device=1
    )

    sd.wait()

    # Aumentar ganancia
    audio = audio.astype(np.float32) * ganancia

    # Evitar que el audio se salga del rango de int16
    audio = np.clip(audio, -32768, 32767)

    # Volver a int16
    audio = audio.astype(np.int16)

    wav.write("audio.wav", frecuencia, audio)

    print("Grabación terminada")


def convertir_a_texto():
    reconocedor = sr.Recognizer()

    with sr.AudioFile("audio.wav") as fuente:
        audio = reconocedor.record(fuente)

    try:
        texto = reconocedor.recognize_google(
            audio,
            language="es-ES"
        )

        print("Audio reconocido:", texto)
        return texto

    except sr.UnknownValueError:
        print("Audio no reconocido")
        return None

    except sr.RequestError as error:
        print("Error de reconocimiento:", error)
        return None