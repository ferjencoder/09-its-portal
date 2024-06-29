// its_portal/static/assets/js/edit_profile.js

document.addEventListener("DOMContentLoaded", function () {
    const predefinedImages = document.querySelectorAll(".predefined-image");
    const predefinedImageInput = document.getElementById("predefined_image");
    const profileImage = document.querySelector(".profile-image");

    predefinedImages.forEach(image => {
        image.addEventListener("click", function() {
            predefinedImages.forEach(img => img.classList.remove("selected"));
            this.classList.add("selected");
            predefinedImageInput.value = this.getAttribute("data-image-src");
        });
    });

    const selectImageButton = document.getElementById("selectImage");
    if (selectImageButton) {
        selectImageButton.addEventListener("click", function () {
            const selectedImage = document.querySelector(".predefined-image.selected");
            if (selectedImage) {
                predefinedImageInput.value = selectedImage.getAttribute("data-image-src");
                profileImage.src = selectedImage.getAttribute("data-image-src");
                $('#imageModal').modal('hide');
            }
        });
    }
});
