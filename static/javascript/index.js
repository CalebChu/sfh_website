// function adjustContentArea() {
//     let vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
//     const contentArea = document.getElementById("header-container");
//     const indexHeader = document.getElementById("index-header");
//     const header = document.getElementById("header-body").offsetHeight;
//     contentArea.style.height = String(vh - header + 20) + "px";
//     indexHeader.style.height = String(vh - header + 20) + "px";
// }

// document.addEventListener("DOMContentLoaded", () => {
//     adjustContentArea();

//     var ro = new ResizeObserver(entries => {
//         for (let entry of entries) {
//             const elem = entry.target;

//             if (elem.id == 'header-body') {
//                 adjustContentArea();
//             }
//         }
//     });

//     ro.observe(document.getElementById('header-body'));
// });

// addEventListener("resize", () => {
//     adjustContentArea();
// });