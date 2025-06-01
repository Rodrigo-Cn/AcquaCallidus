var userMenuDiv = document.getElementById("userMenu");
var userMenu = document.getElementById("userButton");
var navMenuDiv = document.getElementById("nav-content");
var navMenu = document.getElementById("nav-toggle");

document.onclick = check;

function check(e) {
    var target = (e && e.target) || (event && event.srcElement);

    if (!checkParent(target, userMenuDiv)) {
        if (checkParent(target, userMenu)) {
            if (userMenuDiv.classList.contains("invisible")) {
                userMenuDiv.classList.remove("invisible");
            } else { userMenuDiv.classList.add("invisible"); }
        } else {
            userMenuDiv.classList.add("invisible");
        }
    }

    if (!checkParent(target, navMenuDiv)) {
        if (checkParent(target, navMenu)) {
            if (navMenuDiv.classList.contains("hidden")) {
                navMenuDiv.classList.remove("hidden");
            } else { navMenuDiv.classList.add("hidden"); }
        } else {
            navMenuDiv.classList.add("hidden");
        }
    }

}

function checkParent(t, elm) {
    while (t.parentNode) {
        if (t == elm) { return true; }
        t = t.parentNode;
    }
    return false;
}