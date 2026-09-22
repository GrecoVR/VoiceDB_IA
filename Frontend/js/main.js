const API={autos:"/auto",estado:"/estado",voz:"/voz"};

const VALOR_REFERENCIA=30000;
const VOICE_SECONDS=10;

let autos=[];
let mostrarValor=false;
let escuchando=false;
let intervalo=null;

const tabla=document.getElementById("TablaAutos");
const contador=document.getElementById("contadorAutos");
const estado=document.getElementById("estadoConexion");
const botonMicrofono=document.getElementById("botonMicrofono");
const temporizador=document.getElementById("temporizadorVoz");
const estadoVoz=document.getElementById("estadoVoz");
const encabezadoPrecio=document.getElementById("Precio");
const botonPrecio=document.getElementById("botonPrecio");
const actualizar=document.getElementById("botonActualizar");
const vacio=document.getElementById("estadoVacio");

async function cargarAutos(){
    try{
        const respuesta=await fetch(API.autos);
        const datos=await respuesta.json();
        autos=datos.vehiculos||[];
        mostrarAutos();
    }catch(error){
        console.error(error);
    }
}

function mostrarAutos(){
    tabla.innerHTML="";
    contador.textContent=autos.length;

    if(autos.length===0){
        vacio.style.display="block";
        return;
    }

    vacio.style.display="none";

    autos.forEach(auto=>{
        const fila=document.createElement("tr");
        const precio=Number(auto.precio||0);
        const valor=Math.floor(precio/VALOR_REFERENCIA);

        fila.innerHTML=`
            <td>${auto.marca||""}</td>
            <td>${auto.modelo||""}</td>
            <td>${mostrarValor?`${valor} Mazda MX-5`:`$${precio.toLocaleString()}`}</td>
            <td>
                <button class="boton-eliminar" onclick="eliminarAuto(${auto.id})">Eliminar</button>
            </td>
        `;

        tabla.appendChild(fila);
    });
}

async function eliminarAuto(id){
    try{
        const respuesta=await fetch(`${API.autos}/${id}`,{method:"DELETE"});

        if(!respuesta.ok){
            throw new Error("No se pudo eliminar");
        }

        await cargarAutos();
    }catch(error){
        console.error(error);
    }
}

function cambiarPrecio(){
    mostrarValor=!mostrarValor;
    encabezadoPrecio.textContent=mostrarValor?"Valor":"Precio";
    mostrarAutos();
}

async function comprobarConexion(){
    try{
        const respuesta=await fetch(API.estado);

        if(!respuesta.ok){
            throw new Error();
        }

        const datos=await respuesta.json();

        if(datos.estado==="activo"){
            estado.textContent="Conectado";
            estado.classList.add("conectado");
        }
    }catch{
        estado.textContent="Desconectado";
        estado.classList.remove("conectado");
    }
}

async function iniciarMicrofono(){
    if(escuchando)return;

    escuchando=true;

    let segundos=VOICE_SECONDS;

    temporizador.textContent=segundos;
    estadoVoz.textContent="Escuchando...";
    botonMicrofono.classList.add("activo");

    intervalo=setInterval(()=>{
        segundos--;
        temporizador.textContent=segundos;

        if(segundos<=0){
            detenerMicrofono();
        }
    },1000);

    try{
        const respuesta=await fetch(API.voz,{method:"POST"});
        const datos=await respuesta.json();

        console.log(datos);

        if(datos.estado==="ok"){
            if(datos.resultado.resultado===false){
                alert("El auto ya está registrado");
                return;
            }

            await cargarAutos();
        }
    }catch(error){
        console.error(error);
    }finally{
        detenerMicrofono();
    }
}

function detenerMicrofono(){
    clearInterval(intervalo);
    escuchando=false;
    temporizador.textContent="";
    estadoVoz.textContent="Presiona para hablar";
    botonMicrofono.classList.remove("activo");
}

botonMicrofono.addEventListener("click",iniciarMicrofono);
botonPrecio.addEventListener("click",cambiarPrecio);
actualizar.addEventListener("click",cargarAutos);

cargarAutos();
comprobarConexion();

