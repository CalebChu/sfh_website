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

function markAttendance(id, action, element) {
    fetch(window.location.href, {
        method: "POST",
        headers: {
            'X-CSRFToken': getToken("csrftoken"),
        },
        body: JSON.stringify({
            "id": id,
            "action": action,
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data["status"] == action) {
            const toRemove = action == "present" ? "absent" : "present";

            element.classList.add(action);
            element.classList.remove(toRemove);

            const oldParent = element.parentNode;
            const newParent = document.querySelector(`.show-${action} .members-container`);
            newParent.appendChild(element);

            const oldParentLabel = document.querySelector(`.show-${toRemove} .attendance-opener`);
            const newParentLabel = document.querySelector(`.show-${action} .attendance-opener`);
            oldParentLabel.innerHTML = `<i class='bx bx-chevron-right icon-open'></i>show members marked ${toRemove} (${oldParent.childElementCount})`;
            newParentLabel.innerHTML = `<i class='bx bx-chevron-right icon-open'></i>show members marked ${action} (${newParent.childElementCount})`;
        }
    })
    .catch(error => {
        console.log("Error: ", error);
    })
}

document.addEventListener("DOMContentLoaded", () => {
    const attendance_listings = document.querySelectorAll(".attendance-listing");

    for (const attendance_listing of attendance_listings) {
        const check = attendance_listing.querySelector(".mark-present");
        const absent = attendance_listing.querySelector(".mark-absent");

        if (!check) {
            continue;
        }
        
        check.addEventListener("click", () => {
            if (attendance_listing.classList.contains("present")) {
                return;
            }

            const id = attendance_listing.id;
            markAttendance(id, "present", attendance_listing);
        });
        absent.addEventListener("click", () => {
            if (attendance_listing.classList.contains("absent")) {
                return;
            }

            const id = attendance_listing.id;
            markAttendance(id, "absent", attendance_listing);
        });
    }

    const openerPresent = document.querySelector(`.show-present .attendance-opener`);
    const openerAbsent = document.querySelector(`.show-absent .attendance-opener`);

    openerPresent.addEventListener('click', () => {
        const container = openerPresent.parentNode;
        const membersContainer = container.querySelector(".members-container");

        container.classList.toggle("open");
        container.classList.toggle("closed");
        membersContainer.classList.toggle("members-container-closed");
        membersContainer.classList.toggle("members-container-open");
    });

    openerAbsent.addEventListener('click', () => {
        const container = openerAbsent.parentNode;
        const membersContainer = openerAbsent.parentNode.querySelector(".members-container");

        container.classList.toggle("open");
        container.classList.toggle("closed");
        membersContainer.classList.toggle("members-container-closed");
        membersContainer.classList.toggle("members-container-open");
    });

    const markAll = document.querySelectorAll(".mark-all .mark-attendance");
    const unmarked_attendance_listings = document.querySelectorAll("#unmarked .attendance-listing");

    for (const markAllButton of markAll) {
        markAllButton.addEventListener('click', () => {
            for (const attendance_listing of unmarked_attendance_listings) {
                const id = attendance_listing.id;
                const action = markAllButton.classList.contains("mark-present-all") ? "present" : "absent";

                if (attendance_listing.classList.contains(action)) {
                    continue;
                }

                markAttendance(id, action, attendance_listing);
            }
        })
    }
});