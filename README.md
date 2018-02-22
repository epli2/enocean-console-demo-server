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


## Macで動かす手順
### 準備
1. USBドングルをMacに挿す
2. webship2017のrepositoryをクローンする
3. `kitchen/mqtt-enocean/`のディレクトリで`npm install`
4. `kitchen/mqtt-enocean/config/development.js`を編集, USBドングルのデバイスファイルのパスを書き込む
```javascript
module.exports = {
  portName: "/dev/cu.usbserial-FTSCWGP", // 例
```

5. mosquittoをインストールする `brew install mosquitto`
6. mosquittoの設定ファイルを記述する `vi /usr/local/etc/mosquitto/mosquitto.conf`
```
listener 1883
protocol mqtt

listener 8080
protocol websockets

allow_anonymous true

log_type all
websockets_log_level 1023
connection_messages true
```

### 起動
1. webship2017の`kitchen/mqtt-enocean/`のディレクトリで`node index.js`
2. mosquitto起動 `/usr/local/sbin/mosquitto -c /usr/local/etc/mosquitto/mosquitto.conf`
3. このサーバを起動 `python3 main.py`

## 使用方法
### 前提
- EnOceanセンサのMQTT on WebSocketサーバを別途起動する必要があります
- [こちら](https://github.com/epli2/enocean-console-demo)のREADMEを参考に、`templates/`以下に`index.html`を、`static/`以下に`js/`と`css/`をコピーしてください

### 設定
`config.json`の`mqtt_server.ip`の値をEnOceanセンサのMQTTサーバのものに変えてください  
`config.json`の`audio.INDEX`の値を使用するマイクのインデックスに変えてください  
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
