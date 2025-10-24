$(document).ready(function() {
  function updateControllers() {
    const params = window.location.search;
    $.ajax({
      url: `/controllers/status/${params}`,
      type: "GET",
      dataType: "json",
      success: function(response) {
        if (!response.controllers) return;

        response.controllers.forEach(controller => {
          const card = $(`[data-controller-id="${controller.id}"]`);
          if (!card.length) return;

          const statusEl = card.find(".controller-status");
          if (controller.status) {
            statusEl.text("Online")
              .removeClass("bg-gray-400")
              .addClass("bg-green-600");
          } else {
            statusEl.text("Offline")
              .removeClass("bg-green-600")
              .addClass("bg-gray-400");
          }

          const phaseIcon = card.find(".controller-phase-icon");
          const phaseText = card.find(".controller-phase-text");

          let icon = "sprout";
          let color = "text-green-600";
          let phaseLabel = "(Desconhecida)";
          switch (controller.phaseVegetable) {
            case 1: icon = "sprout"; color = "text-green-600"; phaseLabel = 'Fase Inicial'; break;
            case 2: icon = "leaf"; color = "text-green-600"; phaseLabel = 'Fase Vegetativa'; break;
            case 3: icon = "flower"; color = "text-pink-500"; phaseLabel = 'Fase de Floração'; break;
            case 4: icon = "apple"; color = "text-red-500"; phaseLabel = 'Fase de Frutificação'; break;
            case 5: icon = "package"; color = "text-yellow-600"; phaseLabel = 'Fase de Maturação'; break;
          }

          phaseIcon.attr("data-lucide", icon)
                   .attr("class", `controller-phase-icon w-5 h-5 mr-2 ${color}`);
          phaseText.text(`(${phaseLabel})`);

          controller.valves.forEach(valve => {
            const valveEl = card.find(`[data-valve-id="${valve.id}"]`);
            if (!valveEl.length) return;

            const valveIcon = valveEl.find("[data-lucide='droplet']");
            const valveStatus = valveEl.find(".valve-status-text");

            if (valve.status) {
              valveIcon.removeClass("text-red-600").addClass("text-blue-600");
              valveStatus.text("Irrigando")
                         .removeClass("text-red-600")
                         .addClass("text-green-600");
            } else {
              valveIcon.removeClass("text-blue-600").addClass("text-red-600");
              valveStatus.text("Desativada")
                         .removeClass("text-green-600")
                         .addClass("text-red-600");
            }
          });
        });

        lucide.createIcons();
      },
      error: function(xhr, status, error) {
        console.error("Erro ao atualizar controladores:", error);
      }
    });
  }

  updateControllers();
  setInterval(updateControllers, 1000);
});
