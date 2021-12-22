from machine import Pin, PWM
import time

# 蜂鳴器 (15 代表 D1 mini 的 D8 腳位)
buzzer = PWM(Pin(15))
buzzer.duty(512)

# 頻率從 100 遞增至 1500 後再遞減
for i in range(100,1500):
    buzzer.freq(i)
    time.sleep_ms(1)
# range 第 3 個參數需要設定 -1 表示遞減
for i in range(1500,100,-1):
    buzzer.freq(i)
    time.sleep_ms(1)
    
# 關閉蜂鳴器
buzzer.duty(0)
