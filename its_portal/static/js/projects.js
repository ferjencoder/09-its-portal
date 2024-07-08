//main/projects.js

document.addEventListener("DOMContentLoaded", function() {
        // Modal para eliminar entregable
        const deleteDeliverableModal = document.getElementById('deleteDeliverableModal');
        deleteDeliverableModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const deliverableId = button.getAttribute('data-deliverable-id');
            const deliverableName = button.getAttribute('data-deliverable-name');
            const modalDeliverableName = deleteDeliverableModal.querySelector('#modalDeliverableName');
            modalDeliverableName.textContent = deliverableName;

            const deleteDeliverableForm = document.getElementById('deleteDeliverableForm');
            deleteDeliverableForm.action = '{% url "projects_app:delete_deliverable" 0 %}'.replace('0', deliverableId);
        });

        // modal para subir documento
        const uploadDocumentModal = document.getElementById('uploadDocumentModal');
        uploadDocumentModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const deliverableId = button.getAttribute('data-deliverable-id');
            const uploadDocumentForm = document.getElementById('uploadDocumentForm');
            uploadDocumentForm.action = '{% url "projects_app:upload_document" 0 %}'.replace('0', deliverableId);
        });

        // modal para aprobar documento
        const approveDocumentModal = document.getElementById('approveDocumentModal');
        approveDocumentModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const deliverableId = button.getAttribute('data-deliverable-id');
            const approveDocumentForm = document.getElementById('approveDocumentForm');
            approveDocumentForm.action = '{% url "projects_app:approve_document" 0 %}'.replace('0', deliverableId);
        });

        // Modal para editar entregable
        const editDeliverableModal = document.getElementById('editDeliverableModal');
        editDeliverableModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const deliverableId = button.getAttribute('data-deliverable-id');
            const editDeliverableForm = document.getElementById('editDeliverableForm');
            editDeliverableForm.action = '{% url "projects_app:edit_deliverable" 0 %}'.replace('0', deliverableId);

            // form con la info del deliverable
            const deliverable = button.getAttribute('data-deliverable');
            const parsedDeliverable = JSON.parse(deliverable);
            document.getElementById('deliverableName').value = parsedDeliverable.name;
            document.getElementById('deliverableDueDate').value = parsedDeliverable.due_date;
            document.getElementById('deliverableStatus').value = parsedDeliverable.status;
        });
    });