from servo import Servo
from machine import Pin
import time

# 建立伺服馬達物件 D7 腳位
my_servo = Servo(Pin(13))
while True:
    my_servo.write_angle(0)
    time.sleep(0.5)
    my_servo.write_angle(90)
    time.sleep(0.5)
