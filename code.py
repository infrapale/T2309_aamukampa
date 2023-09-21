# SPDX-FileCopyrightText: 2019 Sommersoft
# SPDX-FileCopyrightText: Copyright (c) 2021 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

# Simple demo of reading and writing the time for the PCF8563 real-time clock.
# Change the if False to if True below to set the time, otherwise it will just
# print the current date and time every second.  Notice also comments to adjust
# for working with hardware vs. software I2C.

# import audiocore
from audiocore import RawSample
import audiopwmio
import time
import board
import busio
import digitalio
import pico_rtc_u2u_sd_gpio as gpio
import array
import math

from adafruit_pcf8563.pcf8563 import PCF8563
i2c_en = digitalio.DigitalInOut(gpio.EN_I2C_PIN)
i2c_en.direction = digitalio.Direction.OUTPUT
i2c_en.value = 1

# Change to the appropriate I2C clock & data pins here!
i2c_bus = busio.I2C(gpio.I2C0_SCL_PIN, gpio.I2C0_SDA_PIN, frequency=100000)
#i2c_bus = busio.I2C(board.SCL, board.SDA)

# Create the RTC instance:
rtc = PCF8563(i2c_bus)

# Lookup table for names of days (nicer printing).
days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")


# pylint: disable-msg=using-constant-test
if True:  # change to True if you want to set the time!
    #                     year, mon, date, hour, min, sec, wday, yday, isdst
    t = time.struct_time((2023, 9, 16, 14, 54, 0, 5, -1, -1))
    # you must set year, mon, date, hour, min, sec and weekday
    # yearday is not supported, isdst can be set but we don't do anything with it at this time
    print("Setting time to:", t)  # uncomment for debugging
    rtc.datetime = t
    print()
# pylint: enable-msg=using-constant-test


# Main loop:
while True:
    if rtc.datetime_compromised:
        print("RTC unset")
    else:
        print("RTC reports time is valid")
    t = rtc.datetime
    print(t)     # uncomment for debugging
    print(
        "The date is {} {}/{}/{}".format(
            days[int(t.tm_wday)], t.tm_mday, t.tm_mon, t.tm_year
        )
    )
    print("The time is {}:{:02}:{:02}".format(t.tm_hour, t.tm_min, t.tm_sec))
    time.sleep(1)  # wait a second
    
    # Generate one period of sine wav.
    try:
        from audioio import AudioOut
    except ImportError:
        try:
            from audiopwmio import PWMAudioOut as AudioOut
        except ImportError:
            pass  # not always supported by every board!

    button = digitalio.DigitalInOut(board.A1)
    button.switch_to_input(pull=digitalio.Pull.UP)

    tone_volume = 0.1  # Increase this to increase the volume of the tone.
    frequency = 440  # Set this to the Hz of the tone you want to generate.
    length = 8000 // frequency
    sine_wave = array.array("H", [0] * length)
    for i in range(length):
        sine_wave[i] = int((1 + math.sin(math.pi * 2 * i / length)) * tone_volume * (2 ** 15 - 1))

    audio = AudioOut(gpio.PWM7A_PIN)
    sine_wave_sample = RawSample(sine_wave)

    while True:
        if True:   #not button.value:
            audio.play(sine_wave_sample, loop=True)
            time.sleep(1)
            audio.stop()
