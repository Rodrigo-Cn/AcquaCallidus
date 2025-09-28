document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("valve-form");
  const valve = document.getElementById("valve");

  if (form && valve) {
    form.addEventListener("submit", function (e) {
      const valveId = valve.value;
      if (valveId) {
        this.action = `/controllers/irrigationscontroller/${valveId}/`;
      } else {
        e.preventDefault();
        alert("Selecione uma válvula!");
      }
    });
  }

  const valveSelect = document.getElementById("valve");

  function updateTextColor() {
    if (valveSelect.value === "") {
      valveSelect.classList.remove("text-gray-700");
      valveSelect.classList.add("text-gray-500");
    } else {
      valveSelect.classList.remove("text-gray-500");
      valveSelect.classList.add("text-gray-700");
    }
  }

  updateTextColor();
  valveSelect.addEventListener("change", updateTextColor);
});
