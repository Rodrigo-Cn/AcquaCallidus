let editMapInitialized = false;
let editMarker;
let editMap;
let GeolocationIdToEdit = null;

function openEditModal(id) {
  GeolocationIdToEdit = id;
  const modal = document.getElementById("modal-edit");
  const formEdit = document.getElementById("locationForm-edit");
  modal.classList.remove("hidden");
  modal.classList.add("flex");

  modal.addEventListener("click", function (event) {
    if (event.target === modal) {
      closeEditModal();
    }
  }, { once: true });

  const urlParams = new URLSearchParams(window.location.search);
  const nameQuery = urlParams.get("name");
  const pageNumber = urlParams.get('page') || 1;

  let actionUrl = `/geolocations/${id}/update/`;
  const queryParams = [];
  if (nameQuery) queryParams.push(`name_page=${encodeURIComponent(nameQuery)}`);
  if (pageNumber) queryParams.push(`page=${encodeURIComponent(pageNumber)}`);
  if (queryParams.length > 0) actionUrl += `?${queryParams.join('&')}`;
  formEdit.action = actionUrl;

  fetch(`/geolocations/${id}/`)
    .then(response => {
      if (!response.ok) throw new Error("Erro ao carregar dados.");
      return response.json();
    })
    .then(data => {
      document.querySelector("#city-edit").value = data.city || "";
      document.querySelector("#state-edit").value = data.state || "";
      document.querySelector("#latitude-edit").value = data.latitude || "";
      document.querySelector("#longitude-edit").value = data.longitude || "";
      document.querySelector("#property-name").value = data.property_name || "";

      if (!editMapInitialized) {
        editMap = L.map('map-edit').setView(
          [data.latitude || -14.2350, data.longitude || -51.9253],
          data.latitude && data.longitude ? 12 : 4
        );

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: '© OpenStreetMap'
        }).addTo(editMap);

        editMap.on('click', function (e) {
          const { lat, lng } = e.latlng;
          document.getElementById('latitude-edit').value = lat.toFixed(6);
          document.getElementById('longitude-edit').value = lng.toFixed(6);

          if (editMarker) editMap.removeLayer(editMarker);
          editMarker = L.marker([lat, lng]).addTo(editMap);
        });

        editMapInitialized = true;
      }

      editMap.setView([data.latitude || -14.2350, data.longitude || -51.9253], 12);

      if (editMarker) editMap.removeLayer(editMarker);
      if (data.latitude && data.longitude) {
        editMarker = L.marker([data.latitude, data.longitude]).addTo(editMap);
      }

      setTimeout(() => editMap.invalidateSize(), 100);
    })
    .catch(error => {
      console.error(error);
      alert("Erro ao carregar propriedade para edição.");
    });
}

function closeEditModal() {
  const modal = document.getElementById("modal-edit");
  modal.classList.remove("flex");
  modal.classList.add("hidden");
}

async function geocodeCityStateEdit(city, state) {
  const citySpinner = document.getElementById('cityLoadingSpinner-edit');
  const stateSpinner = document.getElementById('stateLoadingSpinner-edit');
  citySpinner.classList.remove('hidden');
  stateSpinner.classList.remove('hidden');

  try {
    const query = `${city}, ${state}, Brasil`;
    const response = await fetch(
      `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}`
    );
    const data = await response.json();

    if (data.length > 0) {
      const { lat, lon } = data[0];
      editMap.setView([lat, lon], 12);

      if (editMarker) editMap.removeLayer(editMarker);
      editMarker = L.marker([lat, lon]).addTo(editMap);

      document.getElementById('latitude-edit').value = parseFloat(lat).toFixed(6);
      document.getElementById('longitude-edit').value = parseFloat(lon).toFixed(6);
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
  const cityInput = document.getElementById('city-edit');
  const stateInput = document.getElementById('state-edit');

  const handleKeyEdit = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();

      const city = cityInput.value.trim();
      const state = stateInput.value.trim();

      if (!city || !state) {
        if (!city) cityInput.classList.add('border-red-500');
        if (!state) stateInput.classList.add('border-red-500');
        showNotification('Preencha cidade e estado.', 'error');
        return;
      }

      geocodeCityStateEdit(city, state);
    }
  };

  cityInput.addEventListener('keydown', handleKeyEdit);
  stateInput.addEventListener('keydown', handleKeyEdit);

  cityInput.addEventListener('input', () => cityInput.classList.remove('border-red-500'));
  stateInput.addEventListener('input', () => stateInput.classList.remove('border-red-500'));
});

function handleSubmitEdit(event) {
  event.preventDefault();

  const city = document.getElementById('city-edit').value.trim();
  const state = document.getElementById('state-edit').value.trim();
  const lat = document.getElementById('latitude-edit').value.trim();
  const lng = document.getElementById('longitude-edit').value.trim();

  if (!city || city.length < 2) {
    showNotification('Informe uma cidade válida.', 'error');
    return;
  }
  if (!state || state.length < 2) {
    showNotification('Informe um estado válido.', 'error');
    return;
  }
  if (!lat || !lng) {
    showNotification('Selecione sua localização no mapa.', 'error');
    return;
  }

  const latitude = parseFloat(lat);
  const longitude = parseFloat(lng);

  if (isNaN(latitude) || latitude < -90 || latitude > 90) {
    showNotification('Latitude inválida.', 'error');
    return;
  }
  if (isNaN(longitude) || longitude < -180 || longitude > 180) {
    showNotification('Longitude inválida.', 'error');
    return;
  }

  const submitBtn = document.getElementById('submitBtn-edit');
  const submitLoadingSpinner = document.getElementById('submitLoadingSpinner-edit');
  const btnText = document.getElementById('btnText-edit');

  submitLoadingSpinner.classList.remove('hidden');
  btnText.textContent = 'Salvando...';
  submitBtn.disabled = true;

  setTimeout(() => {
    document.getElementById('locationForm-edit').submit();
  }, 500);
}
