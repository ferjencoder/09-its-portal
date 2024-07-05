// its_portal/static/assets/js/edit_profile.js

document.addEventListener("DOMContentLoaded", function () {
    const predefinedImages = document.querySelectorAll(".predefined-image");
    const predefinedImageInput = document.getElementById("predefined_image");
    const profileImage = document.querySelector(".profile-image");
    const uploadImageInput = document.getElementById("id_profile_picture");
    const selectImageButton = document.getElementById("selectImage");
    const form = document.querySelector("form");

    predefinedImages.forEach(image => {
        image.addEventListener("click", function() {
            predefinedImages.forEach(img => img.classList.remove("selected"));
            this.classList.add("selected");
            predefinedImageInput.value = this.getAttribute("data-image-src");
        });
    });

    if (selectImageButton) {
        selectImageButton.addEventListener("click", function () {
            const selectedImage = document.querySelector(".predefined-image.selected");
            if (selectedImage) {
                predefinedImageInput.value = selectedImage.getAttribute("data-image-src");
                profileImage.src = selectedImage.getAttribute("data-image-src");
            }
            if (uploadImageInput.files.length > 0) {
                const file = uploadImageInput.files[0];
                const reader = new FileReader();
                reader.onload = function (e) {
                    profileImage.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
            $('#imageModal').modal('hide'); // Cerrar el modal
        });
    }

    if (form) {
        form.addEventListener("submit", function (e) {
            e.preventDefault(); // Prevenir envío por defecto
            form.submit(); // Enviar el formulario manualmente
        });
    }
});




