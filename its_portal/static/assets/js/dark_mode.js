// its_portal/static/assets/js/dark_mode.js

document.addEventListener('DOMContentLoaded', function() {
    const darkModeIcon = document.querySelector('#dark-mode-icon');
    const body = document.body;
    const dropdowns = document.querySelectorAll('.dropdown');

    function applyTheme(theme) {
        body.classList.toggle('dark-mode', theme === 'dark-mode');
        if (darkModeIcon) {
            darkModeIcon.className = theme === 'dark-mode' ? 'fas fa-sun' : 'fas fa-moon';
        }
        dropdowns.forEach(dropdown => {
            dropdown.setAttribute('data-bs-theme', theme === 'dark-mode' ? 'dark' : 'light');
        });
    }

    const currentTheme = localStorage.getItem('theme') ? localStorage.getItem('theme') : 'light-mode';
    applyTheme(currentTheme);

    if (darkModeIcon) {
        darkModeIcon.addEventListener('click', function () {
            const newTheme = body.classList.contains('dark-mode') ? 'light-mode' : 'dark-mode';
            localStorage.setItem('theme', newTheme);
            applyTheme(newTheme);
        });
    }
});



