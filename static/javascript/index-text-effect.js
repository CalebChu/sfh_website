document.addEventListener("DOMContentLoaded", () => {
    const stats = document.querySelectorAll(".header-stat-container");

    for (const stat of stats) {
        const statValue = stat.querySelector(".header-stat-value");
        const value = parseInt(statValue.innerHTML);
    }
});