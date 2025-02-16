function toggleMenu() {
    var menu = document.getElementById('dropdown-menu');

    // Alternar la clase 'active' para mostrar u ocultar el menú
    menu.classList.toggle('active');
}

// Cerrar el menú si se hace clic fuera de él
window.onclick = function(event) {
    var menu = document.getElementById('dropdown-menu');
    var button = document.querySelector('.menu-button');

    // Si se hace clic fuera del menú y del botón, se oculta
    if (!menu.contains(event.target) && !button.contains(event.target)) {
        menu.classList.remove('active');
    }
};
