from machine import Pin
import network     
from umqtt.robust import MQTTClient # mqtt函式庫
import time

# 按鈕(14 代表 D1 mini 的 D5 腳位)
button=Pin(14,Pin.IN,Pin.PULL_UP)

# 連線至無線網路
sta=network.WLAN(network.STA_IF)
sta.active(True)   
sta.connect('無線網路名稱', '無線網路密碼')  
while not sta.isconnected() :
    pass
print('Wi-Fi連線成功')

client = MQTTClient(client_id='',                  # 用戶端識別名稱
                    server='io.adafruit.com',      # 中介伺服器網址
                    user='AIO_USER',               # AIO 帳戶名稱
                    password='AIO_KEY')            # AIO 金鑰

TOPIC = client.user.encode() + b'/feeds/visitors'  # 訂閱主題

# 連線至 MQTT 伺服器
client.connect()          
print('MQTT連線成功')

count = 0

while True:
    # 與伺服端通訊, 確保不會斷線
    client.ping()
    # ping() 需搭配 check_msg(), 不然無法接收回應
    client.check_msg()
    
    # 目前按鈕狀態
    now_status = button.value()
    print(now_status)
    time.sleep(0.1)
    # 如果按下按鈕
    if(now_status == 0):
        count += 1                # 次數 +1
        # 傳送資料到 MQTT 伺服器
        client.publish(                   
            TOPIC,
            str(count).encode()    # 傳送的資料改為 bytes 物件
        )               
        print('完成上傳。請稍等才能繼續上傳資料!')
        time.sleep(2)
        print('可以繼續上傳資料')