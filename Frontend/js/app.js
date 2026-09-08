const API = {
    autos: "/auto",
    estado: "/estado",
    voz: "/voz"
};

const VALOR_REFERENCIA = 30000;
const VOICE_SECONDS = 10;

let autos = [];
let mostrarValor = false;
let escuchando = false;
let intervalo = null;

// HTML
const tabla = document.getElementById("vehicleTableBody");
const contador = document.getElementById("contador_autos");
const estado = document.getElementById("connectionStatus");
const botonMicrofono = document.getElementById("micButton");
const temporizador = document.getElementById("voiceTimer");
const estadoVoz = document.getElementById("voiceState");
const encabezadoPrecio = document.getElementById("priceHeader");
const botonPrecio = document.getElementById("priceToggle");
const actualizar = document.getElementById("refreshButton");
const vacio = document.getElementById("emptyState");

// Cargar autos

async function cargarAutos() {
    try {
        const respuesta = await fetch(API.autos);
        const datos = await respuesta.json();

        autos = datos.vehiculos || [];
        mostrarAutos();

    } catch (error) {
        console.error(error);
    }
}

// Mostrar tabla

function mostrarAutos() {
    tabla.innerHTML = "";

    contador.textContent = autos.length;

    if (autos.length === 0) {
        vacio.style.display = "block";
        return;
    }

    vacio.style.display = "none";

    autos.forEach(auto => {
        const fila = document.createElement("tr");

        const precio = Number(auto.precio || 0);

        const valor = Math.floor(precio / VALOR_REFERENCIA);

        fila.innerHTML = `
            <td>${auto.marca || ""}</td>
            <td>${auto.modelo || ""}</td>
            <td>
                ${
                    mostrarValor
                    ? `${valor} Mazda MX-5`
                    : `$${precio.toLocaleString()}`
                }
            </td>
            <td>
                <button class="delete-button" id = "delete-button" onclick="eliminarAuto(${auto.id})">
                    Eliminar
                </button>
            </td>
        `;

        tabla.appendChild(fila);
    });
}

// Eliminar auto

async function eliminarAuto(id) {
    try {
        const respuesta = await fetch(`${API.autos}/${id}`, {
            method: "delete"
        });

        if (!respuesta.ok) {
            throw new Error("No se pudo eliminar");
        }

        await cargarAutos();

    } catch (error) {
        console.error(error);
    }
}

// -------------------------
// Precio / Valor
// -------------------------

function cambiarPrecio() {
    mostrarValor = !mostrarValor;

    if (mostrarValor) {
        encabezadoPrecio.textContent = "Valor";
    } else {
        encabezadoPrecio.textContent = "Precio";
    }

    mostrarAutos();
}

// -------------------------
// Comprobar conexión
// -------------------------

async function comprobarConexion() {
    try {
        const respuesta = await fetch(API.estado);

        if (!respuesta.ok) {
            throw new Error();
        }

        const datos = await respuesta.json();

        if (datos.estado === "activo") {
            estado.textContent = "Conectado";
            estado.classList.add("connected");
        }

    } catch {
        estado.textContent = "Desconectado";
        estado.classList.remove("connected");
    }
}

// -------------------------
// Micrófono
// -------------------------

async function iniciarMicrofono() {

    if (escuchando) return;

    escuchando = true;

    let segundos = VOICE_SECONDS;

    temporizador.textContent = segundos;
    estadoVoz.textContent = "Escuchando...";

    botonMicrofono.classList.add("active");

    intervalo = setInterval(() => {

        segundos--;

        temporizador.textContent = segundos;

        if (segundos <= 0) {
            detenerMicrofono();
        }

    }, 1000);

    try {

        const respuesta = await fetch(API.voz, {
            method: "POST"
        });

        const datos = await respuesta.json();

        console.log(datos);

        await cargarAutos();

    } catch (error) {

        console.error(error);

    } finally {

        detenerMicrofono();

    }
}

// -------------------------
// Detener micrófono
// -------------------------

function detenerMicrofono() {

    clearInterval(intervalo);

    escuchando = false;

    temporizador.textContent = "";

    estadoVoz.textContent = "Presiona para hablar";

    botonMicrofono.classList.remove("active");
}

// -------------------------
// Eventos
// -------------------------

botonMicrofono.addEventListener("click", iniciarMicrofono);

botonPrecio.addEventListener("click", cambiarPrecio);

actualizar.addEventListener("click", cargarAutos);

// -------------------------
// Inicio
// -------------------------

cargarAutos();
comprobarConexion();