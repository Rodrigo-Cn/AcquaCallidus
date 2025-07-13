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

    $("#geolocation-select").select2({
    placeholder: "Selecione uma cidade",
    allowClear: true,
    });

    $("#geolocation-form").on("submit", function (e) {
    e.preventDefault();
    const selectedGeolocationId = $("#geolocation-select").val();

    if (selectedGeolocationId) {
        document.getElementById('geolocation-select').value = selectedGeolocationId;
        document.getElementById('geolocation-form').submit();
    } else {
        openModal("Por favor, selecione uma cidade.");
    }
    });
});