// static/assets/js/form_validation.js

document.addEventListener('DOMContentLoaded', function() {
    'use strict';

    const forms = document.querySelectorAll('.needs-validation');

    forms.forEach(form => {
        form.addEventListener('submit', event => {
            const password1 = form.querySelector('#id_password1');
            const password2 = form.querySelector('#id_password2');

            // Check si el form es válido
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }

            // Check si las pass matchean
            if (password1 && password2 && password1.value !== password2.value) {
                event.preventDefault();
                event.stopPropagation();
                password2.setCustomValidity('Passwords must match.');
                password2.reportValidity(); // Mostrar el error de inmediato
            } else {
                password2.setCustomValidity('');
            }

            form.classList.add('was-validated');
        });
    });

    // Manejo de la advertencia de CAPS LOCK
    const passwordFields = document.querySelectorAll('#id_password1, #id_password2, #id_password');
    passwordFields.forEach(passwordField => {
        const capsLockWarning = passwordField.parentElement.querySelector('.caps-lock-warning');

        passwordField.addEventListener('keyup', function(event) {
            if (capsLockWarning) {
                if (event.getModifierState('CapsLock')) {
                    capsLockWarning.style.display = 'block';
                } else {
                    capsLockWarning.style.display = 'none';
                }
            }
        });
    });
});
