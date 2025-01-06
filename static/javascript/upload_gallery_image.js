
document.addEventListener("DOMContentLoaded", () => {
    const imgUpload = document.getElementById("id_image");
    const imgPreview = document.getElementById("img-preview");

    imgUpload.onchange = function() {
        const [file] = imgUpload.files;
        console.log("updated");
        if (file) { 
            console.log("updated preview")
            imgPreview.src = URL.createObjectURL(file);
        }
    }
});