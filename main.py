# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_socketio import SocketIO
from pymongo import MongoClient

import mqtt
import audio

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/history/<paramname>/<int:length>', methods=['GET'])
def history(paramname, length):
    if paramname == 'temperature':
        topic = 'sensor/04016897/Temperature'
    elif paramname == 'humidity':
        topic = 'sensor/04016897/Humidity'
    elif paramname == 'illumination':
        topic = 'sensor/04016777/Illumination'
    else:
        return '{ }'

    data = []
    for i in co.find({'topic': topic}).sort('timestamp', -1).limit(length):
        data.append('{"value":%s,"timestamp":"%s","ret":"%s"}' % (i['value'], i['timestamp'], i['ret']))
    return '{"data":[%s]}' % ','.join(data)

@socketio.on('connect', namespace='/api/socket')
def test_connect():
    print('connected from client')

if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    db = client.sensordb
    co = db.sensordata
    mqtt.start(socketio)
    audio.start(socketio)
    socketio.run(app, host='0.0.0.0', debug=True)
