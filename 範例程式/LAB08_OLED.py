from machine import Pin, I2C
from ssd1306_i2c_flag import SSD1306_I2C_FLAG
import time

# 指定 SCL 在 5 號腳位 (D1), SDA 在 4 號腳位 (D2)
i2c = I2C(scl=Pin(5), sda=Pin(4))

# 指定寬 128 像素, 高 64 像素, 以及要使用的 I2C 物件
oled = SSD1306_I2C_FLAG(128, 64, i2c)

# 分別在 (0,0) (0,16) (0,32) (0,48) 顯示文字
oled.text("Welcome", 0, 0)
oled.text("to", 0, 16)
oled.text("the", 0, 32)
oled.text("Museum", 0, 48)
oled.show()

while True:
    # 向右轉動
    oled.hw_scroll_h()
    time.sleep(4.5)
    # 向左轉動
    oled.hw_scroll_h(False)
    time.sleep(4.5)
    oled.hw_scroll_off()
    time.sleep(1)