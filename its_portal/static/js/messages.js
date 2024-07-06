//main/messages.js

document.addEventListener("DOMContentLoaded", function() {
    const editDeleteModal = document.getElementById("editDeleteModal");
    const deleteMessageForm = document.getElementById("deleteMessageForm");
    const messageContentTextarea = document.getElementById("messageContent");

    // Evento para mostrar el modal de edicion/eliminacion
    editDeleteModal.addEventListener("show.bs.modal", function(event) {
        const button = event.relatedTarget;
        const messageId = button.getAttribute("data-message-id");
        const messageContent = button.getAttribute("data-message-content");

        // URLs para editar y eliminar el mensaje
        const editActionUrl = `/en/messages/edit/${messageId}/`;
        const deleteActionUrl = `/en/messages/delete/${messageId}/`;

        // Asigna las URLs a los formularios de edicion y eliminacion
        document.getElementById("editMessageForm").setAttribute("action", editActionUrl);
        deleteMessageForm.setAttribute("action", deleteActionUrl);

        // Establece el contenido del mensaje en el textarea
        messageContentTextarea.value = messageContent;
    });
});
