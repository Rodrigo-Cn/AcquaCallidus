let cultureIdToDelete = null;

function openDeleteCultureModal(id) {
  cultureIdToDelete = id;
  const modal = document.getElementById("deleteCultureModal");
  const modalContent = modal.querySelector(".bg-white");

  modal.classList.remove("hidden", "opacity-0");
  modal.classList.add("opacity-100");
  modalContent.classList.add("scale-100");
  modalContent.classList.remove("scale-95");
}

function closeDeleteCultureModal() {
  const modal = document.getElementById("deleteCultureModal");
  const modalContent = modal.querySelector(".bg-white");

  modal.classList.remove("opacity-100");
  modal.classList.add("opacity-0");
  modalContent.classList.remove("scale-100");
  modalContent.classList.add("scale-95");

  setTimeout(() => {
    modal.classList.add("hidden");
    cultureIdToDelete = null;
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
  document.getElementById("cancelCultureModalBtnTop").addEventListener("click", closeDeleteCultureModal);
  document.getElementById("cancelCultureModalBtnBottom").addEventListener("click", closeDeleteCultureModal);

  document.getElementById("deleteCultureModal").addEventListener("click", (e) => {
    if (e.target.id === "deleteCultureModal") {
      closeDeleteCultureModal();
    }
  });

  document.getElementById("confirmDeleteCultureBtn").addEventListener("click", () => {
    if (!cultureIdToDelete) return;

    const form = document.createElement('form');
    form.method = 'POST';
    form.action = `/culturesvegetables/${cultureIdToDelete}/delete/`;

    const csrfToken = getCookie('csrftoken');
    const csrfInput = document.createElement('input');
    csrfInput.type = 'hidden';
    csrfInput.name = 'csrfmiddlewaretoken';
    csrfInput.value = csrfToken;
    form.appendChild(csrfInput);

    document.body.appendChild(form);
    form.submit();
    closeDeleteCultureModal();
  });
});
