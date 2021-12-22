from umqtt.robust import MQTTClient 
from machine import Pin
import network
import time

# 振動馬達(12 代表 D1 mini 的 D6 腳位)
shake = Pin(12,Pin.OUT,value = 0)

# 連線至無線網路
sta=network.WLAN(network.STA_IF)
sta.active(True)   
sta.connect('FlagPub','')  
while not sta.isconnected() :
    pass
print('Wi-Fi連線成功')

client = MQTTClient(client_id='',                  # 用戶端識別名稱
                    server='io.adafruit.com',      # 中介伺服器網址
                    user='FM634A',               # AIO 帳戶名稱
                    password='aio_PkST29GERTdduZk5uzTmYy4JQ4xU')            # AIO 金鑰

TOPIC = str.encode(USERNAME) + b'/feeds/game'          # 訂閱主題

# 連線至 MQTT 伺服器         
client.connect()           
print('MQTT連線成功')

# 從 MQTT 伺服器獲得資料
def get_cmd(topic,msg):
    print(msg)
    # 如果接收到的資訊為 person, 開始滾動
    if(msg == b"end"):
        shake.value(1)
        time.sleep(1.5)
        shake.value(0)
        
client.set_callback(get_cmd)
client.subscribe(TOPIC)

while True:
    # 與伺服端通訊, 確保不會斷線
    client.ping()
    # 確定是否有新資料
    client.check_msg()
