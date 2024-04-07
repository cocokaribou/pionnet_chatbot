chatMessages = document.getElementById('chat-messages');
userInput = document.getElementById('user-input');
sendButton = document.getElementById('send-button');

// 채팅에 메세지 추가하는 함수
function addMessage(message, className) {
    const li = document.createElement('li');
    li.textContent = message;
    li.classList.add('message', className);
    chatMessages.appendChild(li);
    chatMessages.scrollTop = chatMessages.scrollHeight; // 아래로 스크롤다운
}

// 로딩 메세지를 지우고 챗봇의 답변으로 업데이트하는 함수
function modifyMessage(message) {
    if (chatMessages.lastChild.textContent == "⏳...") {
        chatMessages.lastChild.textContent = message;
    } else {
        addMessage(message, 'bot-message');
    }
}

// 챗봇 api 호출부
async function sendMessage() {
    const userMessage = userInput.value.trim();
    if (userMessage !== '') {
        addMessage(userMessage, 'user-message');
        userInput.value = ''; // 입력칸 비우기

        addMessage("⏳...", 'bot-message'); // 챗봇 응답이 돌아올 때까지 디폴트 로딩 메세지

        // 유저의 질문을 chatbot api의 query parameter로 전송
        try {
            const response = await fetch(`http://localhost:8000/chatbot?query=${encodeURIComponent(userMessage)}`);
            const data = await response.json();
            const botMessage = data;
            modifyMessage(botMessage)
        } catch (error) {
            console.error('Error sending/receiving message:', error);
        }
    }
}

sendButton.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});