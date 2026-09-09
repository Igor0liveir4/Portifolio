document.addEventListener("DOMContentLoaded", () => {
    const contactForm = document.getElementById("contact-form");
    const feedbackMsg = document.getElementById("form-feedback");
    const btnSubmit = document.getElementById("btn-submit");

    if (contactForm) {
        contactForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            btnSubmit.disabled = true;
            btnSubmit.innerText = "Enviando...";

            const formData = {
                name: document.getElementById("name").value,
                email: document.getElementById("email").value,
                subject: document.getElementById("subject").value,
                message: document.getElementById("message").value
            };

            try {
                const response = await fetch("/api/contact/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(formData)
                });

                if (response.ok) {
                    feedbackMsg.style.color = "#10B981"; // Verde
                    feedbackMsg.innerText = "Mensagem enviada com sucesso! Em breve entrarei em contato.";
                    contactForm.reset();
                } else {
                    const errorData = await response.json();
                    feedbackMsg.style.color = "#EF4444"; // Vermelho
                    feedbackMsg.innerText = "Erro ao enviar mensagem: " + (errorData.detail || "Tente novamente.");
                }
            } catch (error) {
                feedbackMsg.style.color = "#EF4444";
                feedbackMsg.innerText = "Erro de conexão com o servidor. Tente novamente mais tarde.";
            } finally {
                btnSubmit.disabled = false;
                btnSubmit.innerText = "Enviar Mensagem";
            }
        });
    }
});