//static/assets/js/form_validation.js

// js 4 disabling form subm 4 invalid fields
document.addEventListener('DOMContentLoaded', function() {
    'use strict';

    const forms = document.querySelectorAll('.needs-validation');

    forms.forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }

            form.classList.add('was-validated');
        });
    });

    // 🔍 CAPS LOCK
    const passwordField = document.getElementById('password');
    if (passwordField) {
        const capsLockWarning = document.querySelector('.caps-lock-warning');

        passwordField.addEventListener('keyup', function(event) {
            if (event.getModifierState('CapsLock')) {
                capsLockWarning.style.display = 'block';
            } else {
                capsLockWarning.style.display = 'none';
            }
        });
    }
});