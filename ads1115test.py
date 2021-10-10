import time
import board
import busio
import busio as io
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
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
time.sleep(1)
oled.fill(0)
# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

# Create single-ended input on channel 0

chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2)
chan3 = AnalogIn(ads, ADS.P3)

channels = [chan0,chan1,chan2,chan3]

# Create differential input between channel 0 and 1
#chan = AnalogIn(ads, ADS.P0, ADS.P1)


while True:
    print("{:>5}\t{:>5}".format('raw', 'v'))
    for ch in channels:
        print("{:>5}\t{:>5.3f}".format(ch.value, ch.voltage))
        oled.text('ADS1115 Value', 0, 0, True)
        oled.text(str(chan0.value), 0, 10, True)
        oled.invert(False)
        oled.show()
        time.sleep(0.01)
        oled.fill(0)