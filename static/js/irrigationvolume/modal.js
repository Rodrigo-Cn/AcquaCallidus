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


