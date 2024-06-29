//its_portal/static/assets/js/menu_toggle.js

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
