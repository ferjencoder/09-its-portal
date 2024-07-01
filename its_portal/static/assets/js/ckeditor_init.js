// its_portal/static/assets/js/ckeditor_init.js

document.addEventListener("DOMContentLoaded", function() {
    function initializeEditor(theme) {
        ClassicEditor
            .create(document.querySelector('#id_body'), {
                toolbar: {
                    items: [
                        'undo', 'redo',
                        '|',
                        'heading',
                        '|',
                        'bold', 'italic',
                        '|',
                        'link', 'uploadImage', 'blockQuote',
                        '|',
                        'bulletedList', 'numberedList', 'outdent', 'indent'
                    ]
                },
                image: {
                    toolbar: [
                        'imageTextAlternative', 'imageStyle:side'
                    ]
                },
                simpleUpload: {
                    uploadUrl: '/blog/upload-image/',
                    withCredentials: false,
                    headers: {
                        'X-CSRFToken': getCsrfToken()
                    }
                },
                table: {
                    contentToolbar: [
                        'tableColumn', 'tableRow', 'mergeTableCells'
                    ]
                },
                height: 600,
                width: '100%',
                theme: theme === 'dark-mode' ? 'dark' : 'default'
            })
            .catch(error => {
                console.error('CKEditor error:', error);
            });

        // Class para el textarea del blog
        const textArea = document.querySelector('#id_body');
        if (theme === 'dark-mode') {
            textArea.classList.add('dark-textarea');
        } else {
            textArea.classList.remove('dark-textarea');
        }
    }

    function getCsrfToken() {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        return csrfToken ? csrfToken.value : '';
    }

    const currentTheme = document.body.classList.contains('dark-mode') ? 'dark-mode' : 'default';
    initializeEditor(currentTheme);
});
