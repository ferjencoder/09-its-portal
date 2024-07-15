// static/js/inbox.js

// static/js/inbox.js

document.addEventListener('DOMContentLoaded', function() {
    // Obtener token CSRF
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Abrir modal y establecer el email
    const replyMessageModal = document.getElementById('replyMessageModal');
    replyMessageModal.addEventListener('show.bs.modal', function(event) {
        const button = event.relatedTarget;
        const messageId = button.getAttribute('data-message-id');
        const messageEmail = button.getAttribute('data-message-email');
        const emailInput = replyMessageModal.querySelector('#reply-email');
        emailInput.value = messageEmail;

        const form = document.getElementById('replyMessageForm');
        form.onsubmit = function(event) {
            event.preventDefault();
            const replyMessage = document.getElementById('reply-message').value;
            fetch(`/communications/reply/${messageId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: replyMessage })
            }).then(response => response.json()).then(data => {
                if (data.status === "ok") {
                    window.location.reload();
                } else {
                    alert("Error al responder el mensaje.");
                }
            }).catch(error => console.error('Error:', error));
        };
    });

    // Definir función para archivar mensaje
    window.archiveMessage = function(button) {
        const messageId = button.getAttribute('data-message-id');
        fetch(`/communications/archive/${messageId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            }
        }).then(response => response.json()).then(data => {
            if (data.status === "ok") {
                window.location.reload();
            } else {
                alert("Error al archivar el mensaje.");
            }
        }).catch(error => console.error('Error:', error));
    }
});
