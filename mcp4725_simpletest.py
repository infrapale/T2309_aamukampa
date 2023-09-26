# SPDX-FileCopyrightText: 2018 Tony DiCola for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of setting the DAC value up and down through its entire range
# of values.
import board
import busio
import time
import adafruit_mcp4725
import digitalio
import pico_rtc_u2u_sd_gpio as gpio

# Initialize I2C bus.
# i2c = busio.I2C(gpio.I2C0_SCL_PIN, gpio.I2C0_SDA_PIN, frequency=1000000)
i2c = busio.I2C(gpio.I2C1_SCL_PIN, gpio.I2C1_SDA_PIN, frequency=1000000)
#i2c = busio.I2C(board.SCL, board.SDA)
i2c_en = digitalio.DigitalInOut(gpio.EN_I2C_PIN) 
i2c_en.direction = digitalio.Direction.OUTPUT
i2c_en.value = 1

while not i2c.try_lock():
    pass

try:
    while True:
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
