# IOT Sensors Proj

### sudo raspi-config

- 1. enable ssh

- 2. enable i2c

- 3. enable spi

- 4. enable console and autologin

- 5. enable wait for network at boot (optional)

reboot

- sudo apt-get update

- sudo apt-get install vim

- sudo apt-get install git

## Connect to Wifi:

https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md

## Wifi auto reconnect (had connected before):

http://alexba.in/blog/2015/01/14/automatically-reconnecting-wifi-on-a-raspberrypi/

## Auto launch :

https://www.raspberrypi-spy.co.uk/2015/02/how-to-autorun-a-python-script-on-raspberry-pi-boot/

## Static IP Address(optional):

http://yehnan.blogspot.tw/2016/05/raspberry-piipdhcpcd.html

## main:

- sudo git clone https://github.com/phoenix61231/IOT_Sensors

Clone repositories below under the IOT_Sensors folder 

## OLED(optional):

- sudo git clone https://github.com/adafruit/Adafruit_Python_SSD1306

- cd Adafruit_Python_SSD1306

- sudo apt-get install build-essential python-dev python-pip python-imaging python-smbus git

- sudo pip install RPi.GPIO

- sudo python setup.py install

## DHT22:

- sudo git clone https://github.com/adafruit/Adafruit_Python_DHT

- cd Adafruit_Python_DHT

- sudo apt-get install build-essential python-dev

- sudo python setup.py install

## BMP180:

- sudo git clone https://github.com/adafruit/Adafruit_Python_BMP

- cd Adafruit_Python_BMP

- sudo python setup.py install

## Paho:

- pip install paho-mqtt

- git clone https://github.com/eclipse/paho.mqtt.python.git

- cd paho.mqtt.python

- python setup.py install

## Wifi:

- pip install wifi



- connect 0.96 inches OLED module to I2C 0 port(optional)

- connect BMP180 module to I2C 0 port

- connect DHT22 module signal wire to GPIO 4 port

- connect MCP3008 ADC to Pi

- connect TEMT600 module to MCP3008 0

- connect GUVA-S12SD module to MCP3008 1

- connect FC-28 module to MCP3008 2


## Functions

- 1. 開機自動連線已知 Wifi AP

- 2. 開機自動啟動

- 3. Wifi 斷線自動重連

- 4. 使用Network Service Discovery 自動搜尋網域中 Broker (Gateway & Module 連至同一AP)

- 5. 環境感測

- 6. Wifi 連線狀態監控

- 7. 與MQTT Broker 連線狀態監控 (異常存至Local file)

- 8. Log

## Extra

- 1. Power Saving Mode
- 2. 異常數值傳至 warning
