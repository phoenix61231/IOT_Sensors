import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def load_font():
    #font = ImageFont.load_default()	
    font = ImageFont.truetype('/home/pi/Desktop/IOT_Sensors/font/Montserrat-Light.ttf', 12)
    font2 = ImageFont.truetype('/home/pi/Desktop/IOT_Sensors/font/fontawesome-webfont.ttf', 14)
    font_icon_big = ImageFont.truetype('/home/pi/Desktop/IOT_Sensors/font/fontawesome-webfont.ttf', 20)
    font_text_big = ImageFont.truetype('/home/pi/Desktop/IOT_Sensors/font/Montserrat-Medium.ttf', 19)
	
    return font, font2, font_icon_big, font_text_big
	
def draw_shape(height):
    # First define some constants to allow easy resizing of shapes.
    padding = -2
    top = padding
    bottom = height-padding
	
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0
	
    return x, top
	
def def_size(disp):
    width = disp.width
    height = disp.height
	
    return width, height
	
def create_blank(width, height):
    # Make sure to create image with mode '1' for 1-bit color.	
    image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)
	
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
	
    return image, draw
	

def init_connect():
    # Raspberry Pi pin configuration:
    RST = None     # on the PiOLED this pin isnt used
    # Note the following are only used with SPI:
    DC = 23
    SPI_PORT = 0
    SPI_DEVICE = 0
	
    return RST
	
def init_disp(RST):
    # 128x64 display with hardware I2C:
    disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
    #if disp fail fix		
		
    # Initialize library.
    disp.begin()

    # Clear display.
    disp.clear()
    disp.display()		
	
    return disp
