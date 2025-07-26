$(document).ready(function () {
    const modal = $("#alert-modal");
    const closeModalBtn = $("#close-modal-btn");
    const okModalBtn = $("#ok-modal-btn");
    const modalMessage = $("#modal-message");

    function openModal(message) {
        modalMessage.text(message);
        modal.removeClass("hidden");
    }

    function closeModal() {
        modal.addClass("hidden");
    }

    closeModalBtn.on("click", closeModal);
    okModalBtn.on("click", closeModal);
    modal.on("click", function (e) {
        if ($(e.target).is(modal)) {
            closeModal();
        }
    });

    $(document).on("keydown", function (e) {
        if (e.key === "Escape" && !modal.hasClass("hidden")) {
            closeModal();
        }
    });

    $("#culture-select").select2({
        placeholder: "Selecione uma cultura",
        allowClear: true,
    });

    $("#culture-form").on("submit", function (e) {
        e.preventDefault();
        const selectedCultureId = $("#culture-select").val();

        if (selectedCultureId) {
            document.getElementById('culture-select').value = selectedCultureId;
            document.getElementById('culture-form').submit();
        } else {
            document.getElementById('culture-form').submit();
        }
    });
});
