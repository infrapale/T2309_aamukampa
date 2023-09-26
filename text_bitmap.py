# SPDX-FileCopyrightText: 2018 Tony DiCola for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of setting the DAC value up and down through its entire range
# of values.

# https://learn.adafruit.com/circuitpython-display-support-using-displayio

import board
import busio
import time
import adafruit_mcp4725
import digitalio
import pico_rtc_u2u_sd_gpio as gpio
import displayio
import terminalio
from adafruit_bitmap_font import bitmap_font
import adafruit_displayio_ssd1306
from adafruit_display_text import label

displayio.release_displays()

# Initialize I2C bus.
# i2c = busio.I2C(gpio.I2C0_SCL_PIN, gpio.I2C0_SDA_PIN, frequency=1000000)
i2c = busio.I2C(gpio.I2C1_SCL_PIN, gpio.I2C1_SDA_PIN, frequency=1000000)
#i2c = busio.I2C(board.SCL, board.SDA)
i2c_en = digitalio.DigitalInOut(gpio.EN_I2C_PIN) 
i2c_en.direction = digitalio.Direction.OUTPUT
i2c_en.value = 1

WIDTH = 128
HEIGHT = 32  # Change to 64 if needed
BORDER = 1

display_bus = displayio.I2CDisplay(i2c, device_address=0x3c)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)


# Set text, font, and color
text = "24.09.23 12:01"
font = bitmap_font.load_font("/Helvetica-Bold-16.bdf")
color = 0xFFFFFF

# Create the tet label
text_area = label.Label(font, text=text, color=color)

# Set the location
text_area.x = 2
text_area.y = 16

# Show it
display.show(text_area)
time.sleep(5.0)

text_area.text = "New text"

time.sleep(5.0)

text_area.text = "XX"

while True:
    pass

# ---------------------------------------------------------------------------------------
