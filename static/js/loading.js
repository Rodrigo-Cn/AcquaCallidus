document.addEventListener("DOMContentLoaded", function () {
    const loader = document.getElementById('page-loader');

    setTimeout(() => {
        loader.classList.add('hidden');
    }, 300);
});

window.addEventListener('beforeunload', function () {
    const loader = document.getElementById('page-loader');
    loader.classList.remove('hidden');
});

window.addEventListener("pageshow", function (event) {
    const loader = document.getElementById('page-loader');
    if (event.persisted) {
        loader.classList.add('hidden');
    }
});