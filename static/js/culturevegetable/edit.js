let editCultureModal;

document.addEventListener("DOMContentLoaded", () => {
  editCultureModal = new Modal(document.getElementById('edit-culture-modal'));
  
  document.querySelector('[data-modal-hide="edit-culture-modal"]').addEventListener("click", () => {
    editCultureModal.hide();
  });
});

function openEditCultureModal(id) {
  fetch(`/culturesvegetables/${id}/`)
    .then(response => {
      if (!response.ok) throw new Error("Erro ao carregar dados.");
      return response.json();
    })
    .then(data => {
      const form = document.getElementById("edit-culture-form");
      form.action = `/culturesvegetables/${id}/update/`;

      document.querySelector("#name_edit").value = data.name || "";
      document.querySelector("#phase_initial_kc_edit").value = data.phase_initial_kc || "";
      document.querySelector("#phase_vegetative_kc_edit").value = data.phase_vegetative_kc || "";
      document.querySelector("#phase_flowering_kc_edit").value = data.phase_flowering_kc || "";
      document.querySelector("#phase_fruiting_kc_edit").value = data.phase_fruiting_kc || "";
      document.querySelector("#phase_maturation_kc_edit").value = data.phase_maturation_kc || "";

      editCultureModal.show();
    })
    .catch(error => {
      console.error(error);
      alert("Erro ao carregar cultura vegetal para edição.");
    });
}