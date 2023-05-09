import logging
from datetime import datetime

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

from pubsub.publisher import publish_message
from scripts.chatbot import ChatBot

app = Flask(__name__)
socketio = SocketIO(app)

chatbot = ChatBot()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/chat')
def chat():
    return render_template('chat.html')


@socketio.on('connect')
def handle_connect():
    logger.info('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
    logger.info('Client disconnected')


@socketio.on('chat message')
def handle_chat_message(message):
    logger.info(f'Received chat message: {message}')

    response = chatbot.generate_response(message)

    publish_message(response)

    emit('bot message', response)


if __name__ == '__main__':
    socketio.run(app, debug=True)
