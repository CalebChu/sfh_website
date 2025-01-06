document.addEventListener("DOMContentLoaded", () => {
    const allButtons = document.querySelectorAll(".copy-button");

    for (const button of allButtons) {
        button.addEventListener("click", () => {
            const text = document.querySelector("#code-"+button.value).innerHTML;
            navigator.clipboard.writeText(text);
        });
    }
});