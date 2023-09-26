import displayio
import terminalio
from adafruit_bitmap_font import bitmap_font
import adafruit_displayio_ssd1306
from adafruit_display_text import label

class simple_ssd:
    def __init__(self, i2c_h):
        self.i2c    = i2c_h
        self.WIDTH  = 128
        self.HEIGHT = 32  # Change to 64 if needed
        self.BORDER = 1
        self.display_bus = displayio.I2CDisplay(i2c_h, device_address=0x3c)
        self.display = adafruit_displayio_ssd1306.SSD1306(self.display_bus, width=self.WIDTH, height=self.HEIGHT)
        self.text   ="SSD" 
        self.font   = bitmap_font.load_font("/Helvetica-Bold-16.bdf")
        self.color  = 0xFFFFFF
        self.text_area = label.Label(self.font, text=self.text, color=self.color)
        self.text_area.x = 2
        self.text_area.y = 16
    @classmethod    
    def release(self):
        displayio.release_displays()
        
    def print(self, txt):
        self.text = txt
        self.text_area = label.Label(self.font, text=self.text, color=self.color)
        self.text_area.x = 2
        self.text_area.y = 16
        self.display.show(self.text_area)

def release():
    displayio.release_displays()
        