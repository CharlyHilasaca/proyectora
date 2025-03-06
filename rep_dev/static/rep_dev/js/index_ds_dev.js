$(document).ready(function () {
    const numPuntos = 200;
    const maxDistPuntos = 100;
    const velocidad = 0.5;
    const puntos = [];
    const canvas = $("#canvas-lineas")[0];
    const ctx = canvas.getContext("2d");

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    function generarPosicion() {
        return {
            x: Math.random() * window.innerWidth,
            y: Math.random() * window.innerHeight,
            vx: (Math.random() - 0.5) * velocidad,
            vy: (Math.random() - 0.5) * velocidad
        };
    }

    function crearPuntos() {
        for (let i = 0; i < numPuntos; i++) {
            puntos.push(generarPosicion());
        }
    }

    function actualizarPuntos() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        for (let i = 0; i < numPuntos; i++) {
            let p = puntos[i];
            p.x += p.vx;
            p.y += p.vy;

            if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
            if (p.y < 0 || p.y > canvas.height) p.vy *= -1;
        }

        dibujarLineas();
        dibujarPuntos();
        requestAnimationFrame(actualizarPuntos);
    }

    function dibujarPuntos() {
        ctx.fillStyle = "white";
        for (let p of puntos) {
            ctx.beginPath();
            ctx.arc(p.x, p.y, 2, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    function dibujarLineas() {
        ctx.strokeStyle = "white";
        ctx.lineWidth = 0.5;
        for (let i = 0; i < numPuntos; i++) {
            for (let j = i + 1; j < numPuntos; j++) {
                let dx = puntos[i].x - puntos[j].x;
                let dy = puntos[i].y - puntos[j].y;
                let dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < maxDistPuntos) {
                    ctx.globalAlpha = 1 - dist / maxDistPuntos;
                    ctx.beginPath();
                    ctx.moveTo(puntos[i].x, puntos[i].y);
                    ctx.lineTo(puntos[j].x, puntos[j].y);
                    ctx.stroke();
                }
            }
        }
        ctx.globalAlpha = 1;
    }

    $(window).resize(() => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });

    crearPuntos();
    actualizarPuntos();
});

document.addEventListener("DOMContentLoaded", function () {
    let items = document.querySelectorAll(".content-item");
    let index = 1; // Elemento central predeterminado

    function actualizarVista() {
        items.forEach(item => {
            item.classList.add("hidden"); // Oculta todos
            item.classList.remove("selected"); // Quita la selección
        });

        let totalItems = items.length;

        // Calcular qué elementos deben mostrarse
        let start = Math.max(0, index - 1); // No permite valores negativos
        let end = Math.min(totalItems - 1, index + 1); // No permite pasar el límite

        // Ajustar cuando el índice está en los extremos
        if (index === 0) {
            end = Math.min(2, totalItems - 1); // Mostrar hasta 3 primeros elementos
        } else if (index === totalItems - 1) {
            start = Math.max(totalItems - 3, 0); // Mostrar los últimos 3 elementos
        }

        // Mostrar los elementos dentro del rango calculado
        for (let i = start; i <= end; i++) {
            items[i].classList.remove("hidden");
        }

        // Marcar el elemento central como seleccionado
        items[index].classList.add("selected");
    }

    document.querySelector(".content-m").addEventListener("click", (e) => {
        let clickedIndex = Array.from(items).indexOf(e.target.closest(".content-item"));
        if (clickedIndex === -1) return;

        if (clickedIndex < index && index > 0) {
            index--; // Mover a la izquierda (si no es el primero)
        } else if (clickedIndex > index && index < items.length - 1) {
            index++; // Mover a la derecha (si no es el último)
        }

        actualizarVista();
    });

    actualizarVista();
});

// filepath: /c:/DjangoProyects/proyecto_principal/rep_dev/static/rep_dev/js/index_ds_dev.js
function toggleMenu() {
    var menu = document.getElementById('dropdown-menu');

    // Alternar la clase 'active' para mostrar u ocultar el menú
    menu.classList.toggle('active');
}

// Cerrar el menú si se hace clic fuera de él
window.onclick = function (event) {
    var menu = document.getElementById('dropdown-menu');
    var button = document.querySelector('.menu-button');

    // Si se hace clic fuera del menú y del botón, se oculta
    if (!menu.contains(event.target) && !button.contains(event.target)) {
        menu.classList.remove('active');
    }
};

document.addEventListener("DOMContentLoaded", function () {
    const menuOptions = document.querySelectorAll(".menu-options a");
    const mains = document.querySelectorAll("main[id^='opcion']"); // Obtiene todos los divs con ID que empieza con "opcion"

    // Mostrar la primera opción por defecto
    showContent("opcion1");

    // Agregar evento a cada opción del menú
    menuOptions.forEach(option => {
        option.addEventListener("click", function (event) {
            event.preventDefault(); // Evita que el enlace cambie la URL

            // Remover la clase 'active' de todas las opciones
            menuOptions.forEach(item => item.classList.remove("active"));

            // Agregar la clase 'active' a la opción seleccionada
            this.classList.add("active");

            // Mostrar el contenido correspondiente
            const optionId = this.getAttribute("data-content");
            showContent(optionId);

            // Ocultar el menú después de seleccionar
            document.getElementById("dropdown-menu").classList.remove("active");
        });
    });

    // Función para mostrar solo el div correspondiente
    function showContent(option) {
        mains.forEach(main => {
            if (main.id === option) {
                main.style.display = "flex"; // Mostrar el div seleccionado
            } else {
                main.style.display = "none"; // Ocultar los demás divs
            }
        });
    }
});
