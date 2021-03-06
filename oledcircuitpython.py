import board
import busio as io
i2c = io.I2C(board.SCL, board.SDA)
import adafruit_ssd1306
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
from digitalio import DigitalInOut

reset_pin = DigitalInOut(board.D21) # any pin!
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)

oled.fill(1)
oled.show()

oled.fill(0)
oled.text('Hello from Pi3B+', 0, 0, True)
oled.show()

import subprocess
from wifi import Cell, Scheme

def wifiscan():
    wifilist = []
    allSSID = Cell.all('wlan0')
    for ssid in allSSID:
        wifilist.append(ssid)
        print(wifilist) # prints all available WIFI SSIDs
    
#    myssid= 'Cell(ssid=vivekHome)' # vivekHome is my wifi name
# 
#    for i in range(len(allSSID )):
#         if str(allSSID [i]) == myssid:
#                 a = i
#                 myssidA = allSSID [a]
#                 print(b)
#                 break
#         else:
#                 print("getout")
# 
#    # Creating Scheme with my SSID.
#    myssid= Scheme.for_cell('wlan0', 'home', myssidA, 'vivek1234') # vive1234 is the password to my wifi myssidA is the wifi name 
# 
#    print(myssid)
#    myssid.save()
#    myssid.activate()



try:
    wifiscan()  
    print("checking for SSID")
    output = subprocess.check_output(['iwgetid'])
    print("connected!")
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

