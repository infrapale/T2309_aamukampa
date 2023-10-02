'''
Aamukampa 

https://github.com/adafruit/circuitpython/issues/851
https://learn.adafruit.com/adafruit-wave-shield-audio-shield-for-arduino/convert-files
https://learn.adafruit.com/mp3-playback-rp2040/pico-mp3
https://learn.adafruit.com/wave-shield-talking-clock/stuff
https://docs.circuitpython.org/en/8.2.x/README.html
https://learn.adafruit.com/adafruit-audio-bff/circuitpython
https://learn.adafruit.com/circuitpython-display-support-using-displayio
https://bigsoundbank.com/categories.html
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
import adafruit_mcp4725
import aamu

# Storage libraries
import adafruit_sdcard
import storage

from simple_ssd import simple_ssd
from rtc_pcf8563 import rtc_pcf8563


#ssd.release()

# Display libraries
#import displayio
#import terminalio
#from adafruit_bitmap_font import bitmap_font
#import adafruit_displayio_ssd1306
#from adafruit_display_text import label


uart = busio.UART(gpio.TX1_PIN, gpio.RX1_PIN, baudrate=9600)
spi = busio.SPI(gpio.SD_CLK_PIN, gpio.SD_MOSI_PIN, gpio.SD_MISO_PIN)
cs = digitalio.DigitalInOut(gpio.SD_CS_PIN)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!

simple_ssd.release()

i2c_en = digitalio.DigitalInOut(gpio.EN_I2C_PIN)
i2c_en.direction = digitalio.Direction.OUTPUT
i2c_en.value = 1

# Change to the appropriate I2C clock & data pins here!
i2c_bus = busio.I2C(gpio.I2C0_SCL_PIN, gpio.I2C0_SDA_PIN, frequency=100000)
i2c1 = busio.I2C(gpio.I2C1_SCL_PIN, gpio.I2C1_SDA_PIN, frequency=1000000)


ssd  = simple_ssd(i2c1)
rtc = rtc_pcf8563(i2c_bus)
dac = adafruit_mcp4725.MCP4725(i2c1, address=0x60)

ssd.print("AAMUKAMPA")
# rtc.set_time()
rtc.print_time()


DISP_LEN = 16

cur_raw = 0


def ssd_aamuja(n,t):
    global cur_raw
    raw_str = " Aamuja {:n}.{:n} : {:3n} ".format(t.tm_mon,t.tm_mday,n)
    len_raw = len(raw_str)
    last = cur_raw + DISP_LEN
    if last < len_raw:
        aamuja_str = raw_str[cur_raw:cur_raw + DISP_LEN]
    else:
        aamuja_str = raw_str[cur_raw:len_raw]
        aamuja_str = aamuja_str + raw_str[0:DISP_LEN-(len_raw-cur_raw)]
    
    print(aamuja_str)    
    ssd.print(aamuja_str)
    cur_raw = cur_raw + 1
    if cur_raw >= len_raw:
        cur_raw = 0
    
def dac_aamuja(n):
    a = 0
    if n <= 50:
        a = n/50 * 3700
    elif n <= 150:
        a = n/150 * 3700
    dac.raw_value = int(a)
  
def open_audio(file_name):
    f = open(file_name, "rb")
    w = audiocore.WaveFile(f)
    return f, w

def play_audio(file_name):
    try:
        with open(file_name, "rb") as f:
            wave = WaveFile(f)
            audio = AudioOut(gpio.PWM7B_PIN)
            print("playing", file_name)
            audio.play(wave)
            while audio.playing:
                pass
    except:
        print("failed", file_name)
        pass

#file_name = "chime_big_ben_2.wav"
file_name = "/sd/chime_big_ben_2.wav"
#file_name = "/sd/cat-time.wav"


# aamuja = 40
aamuja_offset = 0

iter_cnt = 1
SSD_UPDATE_INTERVAL = 0.2

next_ssd_time = time.monotonic() + SSD_UPDATE_INTERVAL
while 1:
    t = rtc.get_time()
    aamuja = aamu.how_many(t.tm_mon,t.tm_mday)
    if uart.in_waiting > 0: 
        key = uart.read(1)
    else:       
        key = None
    if key != None:
        print(chr(key[0]))
        if chr(key[0]) == 'H':
            aamuja_offset = aamuja_offset - 10
            file_name = "/sd/sanna_2b.wav"
            play_audio(file_name)
        elif chr(key[0]) == 'D':
            aamuja_offset = aamuja_offset + 10
            file_name = "/sd/sanna_ojojb.wav"
            play_audio(file_name)
        elif chr(key[0]) == 'A':
            file_name = "/sd/chime_big_ben_2b.wav"
            play_audio(file_name)

        elif chr(key[0]) == 'B':
            play_audio('/sd/alarm_beep.vaw')

            
    a = aamuja + aamuja_offset
    if a < 0:
        a = 0
    if a > 150:
        a = 150

    dac_aamuja(a)
    if time.monotonic() > next_ssd_time:
        next_ssd_time = time.monotonic() + SSD_UPDATE_INTERVAL
        ssd_aamuja(a,t)


'''
file_name = "/sd/chime_big_ben_2.wav"
'''