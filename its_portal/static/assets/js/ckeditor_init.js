// its_portal/static/assets/js/ckeditor_init.js

document.addEventListener("DOMContentLoaded", function() {
    function initializeEditor(theme) {
        ClassicEditor
            .create(document.querySelector('#id_body'), {
                toolbar: {
                    items: [
                        'heading', '|',
                        'bold', 'italic', 'underline', 'strikethrough', 'subscript', 'superscript', '|',
                        'link', 'blockquote', 'code', 'codeBlock', '|',
                        'numberedList', 'bulletedList', 'todoList', '|',
                        'insertImage', 'mediaEmbed', 'insertTable', '|',
                        'textColor', 'bgColor', '|',
                        'alignment', '|',
                        'undo', 'redo'
                    ]
                },
                image: {
                    toolbar: [
                        'imageTextAlternative', 'imageStyle:full', 'imageStyle:side'
                    ]
                },
                table: {
                    contentToolbar: [
                        'tableColumn', 'tableRow', 'mergeTableCells'
                    ]
                },
                height: 400,
                width: '100%',
                theme: theme === 'dark-mode' ? 'dark' : 'default'
            })
            .catch(error => {
                console.error(error);
            });

        // Class para el texarea del blog
        const textArea = document.querySelector('#id_body');
        if (theme === 'dark-mode') {
            textArea.classList.add('dark-textarea');
        } else {
            textArea.classList.remove('dark-textarea');
        }
    }

    const currentTheme = document.body.classList.contains('dark-mode') ? 'dark-mode' : 'default';
    initializeEditor(currentTheme);

    document.getElementById('dark-mode-icon').addEventListener('click', function() {
        // Toggle darkmode
        const newTheme = document.body.classList.contains('dark-mode') ? 'default' : 'dark-mode';
        // Reincializar ckeditor con el theme correcto
        const editorElement = document.querySelector('#id_body');
        if (editorElement) {
            const editorInstance = ClassicEditor.instances.id_body;
            if (editorInstance) {
                editorInstance.destroy().then(() => {
                    initializeEditor(newTheme);
                }).catch(error => {
                    console.error(error);
                });
            }
        }
    });
});