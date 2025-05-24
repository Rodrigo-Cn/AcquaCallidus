setTimeout(() => {
    const toast = document.getElementById('toast');
    if (toast) {
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 300);
    }
}, 5000);