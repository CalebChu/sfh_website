function tabChange(tab, oldTab, tabItemsC, oldTabItemsC, emptyIndicator) {
    if (!tab.classList.contains("tab-inactive")) {
        return;
    }

    const queuedChanges = document.querySelectorAll(".queued-tab-change");

    for (const change of queuedChanges) {
        change.classList.toggle("tab-l-item");
        change.classList.toggle("tab-r-item");
        change.classList.remove("queued-tab-change");
    }
    
    tab.classList.remove("tab-inactive");
    oldTab.classList.add("tab-inactive");

    hide(oldTabItemsC);
    show(tabItemsC);

    if (is_empty(tabItemsC)) {
        emptyIndicator.style.display = "flex";
    }
    else {
        emptyIndicator.style.display = "none";
    }

    document.cookie = `last-tab-open-v=${tab.id}`;
}

function show(cls) {
    const items = document.querySelectorAll(cls);

    for (const item of items) {
        item.style.display = "";
    }
}

function hide(cls) {
    const items = document.querySelectorAll(cls);

    for (const item of items) {
        item.style.display = "none";
    }
}

function is_empty(cls) {
    var items = document.querySelectorAll(cls);

    return (items.length == 0 || (items.length == 1 && items[0].classList.contains("empty-indicator")));
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

document.addEventListener("DOMContentLoaded", () => {
    var cookieIdentifier = "v";

    // if 

    var lastTabOpen = getCookie(`last-tab-open-${cookieIdentifier}`);

    if (!lastTabOpen) {
        lastTabOpen = "l"; 
    }

    const lastTabClosed = lastTabOpen == "l" ? "r" : "l";

    const activeItems = `.tab-${lastTabOpen}-item`;
    const inactiveItems = `.tab-${lastTabClosed}-item`;

    const active = document.getElementById(lastTabOpen);
    const inactive = document.getElementById(lastTabClosed);

    const emptyIndicator = document.querySelector(".empty-indicator");

    inactive.classList.add("tab-inactive");
    active.classList.remove("tab-inactive");

    hide(inactiveItems);

    if (is_empty(activeItems)) {
        emptyIndicator.style.display = "flex";
    }

    const tabL = document.getElementById("l");
    const tabR = document.getElementById("r");

    const tabLItems = ".tab-l-item";
    const tabRItems = ".tab-r-item";

    tabL.addEventListener("click", () => {
        tabChange(tabL, tabR, tabLItems, tabRItems, emptyIndicator);
    });

    tabR.addEventListener("click", () => {
        tabChange(tabR, tabL, tabRItems, tabLItems, emptyIndicator);
    });
});