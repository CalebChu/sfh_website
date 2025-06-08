document.addEventListener("DOMContentLoaded", () => {
    const cover = document.getElementById("cover");
    const opener = document.getElementById("menu-opener-wrapper");
    const sidebar = document.getElementById("sidebar");
    const closeMenu = document.getElementById("close-menu");
    var opening;
    var opened;
    
    opener.addEventListener("click", () => {
        opening = true;
        sidebar.classList.add("open");
        cover.classList.remove("inactive");
        cover.classList.add("active");

        let vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
        let size = vw - sidebar.offsetWidth;
        cover.style.width = String(size) + "px";
   });

    cover.addEventListener("click", () => {
        opening = false;
        sidebar.classList.remove("open");
        cover.classList.remove("active");
        closeMenu.classList.remove("hover-active");

        cover.style.width = "100%";
   });

    cover.addEventListener("transitionend", (e) => {
        if (e.propertyName != "background-color") {
            return;
        }
        if (opening == false) {
            cover.classList.add("inactive");
            opened = false;
        }
        if (opening == true) {
            opened = true;
            closeMenu.classList.add("hover-active");
        }
    });

    addEventListener("resize", () => {
        if (!opened) {
            return;
        }
        
        let vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
        let size = vw - sidebar.offsetWidth;
        cover.style.width = String(size) + "px";
    });
});