function getToken(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie != '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0,name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function update_table(data) {
    const table = document.getElementById("officer-codes-table");
    const row = document.querySelector(".officer-codes-table-header").cloneNode(true);
    row.id = data["id"];

    row.querySelector(".id").innerHTML = data["id"];
    row.querySelector(".code").innerHTML = data["code"];
    row.querySelector(".code").id = "code-"+data["id"];
    row.querySelector(".active").innerHTML = data["active"];
    row.querySelector(".used-by").innerHTML = data["used_by"];
    row.querySelector(".copy-button").value = data["id"];
    row.querySelector(".copy-button").style.display = "flex";

    row.querySelector(".copy-button").addEventListener("click", () => {
        const text = document.querySelector("#code-"+data["id"]).innerHTML;
        navigator.clipboard.writeText(text);
    });

    table.appendChild(row);
}

document.addEventListener("DOMContentLoaded", () => {
    const createNewButton = document.getElementById("create-new");

    createNewButton.addEventListener("click", () => {
        fetch(window.location.href, {
            method: "POST",
            headers: {
                'X-CSRFToken': getToken("csrftoken"),
            },
        })
        .then(response => response.json())
        .then(data => {
            // console.log("Success: ", data);
            update_table(data);
        })
        .catch(error => {
            console.log("Error: ", error);
        })
    });
});