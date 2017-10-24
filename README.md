# IOT_Sensors
IOT Sensors Proj

sudo rasp-config
1. enable ssh
2. enable i2c
reboot

sudo apt-get update

OLED:

sudo apt-get install build-essential python-dev python-pip python-imaging python-smbus git
sudo pip install RPi.GPIO
sudo python setup.py install

DHT22:

sudo apt-get install build-essential python-dev
sudo python setup.py install

