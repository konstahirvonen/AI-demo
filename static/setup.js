async function sendToAI() {
        const message = document.getElementById("userInput").value;
        const resField = document.getElementById("response");

        const inputField = document.getElementById("userInput");

        if (!message.trim()) return;

        inputField.value = "";
        inputField.style.height = "auto";

        resField.innerHTML = '<span class="loader"></span>';
        const response = await fetch("/ask", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message: message})
        });

        const data = await response.json();
        resField.innerText = data.answer;
    }

    const tx = document.getElementById("userInput");

    tx.addEventListener("input", function() {
        this.style.height = "auto";
        this.style.height = (this.scrollHeight) + "px";
    });

    const userInput = document.getElementById("userInput");

    userInput.addEventListener("keydown", function(event) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            sendToAI();
            }
        }
    )