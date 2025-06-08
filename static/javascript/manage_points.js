var selectedMembers = [];

document.addEventListener("DOMContentLoaded", () => {
    const allMembers = document.querySelectorAll(".member-listing-container");
    var membersShown = document.querySelectorAll(".member-listing-container.visible");
    const checkAll = document.querySelector("#check-all-members");
    const searchBar = document.querySelector("#search-members");
    const options = document.querySelector("#options-all");

    options.addEventListener('click', () => {
        if (!(selectedMembers.length == 0)) {
            params = selectedMembers.join("+");
            document.location.href = '/p/edit_points/'+params;
        }
    });

    // add checkbox event for each individual member
    for (const member of membersShown) {
        const check = member.querySelector(".checkbox")

        check.addEventListener("change", () => {
            const id = parseInt(member.id.split("-")[2]);

            if (check.checked) {
                selectedMembers.push(id);

                if (selectedMembers.length >= membersShown.length) {
                    checkAll.checked = true;
                }
            }
            else if (selectedMembers.includes(id)) {
                selectedMembers.splice(selectedMembers.indexOf(id), 1);
                checkAll.checked = false;
            }
        });
    }

    // event listener on check all
    checkAll.addEventListener("change", () => {
        membersShown = document.querySelectorAll(".member-listing-container.visible");
        for (const member of membersShown) {
            const id = parseInt(member.id.split("-")[2]);
            const check = member.querySelector(".checkbox")

            if (checkAll.checked) {
                if (!selectedMembers.includes(id)) {
                    selectedMembers.push(id);
                }
                check.checked = true;
            }
            else {
                if (selectedMembers.includes(id)) {
                    selectedMembers.splice(selectedMembers.indexOf(id), 1);
                }
                check.checked = false;
            }
        }
    });

    searchBar.addEventListener("input", (e) => {
        const val = e.target.value.toLowerCase();
        var allTrue = true;

        for (const member of allMembers) {
            const nameLower = member.querySelector(".members-list-item-name").innerHTML.toLowerCase();

            if (nameLower.indexOf(val) == -1) {
                member.classList.remove("visible");
                member.classList.add("hidden");
            }
            else {
                member.classList.add("visible");
                member.classList.remove("hidden");

                const check = member.querySelector(".checkbox");

                if (check.checked == false) {
                    checkAll.checked = false;
                    allTrue = false;
                }
            }
        }

        if (allTrue) {
            checkAll.checked = true;
        }
    });
});