# -*- coding: utf-8 -*-
import pyaudio
import banpei
import audioop
import threading
import datetime
import json
from pymongo import MongoClient

FRAMES_PER_BUFFER = 4096
CHANNELS = 1
RATE = 48000
INDEX = 0
RECORD_SECONDS = 1

def getstream():
    while True:
        stream = p.open(format=pyaudio.paInt16,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        input_device_index=INDEX,
                        frames_per_buffer=FRAMES_PER_BUFFER)
        for i in range(0, int(RATE / FRAMES_PER_BUFFER * RECORD_SECONDS)):
            data = stream.read(FRAMES_PER_BUFFER, exception_on_overflow = False)
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

    # setup mongodb connection
    global co
    client = MongoClient('localhost', 27017)
    db = client.sensordb
    co = db.sensordata

    socketio = _socketio
    p = pyaudio.PyAudio()
    model = banpei.SST(w=30)
    rmsArray = []
    th = threading.Thread(target=getstream, name='th', args=())
    th.setDaemon(True)
    th.start()
