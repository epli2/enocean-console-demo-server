# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
from pymongo import MongoClient
import json
import mqtt
import audio
import douglasPeucker

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/history/<string:paramname>/<int:length>', defaults={'tolerance': 0}, methods=['GET'])
@app.route('/api/history/<string:paramname>/<int:length>/<float:tolerance>', methods=['GET'])
@app.route('/api/history/<string:paramname>/<int:length>/<int:tolerance>', methods=['GET'])
def history(paramname, length, tolerance):
    if paramname == 'temperature':
        topic = 'sensor/04016897/Temperature'
    elif paramname == 'humidity':
        topic = 'sensor/04016897/Humidity'
    elif paramname == 'illumination':
        topic = 'sensor/04016777/Illumination'
    elif paramname == 'audio':
        topic = 'audio'
    else:
        return jsonify({})

    data = []
    for i in co.find({'topic': topic}).sort('timestamp', -1).limit(length):
        data.append({'value': i['value'], 'timestamp': i['timestamp'], 'topic': i['topic'], 'ret': i['ret']})
    return jsonify({'data': douglasPeucker.simplifyPath(data, tolerance)})

@socketio.on('connect', namespace='/api/socket')
def test_connect():
    print('connected from client')

if __name__ == '__main__':
    configfile = open('./config.json', 'r')
    config = json.load(configfile)
    client = MongoClient(config['mongo']['ip'], config['mongo']['port'])
    db = client.sensordb
    co = db.sensordata
    mqtt.start(socketio)
    audio.start(socketio)
    socketio.run(app, host='0.0.0.0', debug=True)
