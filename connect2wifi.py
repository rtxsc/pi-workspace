#!/usr/bin/env python3
import board
import digitalio
import busio as io
import subprocess
import os
import adafruit_ssd1306
import netifaces
import json
import socket
import sys
from datetime import datetime


MAX_CHAR_DISPLAYABLE  = 21
local_ip = "NULL"
copy_ip = "NULL"
ssid_str = "NULL"
from time import sleep
from digitalio import DigitalInOut

DEFINED_PI_ZERO_W = False

def detect_model() -> str:
    global DEFINED_PI_ZERO_W
    with open('/proc/device-tree/model') as f:
        model = f.read()
        if "Raspberry Pi Zero W" in model:
            DEFINED_PI_ZERO_W = True
        return model

detect_model() # check type of Pi

buzz = digitalio.DigitalInOut(board.D26)
buzz.direction = digitalio.Direction.OUTPUT
i2cErrorSignal = digitalio.DigitalInOut(board.D21)
i2cErrorSignal.direction = digitalio.Direction.OUTPUT
# reset_pin = DigitalInOut(board.D21) # any pin!
# reset_pin.direction = digitalio.Direction.INPUT

def run_led_maker_hat_base():
    led0 = digitalio.DigitalInOut(board.D10)
    led1 = digitalio.DigitalInOut(board.D9)
    led2 = digitalio.DigitalInOut(board.D11)
 
    led3 = digitalio.DigitalInOut(board.D0)
    led4 = digitalio.DigitalInOut(board.D5)
    led5 = digitalio.DigitalInOut(board.D6)

    led6 = digitalio.DigitalInOut(board.D13)
    led7 = digitalio.DigitalInOut(board.D19)

    led8 = digitalio.DigitalInOut(board.D14)
    led9 = digitalio.DigitalInOut(board.D15)
    led10 = digitalio.DigitalInOut(board.D18)

    led11 = digitalio.DigitalInOut(board.D24)

    led12 = digitalio.DigitalInOut(board.D25)
    led13 = digitalio.DigitalInOut(board.D8)
    led14 = digitalio.DigitalInOut(board.D7)
    led15 = digitalio.DigitalInOut(board.D1)

    led16 = digitalio.DigitalInOut(board.D12)
    led17 = digitalio.DigitalInOut(board.D16)
    led18 = digitalio.DigitalInOut(board.D20)
    led19 = digitalio.DigitalInOut(board.D21)

    leds = [led0,led1,led2,led3,led4,led5,led6,
            led7,led8,led9,led10,led11,led12,led13,led14,
            led15,led16,led17,led18,led19]

    for i in leds:
        i.direction = digitalio.Direction.OUTPUT

    for i in leds:
        i.value = True
        sleep(0.02)
    
    for i in leds:
        i.value = False   
        sleep(0.02)

def run_led():
    led0 = digitalio.DigitalInOut(board.D18)
    led1 = digitalio.DigitalInOut(board.D25)
    led2 = digitalio.DigitalInOut(board.D12)
    led3 = digitalio.DigitalInOut(board.D13)
    led4 = digitalio.DigitalInOut(board.D19)
    leds = [led0,led1,led2,led3,led4]
    for i in leds:
        i.direction = digitalio.Direction.OUTPUT

    for i in leds:
        i.value = True
        sleep(0.02)
    
    for i in leds:
        i.value = False   
        sleep(0.02)

def drawTriangle():
    oled.fill(0)
    for y in range(0,8):
        oled.pixel(64-y,y,1)
        oled.pixel(64, y, 1)
        oled.pixel(64+y,y,1)
        oled.show()
    for x in range(56,72): # 32--64--96
        oled.pixel(x,7,1)
        oled.show()

def drawLoadingBar():
    oled.fill(0)
    for x in range(0,127): # 32--64--96
        oled.pixel(x,31,1)
        oled.show()

def checkForIPandSSID():
    global copy_ip
    global ssid_str
    # print("checking for IP address")
    device = 'wlan0'
    cmd = "ip addr show %s | awk '$1 == \"inet\" {gsub(/\/.*$/, \"\", $2); print $2}'" % device

    p = subprocess.Popen(cmd, shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT)
    out, _ = p.communicate()
    local_ip = str(out.strip().decode('UTF-8'))
    copy_ip = local_ip
    # print(copy_ip)
    # print("connected!")

    oled.fill(0)
    oled.text('IPv4 Address', 0, 0, True)
    oled.text('WiFi Connected', 0, 10, True)
    oled.text(copy_ip, 0, 20, True)
    oled.show()
    sleep(1)
    oled.fill(0)
    # print("checking for SSID")
    returnVal = os.system('iwgetid')
    oled.text('SSID Verified', 0, 0, True)
    oled.text(local_ip, 0, 10, True)
    oled.text('iwgetid:'+ str(returnVal), 0, 20, True)
    oled.show()
    sleep(1)
    oled.fill(0)
    # print(returnVal)
    if(returnVal == 0):
        output = subprocess.check_output(['iwgetid'])
        out = output.split(b'"')[1]
        ssid_str = out.decode('UTF-8')
        # print(ssid_str)
        oled.text('Connected to SSID', 0, 0, True)
        oled.text(ssid_str, 0, 10, True)
        oled.show()
        sleep(1)
        oled.fill(0)
    else:
        oled.text(local_ip, 0, 0, True)
        oled.show()
        output = subprocess.check_output(['iwgetid'])
        out = output.split(b'"')[1]
        ssid_str = out.decode('UTF-8')
        # print(ssid_str)
        oled.text(ssid_str, 0, 10, True)
        oled.show()
        sleep(1)
        oled.fill(0)
