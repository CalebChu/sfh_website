document.addEventListener("DOMContentLoaded", () => {
    const contentArea = document.getElementById("officers-content");

    for (const officer of contentArea.children) {
        for (const element of officer.children) {
            if (element.classList.contains("image")) {
                if (element.getAttribute("src") == "") {
                    element.src = "static/images/placeholder.jpg";
                }
            }
            else {
                for (const child of element.children) {
                    if (child.innerHTML.trim() === '' || child.innerHTML.trim() === 'None') { 
                        child.innerHTML = `No ${child.classList} information`;
                    }
                }
            }
        }
    }
});