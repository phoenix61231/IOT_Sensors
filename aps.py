import time
import subprocess
import sys

from datetime import datetime
from threading import Thread
from threading import Timer

from apscheduler.schedulers.blocking import BlockingScheduler

from wifi import Cell

import proj_sensors
import proj_oled
import proj_mqtt
import proj_adc

import logging

#the mqtt client setting
def avahi_broswer(service):
    output = subprocess.check_output('avahi-browse -r -t %s' % service,shell=True)
    list_out = output.split("\n")
    address = list_out[3].split(" = ")
    ip_tmp = address[1].split("[")
    ip = ip_tmp[1].split("]")
    return ip[0]


ip_address = avahi_broswer('_mosquitto._tcp')
instance = "module_001"
gateway_name = "gateway_001"

topic_data = "uscclab/"+ gateway_name +"/"+ instance +"/data"
topic_status = "uscclab/"+ gateway_name +"/"+ instance +"/status"
topic_warning = "uscclab/"+ gateway_name +"/"+ instance +"/warning"


#Initital the mqtt client
client = proj_mqtt.init_mqtt(ip_address, instance)
client.subscribe(topic_data)
client.subscribe(topic_status)
client.subscribe(topic_warning)

#Decline the global variable
humidity_value = 0.0
temperature_value = 0.0
pressure_value = 0.0
light_value = 0.0
uv_value = 0.0
soil_value = 0.0

data_time = ''
status_time = ''

IP = ''
CPU = ''
MemUsage = ''

wifi_signal = ''
wifi_quality = ''

scheduler = BlockingScheduler()
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',datafmt='%a, %d %b %Y %H:%M:%S', filename='/var/log/aps_logging.txt', filemode='a')


#define the data thread
#for initial and getting data
def data_thread():
    global data_time
    global humidity_value, temperature_value, pressure_value
    global light_value, uv_value, soil_value
	
    spi = proj_adc.init_adc(0, 0)
    
    humidity_value, temperature_value = proj_sensors.get_dht22('4')	
    pressure_value = proj_sensors.get_bmp180()

    light_value = proj_adc.get_light(0, 2, spi)
    uv_value = proj_adc.get_uv(1, 2, spi)
    soil_value = proj_adc.get_soil(2, 2, spi)
    #soil_value = 3000
	
    data_time = str(datetime.now())
    print(data_time)
    print("--------------------")


#define the status thread
#for initial and getting status
def status_thread():
    global IP, CPU, MemUsage, status_time

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1 | head --bytes -1"
    IP = subprocess.check_output(cmd, shell = True )
    cmd = "top -bn1 | grep load | awk '{printf \"%.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell = True )
    cmd = "free -m | awk 'NR==2{printf \"MEM: %.2f%%\", $3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True )

    status_time = str(datetime.now())
	

#define the oled display thread
#for initial and oled display
"""def oled_thread():
    global IP, CPU, MemUsage

    RST = proj_oled.init_connect()
    font, font2, font_icon_big, font_text_big = proj_oled.load_font()

    disp = proj_oled.init_disp(RST)
    width, height = proj_oled.def_size(disp)
    x, top = proj_oled.draw_shape(height)
    image, draw = proj_oled.create_blank(width, height)        

    while True:
        # Draw a black filled box to clear the image.
        draw.rectangle((0,0,width,height), outline=0, fill=0)
	
        # Icons
        draw.text((x, top),       unichr(61931),  font=font2, fill=255) #wifi icon
        draw.text((x, top+15),    unichr(62171),  font=font_icon_big, fill=255) 
        #cpu icon
	
        draw.text((18, top),      str(IP),  font=font, fill=255) 
        draw.text((x+22, top+12), str(CPU), font=font_text_big, fill=255) 
        draw.text((x, top+36),    str(MemUsage),  font=font, fill=255)	
	
        # Display image.
        disp.image(image)
        disp.display()"""

#define send data thread
#for the sending data operation with publish error detect
def send_data_thread():
    global temperature_value, humidity_value, pressure_value
    global light_value, uv_value, soil_value
    global client, instance, topic_data, data_time, IP, gateway_name

    temperature = ' / Temperature:{0:0.1f} '.format(temperature_value)
    humidity = '/ Humidity:{0:0.1f} '.format(humidity_value)
    light = '/ Light:{0:0.2f} '.format(light_value)
    uv = '/ UV:{0:0.2f} '.format(uv_value)
    soil = '/ Soil:{0:0.2f} '.format(soil_value)
    pressure = '/ Air Pressure:{0:0.3f} '.format(pressure_value/1000.0)    

    line_data = gateway_name + ' / ' + instance + ' / ' + IP + temperature + humidity + light + uv + soil + pressure + '/ Time:' + data_time
	
    info = client.publish(topic_data, line_data)

    if info.rc is not 0:
        #save to .txt
        with open('data.txt', 'a') as file:
            file.write(line_data + '\n')
            
        with open('log.txt', 'a') as file:
            file.write('Publish error (data) Saved. '+str(datetime.now())+'\n')
    else:
        with open('log.txt', 'a') as file:
            file.write('Publish success (data) '+str(datetime.now())+'\n')
            

#define send status thread
#for the sending data operation with publish error detect
def send_status_thread():
    global status_time, topic_status, client
    global IP, CPU, MemUsage, instance, gateway_name

    line_status = gateway_name + ' / ' + instance + ' / ' + IP + ' / CPU:' + CPU + ' / ' + MemUsage + ' / ' + wifi_signal + ' / ' + str(wifi_quality) + ' / ' +status_time
    info = client.publish(topic_status, line_status)        

    if info.rc is not 0:
        #save to .txt
        with open('status.txt', 'a') as file:
            file.write(line_status + '\n')

        with open('log.txt','a') as file:
            file.write('Publish error (status) Saved '+str(datetime.now())+'\n')    
    else:
        with open('log.txt','a') as file:
            file.write('Publish success (status) '+str(datetime.now())+'\n')

#define wifi connection detect thread
#for the wifi connection signal and quality detect
def wifi_connection_detect_thread():	
    global wifi_quality, wifi_signal

    #wifi signal & quality
    cell = Cell.all('wlan0')[0]

    if cell is not None:
	wifi_signal = str(cell.signal) + ' dBm'
        
        quality = cell.quality
        front = float(quality[1]) + 10.0*float(quality[0])
        rear = float(quality[4]) + 10.0*float(quality[3]) 
        wifi_quality = '{0:0.2f} %'.format(100.0*(front/rear))
    else:
        wifi_signal = 'Wifi Connection Fail'
        wifi_quality = 'Wifi Connection Fail'


scheduler.add_job(data_thread, 'interval', seconds=15)
scheduler.add_job(status_thread, 'interval', seconds=15)

scheduler.add_job(send_data_thread, 'interval', seconds=60)
scheduler.add_job(send_status_thread, 'interval', seconds=60)

scheduler.add_job(wifi_connection_detect_thread, 'interval', seconds=5)

scheduler.start()

#oled_t = Thread(target=oled_thread, name="oled_t")
#oled_t.start()

