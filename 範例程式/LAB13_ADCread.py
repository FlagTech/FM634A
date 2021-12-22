from machine import ADC
import time

adc = ADC(0)   # 設定 A0 輸入腳位

while True:
        print(adc.read())   
        time.sleep(0.5)