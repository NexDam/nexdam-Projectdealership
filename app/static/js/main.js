document.addEventListener("DOMContentLoaded", () => {
    // Auto-dismiss degli alert dopo qualche secondo
    document.querySelectorAll(".alert").forEach((alert) => {
        setTimeout(() => {
            alert.style.transition = "opacity 0.4s";
            alert.style.opacity = "0";
            setTimeout(() => alert.remove(), 400);
        }, 4000);
    });

    // Validazione semplice del form contatti
    const formContatti = document.querySelector(".form-contatti");
    if (formContatti) {
        formContatti.addEventListener("submit", (event) => {
            const requiredFields = formContatti.querySelectorAll("[required]");
            let valido = true;
            requiredFields.forEach((field) => {
                if (!field.value.trim()) {
                    valido = false;
                    field.style.borderColor = "#c0392b";
                } else {
                    field.style.borderColor = "";
                }
            });
            if (!valido) {
                event.preventDefault();
            }
        });
    }
});
