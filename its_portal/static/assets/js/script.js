//its_portal/static/assets/js/scripts.js

document.addEventListener('DOMContentLoaded', function () {
    const darkModeIcon = document.querySelector('#dark-mode-icon');
    const dropdownMenus = document.querySelectorAll('.dropdown-menu');

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

    const predefinedImages = document.querySelectorAll('.predefined-image');
    const selectImageButton = document.getElementById('selectImage');
    let selectedImage = null;

    predefinedImages.forEach(image => {
        image.style.cursor = 'pointer';
        image.addEventListener('click', function () {
            predefinedImages.forEach(img => img.classList.remove('selected'));
            this.classList.add('selected');
            selectedImage = this.getAttribute('data-image-src');
        });
    });

    selectImageButton.addEventListener('click', function () {
        if (selectedImage) {
            const predefinedImageSelect = document.getElementById('id_profile_picture');
            predefinedImageSelect.value = selectedImage;
            const imgPreview = document.querySelector('.rounded-circle');
            imgPreview.src = selectedImage;
            $('#imageModal').modal('hide');
        }
    });
});

$(document).ready(function () {
    $('#menu-toggle').click(function () {
        $('#wrapper').toggleClass('toggled');
        const icon = $('#menu-toggle i');
        const sidebarIcon = $('#sidebar-toggle-icon');
        if ($('#wrapper').hasClass('toggled')) {
            icon.removeClass('bi-arrow-bar-left').addClass('bi-arrow-bar-right');
            sidebarIcon.removeClass('bi-box-arrow-left').addClass('bi-box-arrow-right');
        } else {
            icon.removeClass('bi-arrow-bar-right').addClass('bi-arrow-bar-left');
            sidebarIcon.removeClass('bi-box-arrow-right').addClass('bi-box-arrow-left');
        }
    });
});