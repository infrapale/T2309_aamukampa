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


# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(WIDTH - BORDER * 2, HEIGHT - BORDER * 2, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000  # Black
inner_sprite = displayio.TileGrid(
    inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER
)
splash.append(inner_sprite)

# Draw a label
text = "Hello World!"
text_area = label.Label(
    terminalio.FONT, text=text, color=0xFFFFFF, x=28, y=HEIGHT // 2 - 1
)
splash.append(text_area)

while True:
    pass

# ---------------------------------------------------------------------------------------


while not i2c.try_lock():
    pass

try:
    while flase:
        print(
            "I2C addresses found:",
            [hex(device_address) for device_address in i2c.scan()],
        )
        time.sleep(2)

finally:  # unlock the i2c bus when ctrl-c'ing out of the loop
    i2c.unlock()


# Initialize MCP4725.
dac = adafruit_mcp4725.MCP4725(i2c, address=0x60)
# Optionally you can specify a different addres if you override the A0 pin.
# amp = adafruit_max9744.MAX9744(i2c, address=0x63)

# There are a three ways to set the DAC output, you can use any of these:
dac.value = 65535  # Use the value property with a 16-bit number just like
# the AnalogOut class.  Note the MCP4725 is only a 12-bit
# DAC so quantization errors will occur.  The range of
# values is 0 (minimum/ground) to 65535 (maximum/Vout).

dac.raw_value = 4095  # Use the raw_value property to directly read and write
# the 12-bit DAC value.  The range of values is
# 0 (minimum/ground) to 4095 (maximum/Vout).

dac.normalized_value = 1.0  # Use the normalized_value property to set the
# output with a floating point value in the range
# 0 to 1.0 where 0 is minimum/ground and 1.0 is
# maximum/Vout.

# Main loop will go up and down through the range of DAC values forever.
while True:
    # Go up the 12-bit raw range.
    print("Going up 0-3.3V...")
    for i in range(4095):
        dac.raw_value = i
        time.sleep(0.01)
    # Go back down the 12-bit raw range.
    print("Going down 3.3-0V...") 
    for i in range(4095, -1, -1):
        dac.raw_value = i
        time.sleep(0.01)

