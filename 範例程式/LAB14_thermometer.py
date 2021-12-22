from machine import Pin,ADC
import time
import network
from time import sleep_ms
from umqtt.robust import MQTTClient

# 連線到無線網路
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('FlagPub', '')

adc = ADC(0)                 # 設定 A0 為輸入腳位
print('init:',adc.read())    # 先顯示一次, 確認數值是否正常

# 循環測試網路直到網路連線成功
while not sta_if.isconnected():  
    pass
print("控制板已連線")

# 建立 MQTT 客戶端物件
client = MQTTClient(client_id='',                  # 用戶端識別名稱
                    server='io.adafruit.com',      # 中介伺服器網址
                    user='FM634A',               # AIO 帳戶名稱
                    password='aio_PkST29GERTdduZk5uzTmYy4JQ4xU')          # AIO 金鑰

Topic = client.user.encode() + b'/feeds/thermal'  # 訂閱主題

# 連線至 MQTT 伺服器
client.connect()          
print('MQTT連線成功')

passTime = time.time()        # 經過時間
data=0                        # 資料總和
newData = 0
while True:
    # 與伺服端通訊, 確保不會斷線
    client.ping()
    # ping() 需搭配 check_msg(), 不然無法接收回應
    client.check_msg()
    
    for i in range(20):       # 重複20次      
        thermal=adc.read()    # ADC值
        data=data+thermal     # 加總至data
        time.sleep(0.01)
        
    data=int(data/20)         # 取平均

    #如果新的值超過舊值 1 以上
    if abs(data - newData) > 1:                
        newData = data
        # 距離上次發送超過 2 秒以上就發佈到 MQTT 伺服器
        if time.time() - passTime > 2 :
            client.publish(Topic, str(data))
            print ('send:',data)
            passTime = time.time()
            
    data=0   # 總和歸0