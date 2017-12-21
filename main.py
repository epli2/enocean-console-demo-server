# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_socketio import SocketIO

import mqtt
import audio

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/api/socket')
def test_connect():
    print('connected from client')

if __name__ == '__main__':
    mqtt.start(socketio)
    audio.start(socketio)
    socketio.run(app, host='0.0.0.0', debug=True)
