document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('favorite-map-container');

  if (container.dataset.lat && container.dataset.lon) {
    const lat = parseFloat(container.dataset.lat);
    const lon = parseFloat(container.dataset.lon);

    container.innerHTML = "";

    const map = L.map(container, { zoomControl: false, attributionControl: false }).setView([lat, lon], 1);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: ''
    }).addTo(map);

    const smallIcon = L.icon({
      iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
      iconSize: [16, 24],
      iconAnchor: [8, 24] 
    });

    L.marker([lat, lon], { icon: smallIcon }).addTo(map);

    setTimeout(() => map.invalidateSize(), 100);
  }
});