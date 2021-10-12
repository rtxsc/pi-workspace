#!/usr/bin/env python3

import board
import digitalio
import busio as io
import subprocess
import adafruit_ssd1306
import netifaces
import json
import socket

MAX_CHAR_DISPLAYABLE  = 21

from time import sleep

buzz = digitalio.DigitalInOut(board.D26)
buzz.direction = digitalio.Direction.OUTPUT

i2c = io.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
from digitalio import DigitalInOut

reset_pin = DigitalInOut(board.D21) # any pin!
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)

def run_led():
    led0 = digitalio.DigitalInOut(board.D17)
    led1 = digitalio.DigitalInOut(board.D18)
    led2 = digitalio.DigitalInOut(board.D27)
    led3 = digitalio.DigitalInOut(board.D22)
    led4 = digitalio.DigitalInOut(board.D25)
    led5 = digitalio.DigitalInOut(board.D12)
    led6 = digitalio.DigitalInOut(board.D13)
    led7 = digitalio.DigitalInOut(board.D19)
    leds = [led0,led1,led2,led3,led4,led5,led6,led7]
    for i in leds:
        i.direction = digitalio.Direction.OUTPUT

    for i in leds:
        i.value = True
        sleep(0.1)
    
    for i in leds:
        i.value = False   
        sleep(0.1)

try:

    for i in range(0,32):
        oled.pixel(64, i, 1)
        oled.show()
    oled.fill(0)
    # oled.fill(1)
    # oled.show()
    # sleep(0.5)
    # oled.fill(0)
    run_led()
  
    for i in range (1,2):
        oled.text('Hello from Pi3B+', 0, 0, True)
        # oled.text('123456789ABCDEFGHIJKLMN', 0, 0, True)

        oled.show()
        sleep(0.5)
        print("checking for SSID")

        device = 'wlan0'
        cmd = "ip addr show %s | awk '$1 == \"inet\" {gsub(/\/.*$/, \"\", $2); print $2}'" % device

        p = subprocess.Popen(cmd, shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
        out, _ = p.communicate()
        local_ip = str(out.strip().decode('UTF-8'))
        print(local_ip)

        buzz.value = True
        sleep(0.05)
        buzz.value = False
        sleep(0.1)

        buzz.value = True
        sleep(0.05)
        buzz.value = False
        sleep(0.1)
        # i = 1 / 0 # for deliberate division-by-error occurence 
        # device = 'wlan0'
        # dict = netifaces.ifaddresses(device)[netifaces.AF_INET]
        # print(dict)

        print("connected!")

        oled.fill(0)
        oled.text(local_ip, 0, 0, True)
        oled.text('WiFi Connected', 0, 10, True)
        # oled.text(local_ip, 0, 20, True)
        oled.show()
        
        output = subprocess.check_output(['iwgetid'])
        out = output.split(b'"')[1]
        out_str = out.decode('UTF-8')
        print(out_str)
        oled.text(out_str, 0, 20, True)
        oled.show()
        sleep(1)
        oled.fill(0)

#     print("Connected Wifi SSID: " + output.split('"')[1])
except Exception as e:
    oled.fill(0)
    oled.text(local_ip, 0, 0, True)

    count = 1
    buzz.value = True
    sleep(1)
    buzz.value = False
    sleep(0.5)
    print("Exception:" , e)
    msg = str(e)
    if(len(msg) > MAX_CHAR_DISPLAYABLE):
        oled.text('Exception len:'+str(len(msg)), 0, 10, True)
        for i in range(0,len(msg)):
            if(i < MAX_CHAR_DISPLAYABLE):
                oled.text(msg[0:i], 0, 20, True)
            else:
                oled.fill(0)
                oled.text(local_ip, 0, 0, True)
                oled.text('Exception len:'+str(len(msg)), 0, 10, True)
                lengthOfChar = len(msg[MAX_CHAR_DISPLAYABLE:i])
                if(lengthOfChar == MAX_CHAR_DISPLAYABLE*count):
                    count += 1
                oled.text(msg[MAX_CHAR_DISPLAYABLE*count:i], 0, 20, True)
           
            oled.show()
    else:
        oled.text('Exception len:'+str(len(msg)), 0, 10, True)
        oled.text(msg, 0, 20, True)
        oled.show()


