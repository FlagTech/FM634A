from umqtt.robust import MQTTClient 
from machine import Pin,PWM,I2C
import network
import time
from ssd1306_i2c_flag import SSD1306_I2C_FLAG

i2c = I2C(scl=Pin(5), sda=Pin(4))
oled = SSD1306_I2C_FLAG(128, 64, i2c)

# 連線至無線網路
sta=network.WLAN(network.STA_IF)
sta.active(True)   
sta.connect('FlagPub', '')
while not sta.isconnected() :
    pass
print('Wi-Fi連線成功')

client = MQTTClient(client_id='',                  # 用戶端識別名稱
                    server='io.adafruit.com',      # 中介伺服器網址
                    user='FM634A',               # AIO 帳戶名稱
                    password='aio_PkST29GERTdduZk5uzTmYy4JQ4xU')            # AIO 金鑰

TOPIC = client.user.encode() + b'/feeds/step'      # 訂閱主題

# 連線至 MQTT 伺服器          
client.connect()           
print('MQTT連線成功')

# 從 MQTT 伺服器獲得資料
def get_cmd(topic,msg):
    print(msg)
    # 如果接收到的資訊為 person, 開始捲動
    if(msg == b"person"):
        oled.hw_scroll_h()
        time.sleep(2.5)
        oled.hw_scroll_h(False)
        time.sleep(2.5)
        oled.hw_scroll_off() # 停止捲動
        time.sleep(0.5)
        
client.set_callback(get_cmd)
client.subscribe(TOPIC)
oled.text("Welcome", 0, 0)
oled.text("to", 0, 16)
oled.text("the", 0, 32)
oled.text("Museum", 0, 48)
oled.show()
oled.hw_scroll_off() # 不捲動
time.sleep(1)

while True:
    # 與伺服端通訊, 確保不會斷線
    client.ping()
    # 確定是否有新資料
    client.check_msg()