buzz.value = True
sleep(0.05)
buzz.value = False
sleep(0.1)

buzz.value = True
sleep(0.05)
buzz.value = False
sleep(0.1)

def displayIP():
    oled.fill(0)
    oled.text('IPv4 Address Verified', 0, 0, True)
    oled.text(ssid_str, 0, 10, True)
    oled.text('[  '+copy_ip+'  ]', 0, 20, True)
    oled.show()

try:
    try:
        i2c = io.I2C(board.SCL, board.SDA)
        # once i2c succesfully initialized, then proceed with i2c object declaration
        oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
    except (OSError,ValueError,NameError) as e:
        e = str(e)
        print("Exception Caught: %s\n" %  e)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y, %H:%M:%S, ")
        f = open("repeatconnect2wifi_log.txt", "a")
        f.write(str(dt_string + e + "\n"))
        f.close()

        # print("Oops!", sys.exc_info()[0], "occurred.")
        buzz.value = True
        sleep(0.1)
        buzz.value = False
        sleep(0.1)
        buzz.value = True
        sleep(0.1)
        buzz.value = False
        for i in range(0,5):
            if(i%2==0):
                i2cErrorSignal.value = True
            else:
                i2cErrorSignal.value = False
            sleep(0.1)

    if DEFINED_PI_ZERO_W:
        run_led()
    else:
        run_led_maker_hat_base()

    oled.fill(0)  
    oled.text('crontab startup', 0, 0, True)
    oled.text('running connect2wifi', 0, 10, True)
    oled.text('crontab sleep 10', 0, 20, True)
    oled.show()
    sleep(1)

    # drawTriangle()
    # drawLoadingBar()
    oled.fill(0)  
    if not DEFINED_PI_ZERO_W:
        oled.text('Hello from Pi 3B+', 0, 0, True)
    else:
        oled.text('Hello from Zero W', 0, 0, True)
    oled.text('Connecting to WiFi', 0, 10, True)
    oled.text('This might fail', 0, 20, True)
    # oled.text('123456789ABCDEFGHIJKLMN', 0, 0, True)
    oled.show()
    sleep(0.5)
    checkForIPandSSID()
    displayIP()

except Exception as e:
    e = str(e)
    print("Exception Caught: %s\n" %  e)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y, %H:%M:%S, ")
    f = open("/home/pi/pi-workspace/connect2wifi_log.txt", "a")
    f.write(str(dt_string + e + "\n"))
    f.close()

    oled.fill(0)
    oled.text('IP:'+local_ip, 0, 0, True)
    oled.text('SSID:'+ssid_str, 0, 10, True)
    oled.show()

    count = 1
    buzz.value = True
    sleep(0.25)
    buzz.value = False
    sleep(0.5)
    # print("Exception:" , e)
    oled.fill(0)  
    msg = str(e)

    # use this line to display only a portion of msg
    oled.text(local_ip, 0, 0, True)
    oled.text(msg, 0, 10, True)
    oled.show()

   
    # uncomment the following for the animated text display

    # if(len(msg) > MAX_CHAR_DISPLAYABLE):
    #     oled.text(local_ip, 0, 0, True)
    #     oled.text('Exception len:'+str(len(msg)), 0, 10, True)
    #     for i in range(0,len(msg)):
    #         if(i < MAX_CHAR_DISPLAYABLE):
    #             oled.text(msg[0:i], 0, 20, True)
    #         else:
    #             oled.fill(0)
    #             oled.text(local_ip, 0, 0, True)
    #             oled.text('Exception len:'+str(len(msg)), 0, 10, True)
    #             lengthOfChar = len(msg[MAX_CHAR_DISPLAYABLE:i])
    #             if(lengthOfChar == MAX_CHAR_DISPLAYABLE*count):
    #                 count += 1
    #             oled.text(msg[MAX_CHAR_DISPLAYABLE*count:i], 0, 20, True)
    #         oled.show()
    #     oled.show()
    # else:
    #     oled.text(local_ip, 0, 0, True)
    #     oled.show()
    #     oled.text('Exception len:'+str(len(msg)), 0, 10, True)
    #     oled.text(msg, 0, 20, True)
    #     oled.show()



