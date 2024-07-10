// main/projects.js

document.addEventListener("DOMContentLoaded", function() {
    // Modal para eliminar deliverable
    const deleteDeliverableModal = document.getElementById('deleteDeliverableModal');
    if (deleteDeliverableModal) {
        deleteDeliverableModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const deliverableId = button.getAttribute('data-deliverable-id');
            const deliverableName = button.getAttribute('data-deliverable-name');
            const modalDeliverableName = deleteDeliverableModal.querySelector('#modalDeliverableName');
            modalDeliverableName.textContent = deliverableName;

            const deleteDeliverableForm = document.getElementById('deleteDeliverableForm');
            deleteDeliverableForm.action = deleteDeliverableForm.action.replace('0', deliverableId);
        });
    }

    // modal para subir documento
    const uploadDocumentModal = document.getElementById('uploadDocumentModal');
    if (uploadDocumentModal) {
        uploadDocumentModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const deliverableId = button.getAttribute('data-deliverable-id');
            const uploadDocumentForm = document.getElementById('uploadDocumentForm');
            uploadDocumentForm.action = uploadDocumentForm.action.replace('0', deliverableId);
        });
    }

    // modal para aprobar documento
    const approveDocumentModal = document.getElementById('approveDocumentModal');
    if (approveDocumentModal) {
        approveDocumentModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const deliverableId = button.getAttribute('data-deliverable-id');
            const approveDocumentForm = document.getElementById('approveDocumentForm');
            approveDocumentForm.action = approveDocumentForm.action.replace('0', deliverableId);
        });
    }

    // Modal para editar deliverable
    const editDeliverableModal = document.getElementById('editDeliverableModal');
    if (editDeliverableModal) {
        editDeliverableModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const deliverableId = button.getAttribute('data-deliverable-id');
            const editDeliverableForm = document.getElementById('editDeliverableForm');
            editDeliverableForm.action = editDeliverableForm.action.replace('0', deliverableId);

            // form con la info del deliverable
            const deliverable = button.getAttribute('data-deliverable');
            const parsedDeliverable = JSON.parse(deliverable);
            document.getElementById('deliverableName').value = parsedDeliverable.name;
            document.getElementById('deliverableDueDate').value = parsedDeliverable.due_date;
            document.getElementById('deliverableStatus').value = parsedDeliverable.status;
        });
    }

    // AJAX form para agregar tasks
    const addTaskForm = document.querySelector("#addTaskForm");
    if (addTaskForm) {
        addTaskForm.addEventListener("submit", function(event) {
            event.preventDefault();
            const form = event.target;

            fetch(form.action, {
                method: form.method,
                body: new FormData(form),
                headers: {
                    "X-CSRFToken": form.querySelector('[name="csrfmiddlewaretoken"]').value
                }
            }).then(response => {
                if (response.ok) {
                    window.location.reload();
                } else {
                    console.error("Error submitting form");
                }
            }).catch(error => {
                console.error("Error submitting form:", error);
            });
        });
    }

    // AJAX form para actualizar tasks
    const updateTaskButtons = document.querySelectorAll('.update-task-status');
    updateTaskButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            const taskId = event.currentTarget.getAttribute('data-task-id');
            const taskStatus = event.currentTarget.getAttribute('data-task-status');
            const form = document.querySelector('#updateTaskStatusForm');
            form.action = form.action.replace('0', taskId);
            form.querySelector('#id_status').value = taskStatus;
            const updateTaskStatusModal = new bootstrap.Modal(document.getElementById('updateTaskStatusModal'));
            updateTaskStatusModal.show();
        });
    });

    // AJAX form para agregar deliverables
    const addDeliverableForm = document.querySelector("#addDeliverableForm");
    if (addDeliverableForm) {
        addDeliverableForm.addEventListener("submit", function(event) {
            event.preventDefault();
            const form = event.target;

            fetch(form.action, {
                method: form.method,
                body: new FormData(form),
                headers: {
                    "X-CSRFToken": form.querySelector('[name="csrfmiddlewaretoken"]').value
                }
            }).then(response => {
                if (response.ok) {
                    response.json().then(data => {
                        const newDeliverable = document.createElement("li");
                        newDeliverable.classList.add("list-group-item");
                        newDeliverable.innerHTML = `<a href="/en/projects/documents/${data.document_id}/">${data.document_name}</a>`;
                        document.querySelector(".deliverables-list").appendChild(newDeliverable);
                        const addDeliverableModal = bootstrap.Modal.getInstance(document.getElementById("addDeliverableModal"));
                        addDeliverableModal.hide();
                    });
                } else {
                    console.error("Error submitting form");
                }
            }).catch(error => {
                console.error("Error submitting form:", error);
            });
        });
    }

    // AJAX form para agregar proyectos
    const addProjectForm = document.querySelector("#addProjectForm");
    if (addProjectForm) {
        addProjectForm.addEventListener("submit", function(event) {
            event.preventDefault();
            const form = event.target;

            fetch(form.action, {
                method: form.method,
                body: new FormData(form),
                headers: {
                    "X-CSRFToken": form.querySelector('[name="csrfmiddlewaretoken"]').value
                }
            }).then(response => {
                if (response.ok) {
                    response.json().then(data => {
                        window.location.reload();
                    });
                } else {
                    console.error("Error submitting form");
                }
            }).catch(error => {
                console.error("Error submitting form:", error);
            });
        });
    }
});
