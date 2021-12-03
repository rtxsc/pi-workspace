#!/usr/bin/env python3
import board
from digitalio import DigitalInOut, Direction, Pull
import adafruit_ssd1306
import busio as io
import subprocess
import os
from time import sleep

restart_pin = DigitalInOut(board.D23)
shut_down_pin = DigitalInOut(board.D27) # any pin!
restart_pin.direction = Direction.INPUT
shut_down_pin.direction = Direction.INPUT
# modified on 3.11.2021 referred via https://www.npmjs.com/package/onoff
# https://github.com/fivdi/onoff/wiki/Enabling-Pullup-and-Pulldown-Resistors-on-The-Raspberry-Pi

shut_down_pin.pull = Pull.UP # good to know this method anyway
restart_pin.pull = Pull.UP

buzz = DigitalInOut(board.D26)
buzz.direction = Direction.OUTPUT
i2cErrorSignal = DigitalInOut(board.D21)
i2cErrorSignal.direction = Direction.OUTPUT

def beep_twice():
    buzz.value = True
    sleep(0.5)
    buzz.value = False
    sleep(0.1)
    buzz.value = True
    sleep(0.5)
    buzz.value = False

try:
    i2c = io.I2C(board.SCL, board.SDA)
    # once i2c succesfully initialized, then proceed with i2c object declaration
    oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

except (OSError,ValueError,NameError):
    # print("Oops!", sys.exc_info()[0], "occurred.")
    beep_twice()
    for i in range(0,5):
        if(i%2==0):
            i2cErrorSignal.value = True
        else:
            i2cErrorSignal.value = False
        sleep(0.1)


# modular function to shutdown Pi
def shut_down():
    print("[WARNING] Shutting down Pi now from button D27 press!")
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)

def restart():
    print("Restarting Pi via D23 interrupt")
    command = "/usr/bin/sudo /sbin/reboot -h now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)

def checkForIPandSSID():
    global local_ip
    global ssid_str
    # print("checking for IP address")
    device = 'wlan0'
    cmd = "ip addr show %s | awk '$1 == \"inet\" {gsub(/\/.*$/, \"\", $2); print $2}'" % device

    p = subprocess.Popen(cmd, shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT)
    out, _ = p.communicate()
    local_ip = str(out.strip().decode('UTF-8'))

    output = subprocess.check_output(['iwgetid'])
    out = output.split(b'"')[1]
    ssid_str = out.decode('UTF-8')

buzz.value = True
sleep(0.05)
buzz.value = False
sleep(0.1)

buzz.value = True
sleep(0.05)
buzz.value = False
sleep(0.1)


try:
    checkForIPandSSID()
    while True:
        pinState = shut_down_pin.value
        pinRestart = restart_pin.value
        # print(pinState, pinRestart)
        if(pinRestart == False):
            beep_twice()
            beep_twice()
            oled.fill(0)
            oled.text('RESTARTING PI NOW',0,0,True)
            oled.text('D26 Interrupt Detected',0,0,True)
            sleep(2)
            restart()


        if(pinState == False):
            beep_twice()
            oled.fill(0)
            oled.text('SHUTTING DOWN NOW', 0, 0, True)
            oled.text('Bye-bye from Pi', 0, 10, True)
            oled.text('See You Soon', 0, 20, True)
            oled.show()
            sleep(2)
            shut_down()
        else:
            oled.fill(0)
            oled.text('D23:REST D27:SHUT', 0, 0, True)
            oled.text('>>'+ssid_str+'<<', 0, 10, True)
            oled.text('>>'+local_ip+'<<', 0, 20, True)
            oled.show()
        sleep(1)

except KeyboardInterrupt:
    print("Program Halted by Ctrl+C")
