from machine import Pin
import time

# 按鈕(14 代表 D1 mini 的 D5 腳位)
button=Pin(14,Pin.IN,Pin.PULL_UP)       

while True:
    # 讀取按鈕的值
    print(button.value())
    time.sleep(0.1)