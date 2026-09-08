from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from Backend.Voice.main import procesar_audio
from Backend.Database.select import obtener_autos
from Backend.Database.delete import eliminar_datos

app = FastAPI()

app.mount(
    "/css",
    StaticFiles(directory="Frontend/css"),
    name="css"
)

app.mount(
    "/js",
    StaticFiles(directory="Frontend/js"),
    name="js"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def inicio():

    return FileResponse("Frontend/index.html")

@app.get("/estado")
def estado():
    return {
        "estado": "activo"
    }

@app.post("/voz")
def procesar_voz():

    resultado = procesar_audio()
    
    if resultado is None:
        return {
            "estado": "error",
            "mensaje": "No se pudo procesar el audio"
        }

    return {
        "estado": "ok",
        "resultado": resultado
    }

@app.get("/auto")
def listar_autos():
    
    vehiculos = obtener_autos()
    return {
        "estado": "ok",
        "vehiculos": vehiculos
    }

@app.delete("/auto/{id_auto}")
def eliminar(id_auto: int):

    return eliminar_datos(id_auto)

