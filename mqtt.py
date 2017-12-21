# -*- coding: utf-8 -*-
import banpei
import threading
import json
import paho.mqtt.client as mqtt
from pymongo import MongoClient
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def on_connect(mqttc, obj, flags, rc):
    print('rc: '+str(rc))

def on_message(mqttc, obj, msg):
    payload = json.loads(msg.payload.decode('utf-8'))
    payload['topic'] = msg.topic
    if payload['topic'] == 'sensor/04016777/Illumination':
        data_illum.append(payload['value'])
        payload['ret'] = model_illum.stream_detect(data_illum)
    elif payload['topic'] == 'sensor/04016897/Humidity':
        data_humid.append(payload['value'])
        payload['ret'] = model_humid.stream_detect(data_humid)
    elif payload['topic'] == 'sensor/04016897/Temperature':
        data_temp.append(payload['value'])
        payload['ret'] = model_temp.stream_detect(data_temp)
    co.insert_one(payload)
    socketio.emit('data', JSONEncoder().encode(payload), namespace='/api/socket')
    print(msg.topic+' '+str(msg.qos)+' '+str(msg.payload))

def on_publish(mqttc, obj, mid):
    print('mid: '+str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print('Subscribed: '+str(mid)+' '+str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)

def mqtt_connect():
    mqttc = mqtt.Client(transport='websockets')
    headers = {
        'Sec-WebSocket-Version': '13',
        'Sec-WebSocket-Protocol': 'mqtt'
    }
    mqttc.ws_set_options(path='/mqtt', headers=headers)
    mqttc.username_pw_set('james-kitchen', password='webdino')
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    # mqttc.on_publish = on_publish
    # mqttc.on_subscribe = on_subscribe

    mqttc.connect('192.168.212.21', 8080)

    mqttc.subscribe('sensor/#', 0)

    mqttc.loop_forever()

def start(_socketio):
    global co
    global socketio
    global model_illum
    global model_humid
    global model_temp
    global data_illum
    global data_humid
    global data_temp
    socketio = _socketio
    model_illum = banpei.SST(w=30)
    model_humid = banpei.SST(w=30)
    model_temp = banpei.SST(w=30)
    data_illum = []
    data_humid = []
    data_temp = []

    # setup mongodb connection
    client = MongoClient('localhost', 27017)
    db = client.sensordb
    co = db.sensordata

    for i in co.find({'topic': 'sensor/04016777/Illumination'}).sort('timestamp').limit(1):
        data_illum.insert(0, i['value'])
        print(i['value'])

    for i in co.find({'topic': 'sensor/04016897/Humidity'}).sort('timestamp').limit(1):
        data_humid.insert(0, i['value'])
        print(i['value'])

    for i in co.find({'topic': 'sensor/04016897/Temperature'}).sort('timestamp').limit(1):
        data_temp.insert(0, i['value'])
        print(i['value'])

    # setup mqtt connection
    th = threading.Thread(target=mqtt_connect, name='th', args=())
    th.setDaemon(True)
    th.start()
