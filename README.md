# enocean-console-demo-server
https://github.com/epli2/enocean-console-demo 用のサーバです  

## 使用方法
### 共通
#### インストール
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

#### 設定
- [こちら](https://github.com/epli2/enocean-console-demo)のREADMEを参考に, `templates/`以下に`index.html`を, `static/`以下に`js/`と`css/`をコピーしてください
`config.json`の`audio.INDEX`の値を使用するマイクのインデックスに変えてください  
マイクのインデックスの取得方法  
```python
> import pyaudio
> p = pyaudio.PyAudio()
> for i in range(p.get_device_count()):p.get_device_info_by_index(i)
```

### Macのみの場合
#### 準備
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

7. mongodbをインストールする
`brew install mongodb`  
`brew services start mongodb`

#### 起動
1. webship2017の`kitchen/mqtt-enocean/`のディレクトリで`node index.js`
2. mosquitto起動 `/usr/local/sbin/mosquitto -c /usr/local/etc/mosquitto/mosquitto.conf`
3. `config.json`の`mqtt_server`と`mongo`の`ip`をどちらも`localhost`にする
4. このサーバを起動(ポート5000番で起動する) `python3 main.py`

### Raspberry piで動作するmqttブローカーと通信する場合
1. Raspberry piにmqtt-enoceanとmosquittoをインストールする
2. USBドングルをRaspberry piに挿す
3. `config.json`の`mqtt_server.ip`の値をRaspberry piのものにする
4. 適宜`mqtt_server.username`と`mqtt_server.password`を設定する
5. このサーバを起動(ポート5000番で起動する) `python3 main.py`
6. うまく動作しない場合は`mqtt_server.header`を`true`にする

### Raspberry piのみの場合
Raspberry piではマイクによる音量の取得は現状動作しない
1. USBドングルをRaspberry piに挿す
2. Raspberry piにmqtt-enocean, mosquitto, mongodbをインストールし, 起動する
3. `config.json`の`mqtt_server`と`mongo`の`ip`をどちらも`localhost`にする
4. このサーバを起動(ポート5000番で起動する) `python3 main.py`