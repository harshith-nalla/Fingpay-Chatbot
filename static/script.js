const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

const SESSION_ID = "user123";  // you can randomize per user later

sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
});

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    appendMessage(message, "user");
    userInput.value = "";

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message, session_id: SESSION_ID })
        });

        const data = await res.json();
        appendMessage(data.reply, "bot");
    } catch (error) {
        appendMessage("⚠️ Error contacting chatbot.", "bot");
        console.error(error);
    }
}

function appendMessage(text, sender) {
    const msgDiv = document.createElement("div");
    msgDiv.className = `message ${sender}`;
    msgDiv.textContent = text;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}
