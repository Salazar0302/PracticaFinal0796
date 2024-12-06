document.addEventListener("DOMContentLoaded", () => {
    console.log("Selector Uchiha cargada correctamente.");

    const addForm = document.querySelector("form[action='/add']");
    const nameInput = addForm.querySelector("input[name='name']");
    const participantList = document.querySelector("ul");
    const flashMessage = document.createElement("div");

    // Muestra mensajes de error de manera dinámica
    function showFlashMessage(message, type = "error") {
        flashMessage.textContent = message;
        flashMessage.className = `flash-message ${type}`;
        document.body.prepend(flashMessage);

        setTimeout(() => {
            flashMessage.remove();
        }, 3000);
    }

    // Validar entrada de texto para evitar espacios vacíos o nombres repetidos
    addForm.addEventListener("submit", (event) => {
        const name = nameInput.value.trim();
        const existingNames = Array.from(participantList.querySelectorAll("li")).map(
            (li) => li.textContent
        );

        if (!name) {
            event.preventDefault();
            showFlashMessage("El nombre no puede estar vacío.");
            return;
        }

        if (existingNames.includes(name)) {
            event.preventDefault();
            showFlashMessage("Este nombre ya está en la lista.");
            return;
        }
    });

    // Rotación de la ruleta (simulación)
    const spinButton = document.createElement("button");
    spinButton.textContent = "Girar Ruleta";
    spinButton.style.marginTop = "20px";
    participantList.parentElement.appendChild(spinButton);

    spinButton.addEventListener("click", () => {
        const participants = participantList.querySelectorAll("li");

        if (participants.length === 0) {
            showFlashMessage("No hay participantes en la ruleta.");
            return;
        }

        const randomIndex = Math.floor(Math.random() * participants.length);
        const selectedParticipant = participants[randomIndex];

        selectedParticipant.style.backgroundColor = "#ffeb3b"; // Destacar el nombre seleccionado
        showFlashMessage(`¡Ganador: ${selectedParticipant.textContent}!`, "success");

        setTimeout(() => {
            selectedParticipant.remove(); // Eliminar el nombre seleccionado
        }, 2000);
    });

    // Prevenir más de 60 participantes dinámicamente
    addForm.addEventListener("submit", (event) => {
        if (participantList.children.length >= 60) {
            event.preventDefault();
            showFlashMessage("No se pueden agregar más de 60 nombres.");
        }
    });
});
