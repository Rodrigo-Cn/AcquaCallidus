let mapInitialized = false;
let marker;
let map;

function openModalGeolocation() {
  const modal = document.getElementById("modal");
  modal.classList.remove("hidden");
  modal.classList.add("flex");

  setTimeout(() => {
    if (!mapInitialized) {
      map = L.map('map').setView([-14.2350, -51.9253], 4);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap'
      }).addTo(map);

      map.on('click', function (e) {
        const { lat, lng } = e.latlng;
        document.getElementById('latitude').value = lat.toFixed(6);
        document.getElementById('longitude').value = lng.toFixed(6);

        if (marker) {
          map.removeLayer(marker);
        }
        marker = L.marker([lat, lng]).addTo(map);
      });

      mapInitialized = true;
      setTimeout(() => map.invalidateSize(), 100);
    }
  }, 200);
}

function closeModalGeolocation() {
  const modal = document.getElementById("modal");
  modal.classList.remove("flex");
  modal.classList.add("hidden");
}

function showNotification(message, type = 'success') {
  const notification = document.getElementById('notification');
  notification.textContent = message;
  notification.className = 'fixed top-5 right-5 p-4 rounded shadow-lg text-white transition-opacity duration-300 z-[99999] pointer-events-none';

  if (type === 'success') {
    notification.classList.add('bg-green-600');
  } else if (type === 'error') {
    notification.classList.add('bg-red-600');
  } else {
    notification.classList.add('bg-gray-600');
  }

  notification.classList.remove('hidden');
  setTimeout(() => {
    notification.classList.add('hidden');
  }, 3000);
}

async function geocodeCityState(city, state) {
  const citySpinner = document.getElementById('cityLoadingSpinner');
  const stateSpinner = document.getElementById('stateLoadingSpinner');
  citySpinner.classList.remove('hidden');
  stateSpinner.classList.remove('hidden');

  try {
    const query = `${city}, ${state}, Brasil`;
    const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}`);
    const data = await response.json();

    if (data && data.length > 0) {
      const { lat, lon } = data[0];
      map.setView([lat, lon], 12);

      if (marker) {
        map.removeLayer(marker);
      }
      marker = L.marker([lat, lon]).addTo(map);

      document.getElementById('latitude').value = parseFloat(lat).toFixed(6);
      document.getElementById('longitude').value = parseFloat(lon).toFixed(6);
    } else {
      showNotification('Localização não encontrada.', 'error');
    }
  } catch (error) {
    showNotification('Erro ao buscar localização.', 'error');
  } finally {
    citySpinner.classList.add('hidden');
    stateSpinner.classList.add('hidden');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const cityInput = document.getElementById('city');
  const stateInput = document.getElementById('state');

  const handleKey = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();

      const city = cityInput.value.trim();
      const state = stateInput.value.trim();

      cityInput.classList.remove('border-red-500');
      stateInput.classList.remove('border-red-500');

      if (!city || !state) {
        if (!city) cityInput.classList.add('border-red-500');
        if (!state) stateInput.classList.add('border-red-500');

        showNotification('Preencha cidade e estado.', 'error');

        return;
      }

      geocodeCityState(city, state);
    }
  };

  cityInput.addEventListener('keydown', handleKey);
  stateInput.addEventListener('keydown', handleKey);

  cityInput.addEventListener('input', () => cityInput.classList.remove('border-red-500'));
  stateInput.addEventListener('input', () => stateInput.classList.remove('border-red-500'));
});

function handleSubmit(event) {
  event.preventDefault();

  const city = document.getElementById('city').value.trim();
  const state = document.getElementById('state').value.trim();
  const lat = document.getElementById('latitude').value.trim();
  const lng = document.getElementById('longitude').value.trim();

  if (!city || city.length < 2) {
    showNotification('Informe uma cidade válida (mínimo 2 caracteres).', 'error');
    document.getElementById('city').focus();
    return;
  }

  if (!state || state.length < 2) {
    showNotification('Informe um estado válido (mínimo 2 caracteres).', 'error');
    document.getElementById('state').focus();
    return;
  }

  if (!lat || !lng) {
    showNotification('Selecione sua localização no mapa.', 'error');
    return;
  }

  const latitude = parseFloat(lat);
  const longitude = parseFloat(lng);

  if (isNaN(latitude) || latitude < -90 || latitude > 90) {
    showNotification('Latitude inválida. Deve estar entre -90 e 90.', 'error');
    return;
  }

  if (isNaN(longitude) || longitude < -180 || longitude > 180) {
    showNotification('Longitude inválida. Deve estar entre -180 e 180.', 'error');
    return;
  }

  const submitBtn = document.getElementById('submitBtn');
  const submitLoadingSpinner = document.getElementById('submitLoadingSpinner');
  const btnText = document.getElementById('btnText');

  submitLoadingSpinner.classList.remove('hidden');
  btnText.textContent = 'Salvando...';
  submitBtn.disabled = true;

  setTimeout(() => {
    document.getElementById('locationForm').submit();
  }, 500);
}
