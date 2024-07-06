//its_portal/static/assets/js/forum.js

document.addEventListener('DOMContentLoaded', function() {
    // Maneja la eliminación de posts
    const deleteModalElement = document.getElementById('deleteModal');
    if (deleteModalElement) {
        const deleteModal = new bootstrap.Modal(deleteModalElement);
        const deleteForm = document.getElementById('deleteForm');

        document.querySelectorAll('[data-bs-toggle="modal"]').forEach(button => {
            button.addEventListener('click', function() {
                const postId = this.getAttribute('data-post-id');
                deleteForm.setAttribute('action', deleteForm.getAttribute('action').replace('0', postId));
            });
        });
    }

    // Maneja la creación de posts mediante AJAX
    const createPostForm = document.getElementById('createPostForm');
    if (createPostForm) {
        createPostForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(createPostForm);
            fetch(createPostForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': createPostForm.querySelector('[name=csrfmiddlewaretoken]').value,
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.id) {
                    // Actualiza la lista de posts recientes incorporando el nuevo post
                    const newPostHTML = `
                        <div class="list-group-item">
                            <div class="d-flex align-items-start">
                                <img src="${data.author.profile_picture || '/static/assets/images/default_avatar.png'}" alt="${gettext('Avatar')}" class="rounded-circle me-3" width="40" height="40">
                                <div class="flex-fill">
                                    <a href="${data.url}">${data.title}</a>
                                    <p class="mb-0">${data.content}</p>
                                    <small class="text-muted">${data.created_at}</small>
                                </div>
                                <a href="${data.reply_url}" class="btn btn-primary ms-3">${gettext('Reply')}</a>
                            </div>
                        </div>`;
                    document.getElementById('recent-posts-list').insertAdjacentHTML('afterbegin', newPostHTML);
                } else {
                    alert(gettext('Error creating post'));
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }
});
