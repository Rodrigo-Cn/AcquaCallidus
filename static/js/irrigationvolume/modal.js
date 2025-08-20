function prepareModal() {
  const geolocationSelect = document.getElementById('geolocation-select');
  const geolocationId = geolocationSelect.value;
  const cultureInput = document.getElementById('culture-id');
  const cultureId = cultureInput.value;

  if (!geolocationId) {
    openModal("Por favor, selecione uma cidade.");
    return;
  }

  const confirmButton = document.getElementById('confirm-button');
  confirmButton.href = `/irrigationvolumes/create/${geolocationId}/${cultureId}/`;

  showModal();
}

function showModal() {
  document.getElementById('generate-modal').classList.remove('hidden');
}

function hideModal() {
  document.getElementById('generate-modal').classList.add('hidden');
}

function openModal(message) {
  const modalMessage = $("#modal-message");
  const modal = $("#alert-modal");
  modalMessage.text(message);
  modal.removeClass("hidden");
}

function addConfirmButtonSpinner() {
  const confirmButton = document.getElementById('confirm-button');

  if (!confirmButton) return;

  confirmButton.addEventListener("click", function () {
  confirmButton.innerHTML = `
    <span class="flex items-center justify-center">
      <svg class="animate-spin h-5 w-5 text-white mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
      </svg>
      Carregando...
    </span>
  `;
    confirmButton.classList.add("opacity-70", "pointer-events-none");
  });
}

document.addEventListener("DOMContentLoaded", addConfirmButtonSpinner);

