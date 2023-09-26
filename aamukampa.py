'''
Aamukampa 

https://github.com/adafruit/circuitpython/issues/851
https://learn.adafruit.com/adafruit-wave-shield-audio-shield-for-arduino/convert-files
https://learn.adafruit.com/mp3-playback-rp2040/pico-mp3
https://learn.adafruit.com/wave-shield-talking-clock/stuff
https://docs.circuitpython.org/en/8.2.x/README.html
https://learn.adafruit.com/adafruit-audio-bff/circuitpython
https://learn.adafruit.com/circuitpython-display-support-using-displayio

'''

import audiocore
from audiocore import RawSample
from audiocore import WaveFile
import audiopwmio
import audiobusio
#import audiomixer
import time
import board
import busio
import digitalio
import pico_rtc_u2u_sd_gpio as gpio
import array
import math
from adafruit_pcf8563.pcf8563 import PCF8563

# Storage libraries
import adafruit_sdcard
import storage

from simple_ssd import simple_ssd
import rtc_pcf8563 as rtc


#ssd.release()

# Display libraries
#import displayio
#import terminalio
#from adafruit_bitmap_font import bitmap_font
#import adafruit_displayio_ssd1306
#from adafruit_display_text import label


spi = busio.SPI(gpio.SD_CLK_PIN, gpio.SD_MOSI_PIN, gpio.SD_MISO_PIN)
cs = digitalio.DigitalInOut(gpio.SD_CS_PIN)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

simple_ssd.release()

i2c_en = digitalio.DigitalInOut(gpio.EN_I2C_PIN)
i2c_en.direction = digitalio.Direction.OUTPUT
i2c_en.value = 1

# Change to the appropriate I2C clock & data pins here!
i2c_bus = busio.I2C(gpio.I2C0_SCL_PIN, gpio.I2C0_SDA_PIN, frequency=100000)
i2c1 = busio.I2C(gpio.I2C1_SCL_PIN, gpio.I2C1_SDA_PIN, frequency=1000000)

ssd  = simple_ssd(i2c1)

ssd.print("AAMUKAMPA")


# Create the RTC instance:

rtc.initialize(i2c_bus)

rtc.print_time()