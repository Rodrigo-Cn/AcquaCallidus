let GeolocationIdToDelete = null;

function openDeleteGeolocationModal(id) {
  GeolocationIdToDelete = id;
  const modal = document.getElementById("deleteGeolocationModal");
  const modalContent = modal.querySelector(".bg-white");

  modal.classList.remove("hidden", "opacity-0");
  modal.classList.add("opacity-100");
  modalContent.classList.add("scale-100");
  modalContent.classList.remove("scale-95");
}

function closeDeleteGeolocationModal() {
  const modal = document.getElementById("deleteGeolocationModal");
  const modalContent = modal.querySelector(".bg-white");

  modal.classList.remove("opacity-100");
  modal.classList.add("opacity-0");
  modalContent.classList.remove("scale-100");
  modalContent.classList.add("scale-95");

  setTimeout(() => {
    modal.classList.add("hidden");
    GeolocationIdToDelete = null;
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
  document.getElementById("cancelGeolocationModalBtnTop").addEventListener("click", closeDeleteGeolocationModal);
  document.getElementById("cancelGeolocationModalBtnBottom").addEventListener("click", closeDeleteGeolocationModal);

  document.getElementById("deleteGeolocationModal").addEventListener("click", (e) => {
    if (e.target.id === "deleteGeolocationModal") {
      closeDeleteGeolocationModal();
    }
  });

  document.getElementById("confirmDeleteGeolocationBtn").addEventListener("click", () => {
    if (!GeolocationIdToDelete) return;

    const form = document.createElement('form');
    form.method = 'POST';
    form.action = `/geolocations/${GeolocationIdToDelete}/delete/`;

    const csrfToken = getCookie('csrftoken');
    const csrfInput = document.createElement('input');
    csrfInput.type = 'hidden';
    csrfInput.name = 'csrfmiddlewaretoken';
    csrfInput.value = csrfToken;
    form.appendChild(csrfInput);

    document.body.appendChild(form);
    form.submit();
    closeDeleteGeolocationModal();
  });
});
