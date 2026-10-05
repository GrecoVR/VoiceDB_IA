# Gestión de Autos por Voz

Aplicación web para administrar un inventario de vehículos usando **comandos de voz**. El usuario habla, el audio se transcribe a texto, un modelo de lenguaje local interpreta la orden y el vehículo se guarda en una base de datos MySQL.

## Características

- Registro de autos mediante voz (ej. *"Agrega un Mazda CX-30 de 16000 dólares"*).
- Interpretación de órdenes con un LLM local (Ollama + Qwen 2.5 7B), sin depender de APIs de pago.
- Persistencia en MySQL con validación de duplicados (marca + modelo).
- Tabla de autos ordenada por precio, con opción de eliminar registros.
- Alternancia del precio entre dólares y su equivalente en "Mazda MX-5" (valor de referencia: $30,000).
- Indicador de estado de conexión con el servidor.
- Interfaz con estilo *glassmorphism*.

## Arquitectura

```
Micrófono → SpeechRecognition (Google) → Ollama (qwen2.5:7b) → JSON → MySQL
                                                                    ↑
                        Frontend (HTML/CSS/JS) ←→ API FastAPI ──────┘
```

```
.
├── Backend
│   ├── API/main.py          # Endpoints FastAPI y archivos estáticos
│   ├── Database/            # config, insert, select, delete, main (lógica SQL)
│   └── Voice/               # audio_texto (grabación/STT), ia (LLM), main (flujo)
├── Frontend
│   ├── index.html
│   ├── css/style.css
│   └── js/main.js
└── .gitignore
```

## Tecnologías

| Capa | Tecnología |
|------|-----------|
| Backend | Python, FastAPI, Uvicorn |
| Base de datos | MySQL (`mysql-connector-python`) |
| Voz a texto | `sounddevice`, `scipy`, `SpeechRecognition` |
| IA | Ollama + `qwen2.5:7b` |
| Frontend | HTML, CSS y JavaScript vanilla |

## Requisitos previos

- Python 3.10+
- MySQL Server
- [Ollama](https://ollama.com) instalado
- Un micrófono conectado al equipo donde corre el servidor

## Instalación

1. **Clonar el repositorio**
```bash
   git clone https://github.com/TU_USUARIO/TU_REPO.git
   cd TU_REPO
```

2. **Crear entorno virtual e instalar dependencias**
```bash
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   pip install fastapi uvicorn mysql-connector-python python-dotenv ollama sounddevice scipy numpy SpeechRecognition
```

3. **Crear la base de datos**
```sql
   CREATE DATABASE autos;
   USE autos;
   CREATE TABLE auto (
       id INT AUTO_INCREMENT PRIMARY KEY,
       marca VARCHAR(50) NOT NULL,
       modelo VARCHAR(50) NOT NULL,
       precio DECIMAL(12,2)
   );
```

4. **Configurar variables de entorno**: crea un archivo `.env` en la raíz:
```
   DB_USER=root
   DB_PASSWORD=tu_contraseña
   DB_NAME=autos
   DB_HOST=localhost
```

5. **Descargar el modelo de IA**
```bash
   ollama pull qwen2.5:7b
```

6. **Ajustar el micrófono**: en `Backend/Voice/audio_texto.py` cambia `device=1` por el índice de tu micrófono. Para listar dispositivos:
```bash
   python -c "import sounddevice as sd; print(sd.query_devices())"
```

## Ejecución

Desde la raíz del proyecto:

```bash
uvicorn Backend.API.main:app --reload
```

Abre **http://localhost:8000** en el navegador.

## Uso

1. Pulsa el botón del micrófono (la grabación dura 10 segundos).
2. Di una orden, por ejemplo: *"Registra un Toyota Corolla de 18000 dólares"*.
3. El auto aparecerá en la tabla. Si ya existe (misma marca y modelo), se mostrará un aviso.
4. Usa **Eliminar** para borrar un registro y **⇄** para cambiar la vista del precio.

## Endpoints de la API

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Sirve la interfaz web |
| GET | `/estado` | Comprueba que el servidor está activo |
| POST | `/voz` | Graba, transcribe, interpreta e inserta |
| GET | `/auto` | Lista los autos (ordenados por precio) |
| DELETE | `/auto/{id_auto}` | Elimina un auto por ID |

Documentación interactiva en `http://localhost:8000/docs`.

## Limitaciones conocidas

- La grabación usa el micrófono **del servidor**, no el del navegador; debe ejecutarse en local.
- El reconocimiento de voz usa el servicio gratuito de Google y requiere internet.
- La interfaz alojada en GitHub Pages es solo una vista estática: sin backend no hay datos ni voz.

## Mejoras futuras

- Captura de audio desde el navegador (MediaRecorder API).
- Comandos de voz para eliminar y editar vehículos.
- Validación cuando falte el precio (`null`).
- Dockerización del proyecto.

## 📄 Licencia

Distribuido bajo licencia MIT.
