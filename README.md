IOT Sensors Proj

sudo raspi-config

1. enable ssh

2. enable i2c

3. enable spi

4. enable console and autologin

5. enable wait for network at boot

reboot

sudo apt-get update

auto launch :

https://www.raspberrypi-spy.co.uk/2015/02/how-to-autorun-a-python-script-on-raspberry-pi-boot/

main:

sudo git clone https://github.com/phoenix61231/IOT_Sensors

Clone repositories below under the IOT_Sensors folder 

OLED:

sudo git clone https://github.com/adafruit/Adafruit_Python_SSD1306

cd Adafruit_Python_SSD1306

sudo apt-get install build-essential python-dev python-pip python-imaging python-smbus git

sudo pip install RPi.GPIO

sudo python setup.py install

DHT22:

sudo git clone https://github.com/adafruit/Adafruit_Python_DHT

cd Adafruit_Python_DHT

sudo apt-get install build-essential python-dev

sudo python setup.py install

BMP180:

sudo git clone https://github.com/adafruit/Adafruit_Python_BMP

cd Adafruit_Python_BMP

sudo python setup.py install

Paho:

pip install paho-mqtt

git clone https://github.com/eclipse/paho.mqtt.python.git

cd paho.mqtt.python

python setup.py install



connect 0.96 inches OLED module to I2C 0 port

connect BMP180 module to I2C 0 port

connect DHT22 module signal wire to GPIO 4 port

connect MCP3008 ADC to Pi

connect TEMT600 module to MCP3008 0

connect GUVA-S12SD module to MCP3008 1

connect FC-28 module to MCP3008 2
