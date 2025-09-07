function openDeviceCodeController(button) {
  const code = button.getAttribute("data-code");
  const codeBlock = document.querySelector("#codeControllerContent code");

  codeBlock.textContent = code;
  hljs.highlightElement(codeBlock);

  document.getElementById("codeControllerModal").classList.remove("hidden");
}

document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("codeControllerModal");
  const closeBtn = document.getElementById("closeCodeControllerModal");
  const copyBtn = document.getElementById("copyCodeBtn");

  closeBtn.addEventListener("click", () => {
    modal.classList.add("hidden");
  });

  modal.addEventListener("click", (e) => {
    if (e.target.id === "codeControllerModal") {
      modal.classList.add("hidden");
    }
  });

  copyBtn.addEventListener("click", () => {
    const code = document.querySelector("#codeControllerContent code").textContent;
    navigator.clipboard.writeText(code).then(() => {
      const originalIcon = copyBtn.innerHTML;
      copyBtn.innerHTML = "✅";
      setTimeout(() => {
        copyBtn.innerHTML = originalIcon;
      }, 3000);
    });
  });
});
