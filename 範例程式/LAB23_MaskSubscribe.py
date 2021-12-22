from umqtt.robust import MQTTClient # mqtt函式庫
from servo import Servo
from machine import Pin
import network
import time

# 建立伺服馬達物件
my_servo = Servo(Pin(13))

# 連線至無線網路
sta=network.WLAN(network.STA_IF)
sta.active(True)   
sta.connect('FlagPub','')  
while not sta.isconnected() :
    pass
print('Wi-Fi連線成功')
# MQTT 參數
client = MQTTClient(client_id='',                  # 用戶端識別名稱
                    server='io.adafruit.com',      # 中介伺服器網址
                    user='FM634A',               # AIO 帳戶名稱
                    password='aio_PkST29GERTdduZk5uzTmYy4JQ4xU')            # AIO 金鑰

TOPIC = client.user.encode() + b'/feeds/mask'          # 訂閱主題

# 將伺服馬達轉至上鎖位置
my_servo.write_angle(0)

# 連線至 MQTT 伺服器          
client.connect()          
print('MQTT連線成功')

# 從 MQTT 伺服器獲得資料
def get_cmd(topic,msg):
    print(msg)
    if(msg == b"mask"):
        my_servo.write_angle(90)
        time.sleep(3)
        my_servo.write_angle(0)
    
client.set_callback(get_cmd)
client.subscribe(TOPIC)

while True:
    # 與伺服端通訊, 確保不會斷線
    client.ping()
    # 確定是否有新資料
    client.check_msg()