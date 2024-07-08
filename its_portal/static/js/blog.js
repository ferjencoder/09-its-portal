// main/blog.js

document.addEventListener('DOMContentLoaded', function() {
    const deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
    const deleteForm = document.getElementById('deleteForm');

    // Evento para mostrar el modal de eliminación de post
    document.querySelectorAll('[data-bs-toggle="modal"]').forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.getAttribute('data-post-id');
            deleteForm.setAttribute('action', `/en/blog/delete/${postId}/`);
        });
    });

    // Manejar la creación de categorías mediante AJAX
    const createCategoryForm = document.getElementById('createCategoryForm');
    createCategoryForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(createCategoryForm);
        fetch('/en/blog/create_category/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken'),
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload(); // Recargar la página para ver la nueva categoría
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error creating category');
        });
    });

    // Manejar la eliminación de categorías
    document.querySelectorAll('.delete-category').forEach(button => {
        button.addEventListener('click', function() {
            const categoryId = this.getAttribute('data-category-id');
            console.log(`Deleting category with ID: ${categoryId}`);
            
            if (confirm("¿Estás seguro de que deseas eliminar esta categoría?")) {
                fetch(`/en/blog/delete_category/${categoryId}/`, {
                    method: 'DELETE',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                })
                .then(response => {
                    if (!response.ok) {
                        return response.text().then(text => { throw new Error(text) });
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        location.reload(); // Recargar la página para ver los cambios
                    } else {
                        alert(data.message);
                    }
                })
                .catch(error => {
                    console.error('Error deleting category:', error);
                    alert('Error deleting category');
                });
            }
        });
    });
});

// Función para obtener el valor de la cookie CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
