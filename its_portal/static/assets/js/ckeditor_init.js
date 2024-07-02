// its_portal/static/assets/js/ckeditor_init.js

import {
    ClassicEditor,
    Essentials,
    Bold,
    Italic,
    Paragraph,
    SimpleUploadAdapter,
    Heading,
    Link,
    Image,
    ImageUpload,
    BlockQuote,
    List,
    Indent
} from 'ckeditor5';

document.addEventListener("DOMContentLoaded", function() {
    function initializeEditor(theme) {
        const editorElement = document.querySelector('#id_body');
        if (!editorElement) return;

        const currentLanguage = document.documentElement.lang || 'en';
        const uploadUrl = `/${currentLanguage}/blog/upload-image/`;

        ClassicEditor
            .create(editorElement, {
                plugins: [
                    Essentials,
                    Bold,
                    Italic,
                    Paragraph,
                    SimpleUploadAdapter,
                    Heading,
                    Link,
                    Image,
                    ImageUpload,
                    BlockQuote,
                    List,
                    Indent
                ],
                toolbar: {
                    items: [
                        'undo', 'redo',
                        '|',
                        'heading',
                        '|',
                        'bold', 'italic',
                        '|',
                        'link', 'imageUpload', 'blockQuote', 'insertTable', 'mediaEmbed',
                        '|',
                        'bulletedList', 'numberedList', 'outdent', 'indent'
                    ]
                },
                simpleUpload: {
                    uploadUrl: uploadUrl,
                    withCredentials: false,
                    headers: {
                        'X-CSRFToken': getCsrfToken()
                    }
                },
                height: 600,
                width: '100%',
                theme: theme === 'dark-mode' ? 'dark' : 'default'
            })
            .then(editor => {
                console.log('Editor initialized:', editor);
                window.editorInstance = editor;

                // Hide the original textarea and ensure it's not required
                const textarea = document.querySelector('textarea[name="body"]');
                if (textarea) {
                    textarea.style.display = 'none';  // Hide the textarea
                    textarea.required = false;        // It should not be required as it's hidden
                }
            })
            .catch(error => {
                console.error('CKEditor error:', error);
            });

        if (theme === 'dark-mode') {
            editorElement.classList.add('dark-textarea');
        } else {
            editorElement.classList.remove('dark-textarea');
        }
    }

    function getCsrfToken() {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        return csrfToken ? csrfToken.value : '';
    }

    function makeBodyVisible() {
        const textarea = document.querySelector('textarea[name="body"]');
        if (textarea) {
            textarea.value = window.editorInstance.getData();  // Sync CKEditor data to the hidden textarea
        }
    }

    const currentTheme = document.body.classList.contains('dark-mode') ? 'dark-mode' : 'default';
    initializeEditor(currentTheme);

    // Attach the form submit handler to ensure the textarea gets the CKEditor data
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', makeBodyVisible);
    }
});
