//its_portal/static/assets/js/dark_mode.js
    
document.addEventListener('DOMContentLoaded',function() {
    const darkModeIcon = document.querySelector('#dark-mode-icon');
    const dropdownMenus = document.querySelectorAll('.dropdown-menu');

    if (darkModeIcon) {
        const currentTheme = localStorage.getItem('theme') ? localStorage.getItem('theme') : null;

        if (currentTheme) {
            document.body.classList.add(currentTheme);
            darkModeIcon.className = currentTheme === 'dark-mode' ? 'fas fa-sun' : 'fas fa-moon';
            dropdownMenus.forEach(menu => {
                menu.classList.toggle('dropdown-menu-dark', currentTheme === 'dark-mode');
            });
        }

        darkModeIcon.addEventListener('click', function () {
            if (document.body.classList.contains('dark-mode')) {
                document.body.classList.remove('dark-mode');
                localStorage.setItem('theme', 'light-mode');
                darkModeIcon.className = 'fas fa-moon';
                dropdownMenus.forEach(menu => {
                    menu.classList.remove('dropdown-menu-dark');
                });
            } else {
                document.body.classList.add('dark-mode');
                localStorage.setItem('theme', 'dark-mode');
                darkModeIcon.className = 'fas fa-sun';
                dropdownMenus.forEach(menu => {
                    menu.classList.add('dropdown-menu-dark');
                });
            }
        });
    }
});
