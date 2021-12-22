from umqtt.robust import MQTTClient 
from machine import Pin, PWM
import network
import time

# 蜂鳴器 (15 代表 D1 mini 的 D8 腳位)
#buzzer = Pin(15,Pin.OUT,value = 0)
buzzer = PWM(Pin(15))

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

TOPIC = client.user.encode() + b'/feeds/alarm'          # 訂閱主題

# 連線至 MQTT 伺服器         
client.connect()           
print('MQTT連線成功')

# 從 MQTT 伺服器獲得資料
def get_cmd(topic,msg):
    print(msg)
    # 如果接收到的資訊為 nodoff, 發出警報聲
    if(msg == b"nodoff"):
        buzzer.duty(512)
        print("alarm on")
    else:
        buzzer.duty(0)
        print("alarm off")

client.set_callback(get_cmd)
client.subscribe(TOPIC)

def alarm():
    # 頻率從 100 遞增至 1500 後再遞減
    for i in range(100,1500):
        buzzer.freq(i)
        time.sleep_ms(1)
    # range 第 3 個參數需要設定 -1 表示遞減
    for i in range(1500,100,-1):
        buzzer.freq(i)
        time.sleep_ms(1)

while True:
    # 與伺服端通訊, 確保不會斷線
    client.ping()
    # 確定是否有新資料
    client.check_msg()
    alarm()

