# IOT_Sensors
IOT Sensors Proj

sudo rasp-config

1. enable ssh

2. enable i2c

reboot

sudo apt-get update

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

connect 0.96 inches OLED module to I2C 0 port

connect DHT22 module signal wire to GPIO 4 port

