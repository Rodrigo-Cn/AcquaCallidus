document.addEventListener("DOMContentLoaded", () => {
  const openBtn = document.getElementById("openWifiModal");
  const modal = document.getElementById("wifiModal");
  const closeBtn = document.getElementById("closeWifiModal");
  const form = document.getElementById("wifiForm");

  const passwordWrapper = document.getElementById("passwordWrapper");
  const passwordInput = document.getElementById("password");
  const togglePasswordBtn = document.getElementById("togglePassword");
  const eyeOpen = document.getElementById("eyeOpen");
  const eyeClosed = document.getElementById("eyeClosed");
  const openNetworkCheckbox = document.getElementById("openNetwork");

  openBtn.addEventListener("click", () => modal.classList.remove("hidden"));

  closeBtn.addEventListener("click", () => modal.classList.add("hidden"));
  modal.addEventListener("click", (e) => { 
    if (e.target === modal) modal.classList.add("hidden"); 
  });

  togglePasswordBtn.addEventListener("click", (e) => {
    e.preventDefault(); 
    const type = passwordInput.type === "password" ? "text" : "password";
    passwordInput.type = type;
    eyeOpen.classList.toggle("hidden", type === "text");
    eyeClosed.classList.toggle("hidden", type !== "text");
  });


  openNetworkCheckbox.addEventListener("change", (e) => {
    if (e.target.checked) {
      passwordInput.value = "";
      passwordInput.disabled = true;
      togglePasswordBtn.classList.add("opacity-50", "pointer-events-none");
    } else {
      passwordInput.disabled = false;
      togglePasswordBtn.classList.remove("opacity-50", "pointer-events-none");
    }
  });

  form.addEventListener("submit", () => {
    modal.classList.add("hidden");
  });
});