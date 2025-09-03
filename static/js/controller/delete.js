let controllerIdToDelete = null;

function openDeleteControllerModal(id) {
  controllerIdToDelete = id;
  const modal = document.getElementById("deleteControllerModal");
  const modalContent = modal.querySelector(".bg-white");

  modal.classList.remove("hidden", "opacity-0");
  modal.classList.add("opacity-100");
  modalContent.classList.add("scale-100");
  modalContent.classList.remove("scale-95");
}

function closeDeleteControllerModal() {
  const modal = document.getElementById("deleteControllerModal");
  const modalContent = modal.querySelector(".bg-white");

  modal.classList.remove("opacity-100");
  modal.classList.add("opacity-0");
  modalContent.classList.remove("scale-100");
  modalContent.classList.add("scale-95");

  setTimeout(() => {
    modal.classList.add("hidden");
    controllerIdToDelete = null;
  }, 200);
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById("cancelControllerModalBtnTop").addEventListener("click", closeDeleteControllerModal);
  document.getElementById("cancelControllerModalBtnBottom").addEventListener("click", closeDeleteControllerModal);

  document.getElementById("deleteControllerModal").addEventListener("click", (e) => {
    if (e.target.id === "deleteControllerModal") {
      closeDeleteControllerModal();
    }
  });

  document.getElementById("confirmDeleteControllerBtn").addEventListener("click", () => {
    if (!controllerIdToDelete) return;

    const urlParams = new URLSearchParams(window.location.search);
    const nameQuery = urlParams.get('name') || '';
    const pageNumber = urlParams.get('page') || 1;

    let actionUrl = `/controllers/${controllerIdToDelete}/delete/`;
    const queryParams = [];
    if (nameQuery) queryParams.push(`name_page=${encodeURIComponent(nameQuery)}`);
    if (pageNumber) queryParams.push(`page=${encodeURIComponent(pageNumber)}`);
    if (queryParams.length > 0) actionUrl += `?${queryParams.join('&')}`;

    const form = document.createElement('form');
    form.method = 'POST';
    form.action = actionUrl;

    const csrfToken = getCookie('csrftoken');
    const csrfInput = document.createElement('input');
    csrfInput.type = 'hidden';
    csrfInput.name = 'csrfmiddlewaretoken';
    csrfInput.value = csrfToken;
    form.appendChild(csrfInput);

    document.body.appendChild(form);
    form.submit();
    closeDeleteControllerModal();
  });
});
