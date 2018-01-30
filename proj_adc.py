import spidev
import time
import os

def init_adc(x,y):
    spi = spidev.SpiDev()
    spi.open(x, y)
	
    return spi

def read_adc(ch, spi):
    if((ch>7) or (ch<0)):
        return -1
    adc = spi.xfer2([1,(8+ch)<<4,0])
    data = ((adc[1]&3)<<8) + adc[2]
	
    return data

def convert_volts(data, deci):
    volts = ((data*5)/float(1023))*1000.0
    volts = round(volts,deci)
	
    return volts
	
def get_soil(ch, deci, spi):
    data = read_adc(ch, spi)
    volts = convert_volts(data, deci)
    
    #print('Soil Moisture : {0:0.2f} mV'.format(volts))
    	
    return volts

def get_light(ch, deci, spi):
    data = read_adc(ch, spi)
    volts = convert_volts(data, deci)
    
    #print('Light : {0:0.2f} mV'.format(volts))
    	
    return volts

def get_uv(ch, deci, spi):
    data = read_adc(ch, spi)
    volts = convert_volts(data, deci)
   
    #print('UV : {0:0.2f} mV'.format(volts))
    		
    return volts
