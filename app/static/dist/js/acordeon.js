'use strict'

const bloque    = document.querySelectorAll('.bloque')
const h2        = document.querySelectorAll('.h2')
const article   = document.querySelector('.article')
    

// Cuando CLICK en h2,
    // QUITAR la clase activo de TODOS los bloque
    // Vamos a añadir la clase activo al BLOQUE con la POSICION del h2

// Recorrer TODOS los h2
h2.forEach((cadaH2, i) => {
    // Asignando un CLICK a cada h2
    h2[i].addEventListener('click', (event) => {
        // Evitar que el click en h2 se propague al article
        event.stopPropagation();

        // Recorrer TODOS los bloque
        bloque.forEach((cadaBloque) => {
            // Quitamos la clase activo de TODOS los bloques
            cadaBloque.classList.remove('activo');
        });

        // Añadiendo la clase activo al bloque cuya posición sea igual al del h2
        bloque[i].classList.add('activo');
    });
});

// Agregar un evento de click al article
article.addEventListener('click', (event) => {
    // Verificar si el click fue en un enlace <a> dentro de un div con clase "contenido"
    if (event.target.closest('.contenido')) {
        return; // No hacer nada si el click fue en un enlace <a> dentro de "contenido"
    }

    // Recorrer TODOS los bloque
    bloque.forEach((cadaBloque) => {
        // Quitamos la clase activo de TODOS los bloques
        cadaBloque.classList.remove('activo');
    });
});