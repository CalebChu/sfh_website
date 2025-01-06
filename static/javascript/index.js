function adjustContentArea() {
    let vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
    const contentArea = document.getElementById("content-area");
    const header = document.getElementById("header-body").offsetHeight;
    contentArea.style.height = String(vh - header) + "px";
}

document.addEventListener("DOMContentLoaded", () => {
    adjustContentArea();

    var ro = new ResizeObserver(entries => {
        for (let entry of entries) {
            const elem = entry.target;

            if (elem.id == 'header-body') {
                adjustContentArea();
            }
        }
    });

    ro.observe(document.getElementById('header-body'));
});

addEventListener("resize", () => {
    adjustContentArea();
});