import Adafruit_DHT
import Adafruit_BMP.BMP085 as BMP085

def get_dht22(pin):
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, pin)

    """if humidity is not None and temperature is not None:
        print('Temperature : {0:0.1f}*C\nHumidity : {1:0.1f}%'.format(temperature,humidity))
    else:
        print('.')"""
    return humidity, temperature
	
def get_bmp180():
    bmp180 = BMP085.BMP085()
    pressure = bmp180.read_pressure()
    #print "Air Pressure : {0:0.3f} kPa".format(pressure/1000.0)
	
    return pressure
