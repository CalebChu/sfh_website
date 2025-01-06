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

document.addEventListener("DOMContentLoaded", () => {
    const opp_listings = document.querySelectorAll(".opp-listing");

    for (const opp_listing of opp_listings) {
        const register = opp_listing.querySelector(".register");

        if (!register) {
            continue;
        }
        
        register.addEventListener("click", () => {
            const id = opp_listing.id.split("-")[2];
            const text = register.querySelector(".register-text");

            fetch(window.location.href, {
                method: "POST",
                headers: {
                    'X-CSRFToken': getToken("csrftoken"),
                },
                body: id,
            })
            .then(response => response.json())
            .then(data => {
                console.log(data["status"]);
                if (data["status"] == "registered") {
                    register.classList.remove("unregister");
                    register.classList.add("registered");
                    text.innerHTML = "unregister";
                    opp_listing.classList.toggle('queued-tab-change');
                }
                if (data["status"] == "unregistered") {
                    register.classList.remove("registered");
                    register.classList.add("unregistered");
                    text.innerHTML = "register";
                    opp_listing.classList.toggle('queued-tab-change');
                }
            })
            .catch(error => {
                console.log("Error: ", error);
            })
        });
    }
});