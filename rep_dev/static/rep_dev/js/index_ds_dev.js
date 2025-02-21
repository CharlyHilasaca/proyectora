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
