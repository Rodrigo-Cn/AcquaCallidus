let irrigationIdToDelete = null;

window.openDeleteIrrigationModal = function(id) {
  irrigationIdToDelete = id;
  const modal = document.getElementById("deleteIrrigationModal");
  if (modal) modal.classList.remove("hidden");
};

window.closeDeleteIrrigationModal = function() {
  irrigationIdToDelete = null;
  const modal = document.getElementById("deleteIrrigationModal");
  if (modal) modal.classList.add("hidden");
};

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document.addEventListener('DOMContentLoaded', () => {
  const cancelTop = document.getElementById("cancelIrrigationModalBtnTop");
  if (cancelTop) cancelTop.addEventListener("click", closeDeleteIrrigationModal);

  const cancelBottom = document.getElementById("cancelIrrigationModalBtnBottom");
  if (cancelBottom) cancelBottom.addEventListener("click", closeDeleteIrrigationModal);

  const modal = document.getElementById("deleteIrrigationModal");
  if (modal) {
    modal.addEventListener("click", (e) => {
      if (e.target.id === "deleteIrrigationModal") {
        closeDeleteIrrigationModal();
      }
    });
  }

  const confirmBtn = document.getElementById("confirmDeleteIrrigationBtn");
  if (confirmBtn) {
    confirmBtn.addEventListener("click", () => {
      if (!irrigationIdToDelete) return;

      const urlParams = new URLSearchParams(window.location.search);
      const dateQuery = urlParams.get('date') || '';
      const pageNumber = urlParams.get('page') || 1;

      let actionUrl = `/controllers/irrigationscontroller/${irrigationIdToDelete}/delete/`;
      const queryParams = [];
      if (dateQuery) queryParams.push(`date=${encodeURIComponent(dateQuery)}`);
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

      closeDeleteIrrigationModal();
    });
  }
});
