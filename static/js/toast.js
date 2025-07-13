document.addEventListener('DOMContentLoaded', () => {
    const toasts = document.querySelectorAll('#toast > div');
    toasts.forEach(toast => {
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 5000);
    });
});
