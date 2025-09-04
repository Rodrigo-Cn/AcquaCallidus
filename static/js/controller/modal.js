document.addEventListener("DOMContentLoaded", function () {
    const popup = document.getElementById("popupControlador");
    const valveContainer = document.getElementById("popup-valve-container");
    const addValveBtn = document.getElementById("popup-add-valve");

    let valveCount = 0;
    const maxValves = 3;
    let isEditMode = false;

    function resetForm() {
        isEditMode = false;
        $("#formController").attr("action", "/controllers/store/");
        $("#nomeControlador").val("");
        $("#dispositivoControlador").val("");
        $("#ipControlador").val("");
        $("#faseControlador").val("");
        $("#statusControlador").prop("checked", true);
        $("#irrigacaoControlador").val(new Date().toISOString().split("T")[0]);
        $("#culturaControlador").val(null).trigger("change");
        $("#geoControlador").val(null).trigger("change");

        valveContainer.innerHTML = "";
        valveCount = 0;
        createValveField();

        addValveBtn.style.display = "flex";
    }

    $("#openPopupController").on("click", () => {
        resetForm();
        popup.classList.remove("hidden");
    });

    $("#closePopupController, #fecharFundoControlador").on("click", () => {
        popup.classList.add("hidden");
        resetForm();
    });

    function initSelect2(selector) {
        if ($(selector).length) {
            $(selector).select2({
                placeholder: $(selector).data("placeholder"),
                allowClear: true,
                width: "100%"
            }).on("select2:open", function () {
                document
                    .querySelector(".select2-search__field")
                    .setAttribute("placeholder", "Buscar...");
            });
        }
    }
    initSelect2("#culturaControlador");
    initSelect2("#geoControlador");

    function toggleAddButtonController() {
        if (isEditMode) {
            addValveBtn.style.display = "none";
        } else {
            addValveBtn.style.display =
                valveCount >= maxValves ? "none" : "flex";
        }
    }

    function updateDeleteButtonsController() {
        const allValves = valveContainer.querySelectorAll(".valve-field");

        if (isEditMode) {
            allValves.forEach((v) => {
                const btn = v.querySelector(".remove-valve");
                if (btn) btn.remove();
            });
            return;
        }

        allValves.forEach((v) => {
            const btn = v.querySelector(".remove-valve");
            if (btn) btn.remove();
        });

        if (allValves.length > 1) {
            allValves.forEach((v) => {
                const deleteBtn = document.createElement("button");
                deleteBtn.type = "button";
                deleteBtn.className =
                    "remove-valve bg-red-500 text-white w-10 h-10 rounded-full hover:bg-red-600 flex items-center justify-center";
                deleteBtn.innerHTML = "×";
                v.appendChild(deleteBtn);

                deleteBtn.addEventListener("click", () => {
                    v.remove();
                    valveCount--;
                    toggleAddButtonController();
                    updateDeleteButtonsController();
                });
            });
        }
    }

    function createValveField(valve = null) {
        valveCount++;
        const div = document.createElement("div");
        div.className = "valve-field flex flex-col sm:flex-row gap-2";

        div.innerHTML = `
            <input type="hidden" name="valves[${valveCount}][id]" value="${
            valve?.id || ""
        }"/>
            <input type="number" name="valves[${valveCount}][plants]" placeholder="Qtd. Plantas" value="${
            valve?.plants_number || ""
        }" required
            class="w-full sm:w-1/2 rounded-lg border-gray-300 shadow-sm focus:border-sky-500 focus:ring focus:ring-sky-200 p-3"/>
            <input type="number" step="0.1" name="valves[${valveCount}][radius]" placeholder="Raio de Irrigação (m²)" value="${
            valve?.irrigation_radius || ""
        }" required
            class="w-full sm:w-1/2 rounded-lg border-gray-300 shadow-sm focus:border-sky-500 focus:ring focus:ring-sky-200 p-3"/>
        `;

        valveContainer.appendChild(div);
        toggleAddButtonController();
        updateDeleteButtonsController();
    }

    addValveBtn.addEventListener("click", () => {
        if (!isEditMode && valveCount < maxValves) {
            createValveField();
        }
    });

    resetForm();

    window.editController = function (id) {
        isEditMode = true;
        fetch(`/controllers/${id}/`)
            .then((res) => res.json())
            .then((data) => {
                $("#nomeControlador").val(data.name);
                $("#dispositivoControlador").val(data.device);
                $("#ipControlador").val(data.ip_address);
                $("#faseControlador").val(data.phase_vegetable);
                $("#statusControlador").prop("checked", data.active);
                $(
                    "#irrigacaoControlador"
                ).val(data.last_irrigation || new Date().toISOString().split("T")[0]);
                $("#culturaControlador").val(data.culturevegetable).trigger("change");
                $("#geoControlador").val(data.geolocation).trigger("change");

                $("#formController").attr("action", `/controllers/${id}/update/`);

                valveContainer.innerHTML = "";
                valveCount = 0;

                if (data.valves && data.valves.length) {
                    data.valves.forEach((v) => createValveField(v));
                } else {
                    createValveField();
                }

                addValveBtn.style.display = "none";
                updateDeleteButtonsController();
                popup.classList.remove("hidden");
            });
    };
});
