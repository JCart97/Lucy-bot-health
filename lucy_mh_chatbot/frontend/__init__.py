from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO, emit
from ..db.database import get_db_connection
from . import chatbot
import logging.config
import os

# Load logging configuration
logging.config.fileConfig(os.path.join(os.path.dirname(__file__), '..', 'logging.ini'))

app = Flask(__name__, static_folder="../static", template_folder="../templates")
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev")

socketio = SocketIO(app, cors_allowed_origins='*')

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            'SELECT id, username, password FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        if user:
            login_user(chatbot.User(user[0], user[1]))
            return redirect(url_for('chat'))
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')


@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html', current_user=current_user)


@socketio.on('my_event')
def handle_my_custom_event(json):
    emit('my_response', json, broadcast=True)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(user_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    if not user:
        return None
    return chatbot.User(user[0], user[1])


if __name__ == '__main__':
    socketio.run(app)