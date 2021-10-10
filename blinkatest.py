import board
import digitalio
import busio
import time

print("Hello blinka!")

# Try to great a Digital input
pin = digitalio.DigitalInOut(board.D4)
print("Digital IO ok!")

# Try to create an I2C device
i2c = busio.I2C(board.SCL, board.SDA)
print("I2C ok!")

# Try to create an SPI device
spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)
print("SPI ok!")

print("done!")


print("hello blinky!")

buzz = digitalio.DigitalInOut(board.D26)
led0 = digitalio.DigitalInOut(board.D17)
led1 = digitalio.DigitalInOut(board.D18)
led2 = digitalio.DigitalInOut(board.D27)
led3 = digitalio.DigitalInOut(board.D22)
led4 = digitalio.DigitalInOut(board.D25)
led5 = digitalio.DigitalInOut(board.D12)
led6 = digitalio.DigitalInOut(board.D13)
led7 = digitalio.DigitalInOut(board.D19)
leds = [led0,led1,led2,led3,led4,led5,led6,led7]

buzz.direction = digitalio.Direction.OUTPUT
for i in leds:
    i.direction = digitalio.Direction.OUTPUT

delay = 0.025
while True:
    for i in leds:
        i.value = True
        time.sleep(delay)
    buzz.value = True
    time.sleep(delay*2)
    buzz.value = False
    time.sleep(delay*2)
    for i in leds:
        i.value = False   
        time.sleep(delay)
