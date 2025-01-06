function positionContent() {
    const contentArea = document.getElementById("content-area");
    const header = document.getElementById("header-body").offsetHeight;
    contentArea.style.top = String(header) + "px";
}

document.addEventListener("DOMContentLoaded", () => {
    positionContent();

    var ro = new ResizeObserver(entries => {
        for (let entry of entries) {
            const elem = entry.target;

            if (elem.id == 'header-body') {
                positionContent();
            }
        }
    });

    ro.observe(document.getElementById('header-body'));
});