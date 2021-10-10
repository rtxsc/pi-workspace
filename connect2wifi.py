import board
import digitalio
import busio as io
import subprocess
import socket
import adafruit_ssd1306

from time import sleep

buzz = digitalio.DigitalInOut(board.D26)
buzz.direction = digitalio.Direction.OUTPUT

i2c = io.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
from digitalio import DigitalInOut

reset_pin = DigitalInOut(board.D21) # any pin!
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)

oled.fill(1)
oled.show()
sleep(0.5)
buzz.value = True
sleep(0.05)
buzz.value = False

oled.fill(0)
for i in range(32,96):
    oled.pixel(i, 0, 1)
    oled.pixel(i, 1, 1)
    oled.show()
oled.fill(0)
oled.text('Hello from Pi3B+', 0, 0, True)
oled.show()
sleep(1)

try:
    print("checking for SSID")
    output = subprocess.check_output(['iwgetid'])
    print("connected!")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    print("IP Address:{}".format(local_ip))

    oled.fill(0)
    oled.text(local_ip, 0, 0, True)
    oled.text('WiFi Connected', 0, 10, True)
    oled.show()
    out = output.split(b'"')[1]
    out_str = out.decode('UTF-8')
    print(out_str)
    oled.text(out_str, 0, 20, True)
    oled.show()

#     print("Connected Wifi SSID: " + output.split('"')[1])
except Exception as e:
    print("Exception:" , e)
    oled.text('WiFi Not Connected', 0, 10, True)
    oled.show()

