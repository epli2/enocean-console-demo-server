# -*- coding: utf-8 -*-
import pyaudio
import banpei
import audioop
import threading
import datetime
import json
from pymongo import MongoClient

def getstream():
    while True:
        stream = p.open(format=pyaudio.paInt16,
                        channels=config_audio['CHANNELS'],
                        rate=config_audio['RATE'],
                        input=True,
                        input_device_index=config_audio['INDEX'],
                        frames_per_buffer=config_audio['FRAMES_PER_BUFFER'])
        for i in range(0, int(config_audio['RATE'] / config_audio['FRAMES_PER_BUFFER'] * config_audio['RECORD_SECONDS'])):
            data = stream.read(config_audio['FRAMES_PER_BUFFER'], exception_on_overflow=False)
            rms = audioop.rms(data, 2)
        rmsArray.append(rms)
        print(rms)
        data = {'value': rms,
                'timestamp': str(datetime.datetime.utcnow().isoformat()) + 'Z',
                'topic': 'audio',
                'ret': model.stream_detect(rmsArray)}
        socketio.emit('audio', json.JSONEncoder().encode(data), namespace='/api/socket')
        co.insert_one(data)

def start(_socketio):
    global socketio
    global p
    global stream
    global model
    global rmsArray

    configfile = open('./config.json', 'r')
    config = json.load(configfile)
    global config_audio
    config_audio = config['audio']
    
    # setup mongodb connection
    global co
    client = MongoClient(config['mongo']['ip'], config['mongo']['port'])
    db = client.sensordb
    co = db.sensordata

    socketio = _socketio
    p = pyaudio.PyAudio()
    model = banpei.SST(w=30)
    rmsArray = []
    th = threading.Thread(target=getstream, name='th', args=())
    th.setDaemon(True)
    th.start()
