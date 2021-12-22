from machine import Pin
import time

# 振動馬達(12 代表 D1 mini 的 D6 腳位)
vMotor = Pin(12,Pin.OUT,value = 0)

while True:
    vMotor.value(1)
    time.sleep(0.5)
    vMotor.value(0)
    time.sleep(0.5)