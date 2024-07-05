//its_portal/static/assets/js/menu_toggle.js

// sidebar menu toggle - oculta la sidebar
$(document).ready(function () {
    $('#menu-toggle').click(function () {
        $('#wrapper').toggleClass('toggled');
        const icon = $('#menu-toggle');
        if ($('#wrapper').hasClass('toggled')) {
            icon.removeClass('bi-arrow-bar-left').addClass('bi-arrow-bar-right');
            $('#sidebar-wrapper-expanded').addClass('d-none');
            $('#sidebar-wrapper-collapsed').removeClass('d-none');
        } else {
            icon.removeClass('bi-arrow-bar-right').addClass('bi-arrow-bar-left');
            $('#sidebar-wrapper-expanded').removeClass('d-none');
            $('#sidebar-wrapper-collapsed').addClass('d-none');
        }
    });
});
