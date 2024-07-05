//static/assets/js/form_validation.js

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

    // Manejo de la advertencia de CAPS LOCK
    const passwordField = document.getElementById('id_current_password');
    if (passwordField) {
        const capsLockWarning = document.querySelector('.caps-lock-warning');

        passwordField.addEventListener('keyup', function(event) {
            if (capsLockWarning) {
                if (event.getModifierState('CapsLock')) {
                    capsLockWarning.style.display = 'block';
                } else {
                    capsLockWarning.style.display = 'none';
                }
            }
        });

        passwordField.addEventListener('blur', function() {
            // Mostrar error si la contraseña actual es incorrecta
            const currentPasswordError = document.querySelector('.invalid-feedback.d-block');
            if (currentPasswordError && !this.checkValidity()) {
                currentPasswordError.style.display = 'block';
            }
        });
    }
});
