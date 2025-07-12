document.addEventListener("DOMContentLoaded", function () {
    const mapContainers = document.querySelectorAll(".map-instance");
    mapContainers.forEach(container => {
    if (container && !container._leaflet_id) {
        const lat = parseFloat(container.dataset.lat.replace(',', '.'));
        const lon = parseFloat(container.dataset.lon.replace(',', '.'));
        const map = L.map(container.id).setView([lat, lon], 10);

        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19,
        }).addTo(map);

        L.marker([lat, lon]).addTo(map);

        setTimeout(() => {
        map.invalidateSize();
        }, 100);
    }
    });
});