import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

import Adafruit_DHT

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

import paho.mqtt.client as mqtt
import thread
import os

import spidev

import Adafruit_BMP.BMP085 as BMP085

spi = spidev.SpiDev()
spi.open(0, 0)

def on_message(client, userdata, message):
	print(str(message.payload.decode("utf-8") + " (" + message.topic + ")"))

def ReadADC(ch):
    if((ch>7) or (ch<0)):
        return -1
    adc = spi.xfer2([1,(8+ch)<<4,0])
    data = ((adc[1]&3)<<8) + adc[2]
    return data

def ReadVolts(data, deci):
    volts = (data*3.3)/float(1023)
    volts = round(volts,deci)
    return volts

def getdht22(sensor, pin):
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    if humidity is not None and temperature is not None:
        print('Temperature : {0:0.1f}*C\nHumidity : {1:0.1f}%'.format(temperature,humidity))
    else:
        print('.')
    return humidity, temperature

def getsoil(ch,deci):
    soil_data = ReadADC(ch)
    soil_volts = ReadVolts(soil_data, deci)

    if soil_data is not None and soil_volts is not None:
        print('Soil Moisture : {0:d} ({1:0.2f} V)'.format(soil_data, soil_volts))
    else:
        print('.')
    return soil_data

def getlight(ch,deci):
    light_data = ReadADC(ch)
    light_volts = ReadVolts(light_data, deci)

    if light_data is not None and light_volts is not None:
        print('Light : {0:d} ({1:0.2f} V)'.format(light_data, light_volts))
    else:
        print('.')
    return light_data

def getuv(ch,deci):
    uv_data = ReadADC(ch)
    uv_volts = ReadVolts(uv_data, deci)

    if uv_data is not None and uv_volts is not None:
        print('UV : {0:d} ({1:0.2f} V)'.format(uv_data, uv_volts))
    else:
        print('.')
    return uv_data
    
    
# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding

# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load default font.
font = ImageFont.load_default()

font = ImageFont.truetype('Montserrat-Light.ttf', 12)
font2 = ImageFont.truetype('fontawesome-webfont.ttf', 14)
font_icon_big = ImageFont.truetype('fontawesome-webfont.ttf', 20)
font_text_big = ImageFont.truetype('Montserrat-Medium.ttf', 19)

# Note that sometimes you won't get a readin and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!
# Modify the broker ip here, default will be uscclab server
broker_address = "140.116.82.42"

# create new instance , change the instance name here to avoid crash
print("creating new instance")
instance = "module_001"
client = mqtt.Client(instance)
client.on_message = on_message

print("connecting to broker at " + broker_address)
client.connect(broker_address)  # connect to broker

# Enter the topic to subscribe here, web default is "mqtt/demo"
topic = "mqtt/demo"

client.loop_start()  # start the loop
print("Subscribing to topic : " + topic)
client.subscribe(topic)

print('----------------------------------------')

while True:
    humidity_value, temperature_value = getdht22(Adafruit_DHT.DHT22,'4')
    light_value = getlight(0, 2)
    uv_value = getuv(1, 2)
    soil_value = getsoil(2, 2)

    bmp180 = BMP085.BMP085()
    pressure_value = bmp180.read_pressure()
    print "Air Pressure : {0:0.3f} kPa\n".format(pressure_value/1000.0)

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1 | head --bytes -1"
    IP = subprocess.check_output(cmd, shell = True )
    cmd = "top -bn1 | grep load | awk '{printf \"%.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell = True )
    cmd = "free -m | awk 'NR==2{printf \"MEM: %.2f%%\", $3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True )
    
    line = instance + ' ' + IP + '\nTemperature:{0:0.1f} Humidity:{1:0.1f} Light:{2:d} UV:{3:d} Soil:{4:d} Pressure:{5:0.3f}'.format(humidity_value, temperature_value, light_value, uv_value, soil_value, pressure_value/1000.0)
    client.publish(topic, line)

    # Icons
    draw.text((x, top),       unichr(61931),  font=font2, fill=255) #wifi icon
    draw.text((x, top+15),    unichr(62171),  font=font_icon_big, fill=255) #cpu icon
    
    draw.text((18, top),      str(IP),  font=font, fill=255) 
    draw.text((x+22, top+12), str(CPU), font=font_text_big, fill=255) 
    draw.text((x, top+36),    str(MemUsage),  font=font, fill=255)
    
    # Display image.
    disp.image(image)
    disp.display()

    print "Ctrl + C to exit"
    print "----------------------------------------"
    time.sleep(5)

