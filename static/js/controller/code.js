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
  const downloadBtn = document.getElementById("downloadCodeBtn"); // botão novo

  closeBtn.addEventListener("click", () => {
    modal.classList.add("hidden");
  });

  modal.addEventListener("click", (e) => {
    if (e.target.id === "codeControllerModal") {
      modal.classList.add("hidden");
    }
  });

  function copyToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    } else {
      const textArea = document.createElement("textarea");
      textArea.value = text;
      textArea.style.position = "fixed"; 
      textArea.style.opacity = "0";
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();
      document.execCommand("copy");
      document.body.removeChild(textArea);
      return Promise.resolve();
    }
  }

  copyBtn.addEventListener("click", () => {
    const code = document.querySelector("#codeControllerContent code").textContent;

    copyToClipboard(code).then(() => {
      const originalIcon = copyBtn.innerHTML;
      copyBtn.innerHTML = "✅ Copiado!";
      setTimeout(() => {
        copyBtn.innerHTML = originalIcon;
      }, 2000);
    });
  });

  downloadBtn.addEventListener("click", () => {
    const code = document.querySelector("#codeControllerContent code").textContent;
    const blob = new Blob([code], { type: "text/plain" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "controller_code.c";
    document.body.appendChild(a);
    a.click();

    setTimeout(() => {
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }, 0);
  });
});
