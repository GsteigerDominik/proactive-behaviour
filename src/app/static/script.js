const chatContainer = document.getElementById('chat');
const chatList = document.getElementById('chatList');
const messageInput = document.getElementById('messageInput');

let chatsById = {}; // full messages per chat_id
let chatPreviews = [];
let currentChat = null;

async function loadChatPreviews() {
    try {
        const response = await fetch('/chats');
        const data = await response.json();
        chatPreviews = data;

        renderChatList();
        clearChat(); // No chat selected by default
    } catch (error) {
        console.error("Error loading chat previews:", error);
    }
}

function renderChatList() {
    chatList.innerHTML = '';
    const latestByChatId = {};

    chatPreviews.forEach(entry => {
        const existing = latestByChatId[entry.chat_id];
        if (!existing || new Date(entry.timestamp) > new Date(existing.timestamp)) {
            latestByChatId[entry.chat_id] = entry;
        }
    });

    Object.values(latestByChatId).forEach(chat => {
        const div = document.createElement('div');
        div.className = `chat-preview ${chat.chat_id === currentChat ? 'active' : ''}`;
        div.innerHTML = `<strong>${chat.chat_id}</strong><br><small>${chat.message.slice(0, 40)}</small>`;
        div.onclick = () => {
            currentChat = chat.chat_id;
            loadFullChat(chat.chat_id);
            renderChatList();
        };
        chatList.appendChild(div);
    });
}

async function loadFullChat(chatId) {
    try {
        const response = await fetch(`/chats/${chatId}`);
        const data = await response.json();
        const fullChat = data;

        chatsById[chatId] = fullChat.map(entry => ({
            sender: entry.is_user ? "user" : "bot",
            message: entry.message,
            timestamp: entry.timestamp
        }));

        renderMessages();
    } catch (error) {
        console.error("Error loading full chat:", error);
    }
}

function renderMessages() {
    chatContainer.innerHTML = '';
    const messages = chatsById[currentChat] || [];
    messages.forEach(entry => {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${entry.sender}`;
        msgDiv.innerHTML = `
      <div class="text">${entry.message}</div>
      <div class="timestamp">${formatTimestamp(entry.timestamp)}</div>
    `;
        chatContainer.appendChild(msgDiv);
    });
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function formatTimestamp(ts) {
    const date = new Date(ts);
    return date.toLocaleString(); // You can customize this if needed
}

function clearChat() {
    chatContainer.innerHTML = `<div style="color: #999; text-align: center; margin-top: 50px;">Select a chat to get started</div>`;
}

function sendMessage() {
    const text = messageInput.value.trim();
    if (!text || !currentChat) return;

    const msgObj = {
        sender: "user",
        message: text,
        timestamp: new Date().toISOString()
    };

    chatsById[currentChat] = chatsById[currentChat] || [];
    chatsById[currentChat].push(msgObj);
    messageInput.value = '';
    renderMessages();
    renderChatList();

    fetch('/send-msg', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({chat_id: currentChat, msg: text})
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else if (data.empty) {
                alert('DATA EMPTY');
            } else {
                const msgObj = {
                    sender: "bot",
                    message: data.response,
                    timestamp: new Date().toISOString()
                };
                chatsById[currentChat] = chatsById[currentChat] || [];
                chatsById[currentChat].push(msgObj);
                renderMessages();
                renderChatList();
            }
        })
        .catch(error => console.error('Error:', error));
}

// On load
loadChatPreviews();
