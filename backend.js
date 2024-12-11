function sendMessage() {
    const chatBody = document.getElementById('chatBody');
    const userInput = document.getElementById('userInput');
    
    const userMessage = userInput.value;
    if (userMessage.trim() !== "") {
        // Add user message
        const userMessageElement = document.createElement('div');
        userMessageElement.classList.add('message', 'user');
        userMessageElement.textContent = userMessage;
        chatBody.appendChild(userMessageElement);
        
        // Clear input field
        userInput.value = '';
        
        // Send user message to the Flask backend
        fetch('/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            const botMessageElement = document.createElement('div');
            botMessageElement.classList.add('message', 'bot');
            botMessageElement.textContent = data.response || "Sorry, I didn't get that.";
            chatBody.appendChild(botMessageElement);
            
            // Scroll to the bottom of the chat
            chatBody.scrollTop = chatBody.scrollHeight;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}
