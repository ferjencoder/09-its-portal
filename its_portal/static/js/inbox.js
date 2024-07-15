// static/js/inbox.js

document.addEventListener('DOMContentLoaded', function() {
    // Obtener token CSRF
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Definir función para responder mensaje
    window.replyMessage = function(button) {
        const messageId = button.getAttribute('data-message-id');
        const messageEmail = button.getAttribute('data-message-email');
        const messageText = button.getAttribute('data-message-text');

        const replyMessageModal = new bootstrap.Modal(document.getElementById('replyMessageModal'));
        replyMessageModal.show();

        const emailInput = document.getElementById('reply-email');
        const messageTextarea = document.getElementById('reply-message');
        
        emailInput.value = messageEmail;
        messageTextarea.value = `\n\n---\nFrom: ${messageEmail}\nSent: ${new Date().toLocaleString()}\n\n${messageText}\n`;

        const form = document.getElementById('replyMessageForm');
        form.onsubmit = function(event) {
            event.preventDefault();
            const replyMessage = messageTextarea.value;
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
    };

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
