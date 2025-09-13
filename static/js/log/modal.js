function logExceptionViewer() {
  return {
    showModal: false,
    isLoading: false,
    exceptionText: '',

    async fetchLogException(logId, event) {
      this.showModal = true;
      this.isLoading = true;
      this.exceptionText = '';

      try {
        const response = await fetch(`/logs/${logId}/`, {
          headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json',
          },
          credentials: 'include',
        });

        if (!response.ok) throw new Error('Erro ao buscar log');

        const data = await response.json();

        this.exceptionText = typeof data.exception === 'string'
          ? data.exception
          : JSON.stringify(data.exception, null, 2);

        const button = event.target.closest('button');
        if (button && button.classList.contains('bg-yellow-100')) {
          button.classList.remove(
            'bg-yellow-100', 'text-yellow-700', 'border-yellow-400', 'hover:bg-yellow-500'
          );
          button.classList.add(
            'bg-green-100', 'text-green-700', 'border-green-400', 'hover:bg-green-500'
          );
        }

      } catch (error) {
        this.exceptionText = 'Erro ao carregar log';
      } finally {
        this.isLoading = false;
      }
    }
  };
}