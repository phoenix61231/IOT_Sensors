IOT Sensors Proj

sudo raspi-config

1. enable ssh

2. enable i2c

3. enable spi

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

<<<<<<< HEAD
=======
BMP180:

sudo git clone https://github.com/adafruit/Adafruit_Python_BMP

cd Adafruit_Python_BMP

sudo python setup.py install

>>>>>>> 10e8c040dd78000fc88a56470740de45dee116d7
Paho:

pip install paho-mqtt

git clone https://github.com/eclipse/paho.mqtt.python.git

<<<<<<< HEAD
cd paoh.mqtt.python
=======
cd paho.mqtt.python
>>>>>>> 10e8c040dd78000fc88a56470740de45dee116d7

python setup.py install


connect 0.96 inches OLED module to I2C 0 port

<<<<<<< HEAD
connect DHT22 module signal wire to GPIO 4 port
=======
connect DHT22 module signal wire to GPIO 4 port

>>>>>>> 10e8c040dd78000fc88a56470740de45dee116d7
