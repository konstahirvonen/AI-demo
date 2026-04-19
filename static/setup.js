async function sendToAI() {
        const inputField = document.getElementById("userInput");
        const message = inputField.value;

        if (!message.trim()) return;

        inputField.value = "";
        inputField.style.height = "auto";

        appendMessage("user", message)

        const loader = document.createElement("div");
        loader.id = "loader";
        loader.innerHTML = '<span class="loader"></span>';
        document.getElementById("chatHistory").appendChild(loader);

        const response = await fetch("/ask", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message: message})
        });

        const data = await response.json();
        
        loader.remove();
        appendMessage("assistant", data.answer);
    }


    const userInput = document.getElementById("userInput");

    userInput.addEventListener("keydown", function(event) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            sendToAI();
            }
        }
    )

function appendMessage(role, content) {
    const historyEl = document.getElementById("chatHistory");
    const div = document.createElement("div");
    div.className = `message ${role}`;
    div.innerHTML = `<strong style="font-weight: bold;">${role === "user" ? "You" : "AI"}:</strong> <span>${content}</span>`;
    historyEl.appendChild(div);
    historyEl.scrollTop = historyEl.scrollHeight;
}