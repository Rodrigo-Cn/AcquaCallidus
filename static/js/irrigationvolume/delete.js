function openDeleteModal(id) {
  const modal = document.getElementById(`deleteModal-${id}`);
  if (modal) {
    modal.classList.remove("opacity-0", "pointer-events-none");
    modal.querySelector("div").classList.remove("scale-95");
    modal.querySelector("div").classList.add("scale-100");
  }
}

function closeDeleteModal(id) {
  const modal = document.getElementById(`deleteModal-${id}`);
  if (modal) {
    modal.classList.add("opacity-0", "pointer-events-none");
    modal.querySelector("div").classList.add("scale-95");
    modal.querySelector("div").classList.remove("scale-100");
  }
}
