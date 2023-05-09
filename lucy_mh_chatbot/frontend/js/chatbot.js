// Set up websocket
var socket = new WebSocket(`ws://${window.location.host}/chat`);

// Define function to send message
function sendMessage(event) {
  event.preventDefault();
  var messageInputDom = document.getElementById('messageInput');
  var message = messageInputDom.value;
  messageInputDom.value = '';
  socket.send(JSON.stringify({
    'message': message
  }));
}

// Define function to append message to chat log
function appendMessage(data) {
  var messageLogDom = document.getElementById('messageLog');
  var messageBody = document.createElement('div');
  messageBody.className = 'message-body';
  messageBody.innerText = data.message;
  messageLogDom.appendChild(messageBody);
}

// Set up event listeners
document.getElementById('messageForm').addEventListener('submit', sendMessage);

socket.addEventListener('message', function(event) {
  var data = JSON.parse(event.data);
  appendMessage(data);
});
