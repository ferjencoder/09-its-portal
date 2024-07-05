// its_portal/static/js/dark_mode.js

document.addEventListener('DOMContentLoaded', function() {
    const darkModeIcon = document.querySelector('#dark-mode-icon');
    const body = document.body;
    const dropdowns = document.querySelectorAll('.dropdown');

    // Aplicar el tema oscuro o claro
    function applyTheme(theme) {
        body.classList.toggle('dark-mode', theme === 'dark-mode');
        if (darkModeIcon) {
            darkModeIcon.className = theme === 'dark-mode' ? 'fas fa-sun' : 'fas fa-moon';
        }
        dropdowns.forEach(dropdown => {
            dropdown.setAttribute('data-bs-theme', theme === 'dark-mode' ? 'dark' : 'light');
        });

        // Reinicializar el CKEditor con el tema correcto
        const editorElement = document.querySelector('#id_body');
        if (editorElement) {
            const editorInstance = editorElement.ckeditorInstance;
            if (editorInstance) {
                editorInstance.destroy().then(() => {
                    initializeEditor(theme);
                }).catch(error => {
                    console.error(error);
                });
            }
        }
    }

    const currentTheme = localStorage.getItem('theme') || 'light-mode';
    applyTheme(currentTheme);

    if (darkModeIcon) {
        darkModeIcon.addEventListener('click', function() {
            const newTheme = body.classList.contains('dark-mode') ? 'light-mode' : 'dark-mode';
            localStorage.setItem('theme', newTheme);
            applyTheme(newTheme);
        });
    }

    // Observar cambios en el local storage
    window.addEventListener('storage', function(event) {
        if (event.key === 'theme') {
            applyTheme(event.newValue);
        }
    });

    // Transiciones de página
    const links = document.querySelectorAll('a');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault(); // Prevenir comportamiento por defecto del enlace
            body.classList.add('fade-out'); // Añadir clase fade-out al body
            setTimeout(() => {
                window.location.href = this.href; // Esperar antes de cambiar de página
            }, 500);
        });
    });

    body.classList.add('fade-in'); // Añadir clase fade-in al cargar la página
});
