document.addEventListener('DOMContentLoaded', () => {
  const openModalBtn = document.getElementById('openModalBtn');
  const deleteModal = document.getElementById('deleteModal');
  const cancelBtns = document.querySelectorAll('#cancelModalBtn, #cancelModalBtnBottom');
  const confirmBtn = document.getElementById('confirm-button');

  function openModal() {
    deleteModal.classList.remove('opacity-0', 'pointer-events-none');
    deleteModal.classList.add('opacity-100');
    deleteModal.querySelector('div').classList.remove('scale-95');
    deleteModal.querySelector('div').classList.add('scale-100');
  }

  function closeModal() {
    deleteModal.classList.add('opacity-0', 'pointer-events-none');
    deleteModal.classList.remove('opacity-100');
    deleteModal.querySelector('div').classList.add('scale-95');
    deleteModal.querySelector('div').classList.remove('scale-100');
  }

  if (openModalBtn) openModalBtn.addEventListener('click', openModal);
  cancelBtns.forEach(btn => btn.addEventListener('click', closeModal));

  if (deleteModal) {
    deleteModal.addEventListener('click', e => {
      if (e.target === deleteModal) {
        closeModal();
      }
    });
  }

  document.addEventListener('keydown', e => {
    if (e.key === "Escape" && !deleteModal.classList.contains('pointer-events-none')) {
      closeModal();
    }
  });

  if (confirmBtn) {
    confirmBtn.addEventListener('click', function (e) {
      confirmBtn.textContent = 'Carregando...';
      confirmBtn.style.pointerEvents = 'none';
      confirmBtn.style.opacity = '0.7';
    });
  }
});
