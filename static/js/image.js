document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("profile_photo");
  const fileName = document.getElementById("fileName");

  input.addEventListener("change", () => {
    fileName.textContent = input.files.length > 0 ? input.files[0].name : "";
  });
});
