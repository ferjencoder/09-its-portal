// static/js/contact.js

document.addEventListener('DOMContentLoaded',function() {
    console.log('working');
    
    const showModal = document.getElementById('show_success_modal').value;
    if (showModal === "True") {
        const successModal = new bootstrap.Modal(document.getElementById('successModal'));
        successModal.show();
    }
});
