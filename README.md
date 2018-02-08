# enocean-console-demo-server
https://github.com/epli2/enocean-console-demo 用のサーバです  

## 既知のバグ
- マイクによってはうまく動作しない

## インストール
python3, pip3, mongodbのインストール  
`sudo apt-get install -y python3 python3-pip mongodb-server`  
pythonのライブラリをインストール  
`sudo apt-get install -y python3-pyaudio python3-scipy`

pipからpythonライブラリのインストール
```bash
sudo pip3 install flask flask_socketio pymongo paho-mqtt gevent-websocket
git clone https://github.com/tsurubee/banpei.git
cd banpei
sudo pip3 install .
```
https://github.com/tsurubee/banpei のReadmeも参照してください

## 使用方法
### 前提
- EnOceanセンサのMQTT on WebSocketサーバを別途起動する必要があります
- [こちら](https://github.com/epli2/enocean-console-demo)のREADMEを参考に、`templates/`以下に`index.html`を、`static/`以下に`js/`と`css/`をコピーしてください

### 設定
`mqtt.py`の9行目`MQTT_SERVER_IP = `のipアドレスの部分をEnOceanセンサのMQTTサーバのものに変えてください  
`audio.py`の12行目`INDEX = `の値を使用するマイクのインデックスに変えてください  
マイクのインデックスの取得方法  
```python
> import pyaudio
> p = pyaudio.PyAudio()
> for i in range(p.get_device_count()):p.get_device_info_by_index(i)
```

### サーバ起動
`python3 main.py`  
ログを出力したくないときは
`python3 main.py &> /dev/null`

### アクセス
http://localhost:5000/
