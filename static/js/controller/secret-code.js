document.addEventListener("DOMContentLoaded", function () {
    lucide.createIcons();

    window.toggleSecret = function (button) {
        const card = button.closest(".bg-white");
        const secretSpan = card.querySelector(".secret-code");
        const eyeIcon = button.querySelector("i");

        if (secretSpan.innerText === "****************") {
            secretSpan.innerText = secretSpan.getAttribute("data-code");
            eyeIcon.setAttribute("data-lucide", "eye-off");
        } else {
            secretSpan.innerText = "****************";
            eyeIcon.setAttribute("data-lucide", "eye");
        }

        lucide.createIcons();
    };
});
