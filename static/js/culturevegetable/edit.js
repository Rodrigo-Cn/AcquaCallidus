let editCultureModal;

document.addEventListener("DOMContentLoaded", () => {

  editCultureModal = new Modal(document.getElementById('edit-culture-modal'));
  
  document.querySelector('[data-modal-hide="edit-culture-modal"]').addEventListener("click", () => {
    editCultureModal.hide();
  });
});

function openEditCultureModal(id) {
  const urlParams = new URLSearchParams(window.location.search);
  const nameQuery = urlParams.get('name') || '';
  const pageNumber = urlParams.get('page') || 1;

  fetch(`/culturesvegetables/${id}/`)
    .then(response => {
      if (!response.ok) throw new Error("Erro ao carregar dados.");
      return response.json();
    })
    .then(data => {
      const form = document.getElementById("edit-culture-form");
      const defaultEmoji = "🌱";

      const queryParams = [];
      if (nameQuery) queryParams.push(`name_page=${encodeURIComponent(nameQuery)}`);
      if (pageNumber) queryParams.push(`page=${encodeURIComponent(pageNumber)}`);
      let actionUrl = `/culturesvegetables/${id}/update/`;
      if (queryParams.length > 0) actionUrl += `?${queryParams.join('&')}`;
      form.action = actionUrl;

      document.querySelector("#name_edit").value = data.name || "";
      document.querySelector("#phase_initial_kc_edit").value = data.phase_initial_kc || "";
      document.querySelector("#phase_vegetative_kc_edit").value = data.phase_vegetative_kc || "";
      document.querySelector("#phase_flowering_kc_edit").value = data.phase_flowering_kc || "";
      document.querySelector("#phase_fruiting_kc_edit").value = data.phase_fruiting_kc || "";
      document.querySelector("#phase_maturation_kc_edit").value = data.phase_maturation_kc || "";
      document.querySelector("#emoji_edit").value = data.emoji || defaultEmoji;
      
      editCultureModal.show();
    })
    .catch(error => {
      alert("Erro ao carregar cultura vegetal para edição.");
    });
}