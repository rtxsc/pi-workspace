#edit 12 Oct
import board
import digitalio
import busio as io
import subprocess
import adafruit_ssd1306
import netifaces
import json
import socket


from time import sleep

buzz = digitalio.DigitalInOut(board.D26)
buzz.direction = digitalio.Direction.OUTPUT

i2c = io.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
from digitalio import DigitalInOut

reset_pin = DigitalInOut(board.D21) # any pin!
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)


# for i in range(0,32):
#     oled.pixel(i, 0, 1)
#     oled.pixel(i, 1, 1)
#     oled.show()
# oled.fill(0)

try:
    oled.fill(1)
    oled.show()
    sleep(0.5)
    oled.fill(0)
    buzz.value = True
    sleep(0.05)
    buzz.value = False
    sleep(0.5)

    buzz.value = True
    sleep(0.05)
    buzz.value = False
    sleep(0.5)

    oled.text('Hello from Pi3B+', 0, 0, True)
    oled.show()
    sleep(0.5)
    print("checking for SSID")
    output = subprocess.check_output(['iwgetid'])

    device = 'wlan0'
    cmd = "ip addr show %s | awk '$1 == \"inet\" {gsub(/\/.*$/, \"\", $2); print $2}'" % device

    p = subprocess.Popen(cmd, shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)
    out, _ = p.communicate()
    local_ip = str(out.strip().decode('UTF-8'))
    print(local_ip)

    device = 'wlan0'
    dict = netifaces.ifaddresses(device)[netifaces.AF_INET]
    print(dict)

    print("connected!")

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

