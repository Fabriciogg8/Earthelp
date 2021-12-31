String.prototype.replaceAt=function(index, character) 
{ return this.substr(0, index) + character + this.substr(index+character.length); }
// Forma usar funcion: palabraConGuiones = palabraConGuiones.replaceAt(i*2, letra);


//------------------------------------------------------------------
// var words = document.querySelector('#words').value;

const palabras = ['pollution','erosion','greenhouse','deforestation','biodiversity']; // array desde donde se elige la palabra
const palabra = palabras[Math.floor(Math.random()*palabras.length)]; 
// math.random (toma un numero entre 0y1), lo multiplica por el largo del array, y al hacerle floor
// eligira un valor entre 0 y largo (seleccionando por la posicion en el array)

//  let: porque es una variable
let palabraConGuiones = palabra.replace(/./g,"_ "); //  replace: El patrón puede ser una cadena o una RegExp, y el reemplazo
let contador = 0; // contador para las veces que falla    

document.querySelector('#output').innerHTML = palabraConGuiones;

document.querySelector('#calcular').addEventListener('click',()=> // Cuando hace click en calcular llama a una funcion anonima
{   
    const letra = document.querySelector('#letra').value;
    let fallo = true;
    for (const i in palabra){
        if(letra == palabra[i]){
            palabraConGuiones = palabraConGuiones.replaceAt(i*2, letra); // i*2 es porque al ponerle el guion le pusimos un espacio tambien entonces el indice es el doble
            fallo = false;
        }
    }
    if (fallo){
        contador += 1;
        document.querySelector('#ahorcado').style.backgroundPosition = -(200*contador) + 'px 0'; // desplaza la image del ahorcado
        if (contador == 4){
            alert('perdiste')
        }
    } else {
        if(palabraConGuiones.indexOf('_') < 0){
            document.querySelector('#ganador').style.display = 'flex';
        }
    }
    document.querySelector('#output').innerHTML = palabraConGuiones;

    document.querySelector('#letra').value = ''; // limpia el input despues de apretar el boton
    document.querySelector('#letra').focus(); // envía el puntero del mouse a la casilla para ingresar una nueva letra
} )