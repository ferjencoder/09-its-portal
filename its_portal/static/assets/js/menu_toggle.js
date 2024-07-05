//its_portal/static/assets/js/menu_toggle.js

//sidebar menu toggle - oculta la sidebar

$(document).ready(function () {
    $('#menu-toggle').click(function () {
        $('#wrapper').toggleClass('toggled');
        const icon = $('#menu-toggle');
        if ($('#wrapper').hasClass('toggled')) {
            icon.removeClass('bi-arrow-bar-left').addClass('bi-arrow-bar-right');
        } else {
            icon.removeClass('bi-arrow-bar-right').addClass('bi-arrow-bar-left');
        }
    });
});