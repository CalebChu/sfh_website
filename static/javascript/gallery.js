document.addEventListener("DOMContentLoaded", () =>  {
    const gallery = document.getElementById("gallery-content");

    for (const galleryItem of gallery.children) {
        if (!galleryItem.classList.contains("emphasized")) {
            continue;
        }

        const img = galleryItem.querySelector(".gallery-image");
        const aspectRatio = img.naturalWidth/img.naturalHeight;

        console.log(img.naturalWidth, aspectRatio);

        if (aspectRatio >= 1.7) {
            galleryItem.classList.add('wide');
        }
        if (aspectRatio <= 0.7) {
            galleryItem.classList.add('tall');
        }
        if (aspectRatio > 0.7 && aspectRatio < 1.7 && img.naturalWidth >= 3840) {
            galleryItem.classList.add('tall');
            galleryItem.classList.add('wide');
        }
    }
});