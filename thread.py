import time
import subprocess

from datetime import datetime
from threading import Thread
from threading import Timer

from wifi import Cell

import proj_sensors
import proj_oled
import proj_mqtt
import proj_adc

#the mqtt client setting
ip_address = "172.20.10.8"
instance_data = "module_001_data"
instance_status = "module_001_status"
topic_data = "mqtt/data"
topic_status = "mqtt/status"

#Initital the mqtt client
client_data = proj_mqtt.init_mqtt(ip_address, instance_data, topic_data)
client_status = proj_mqtt.init_mqtt(ip_address, instance_status, topic_status)

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

#define the data thread
#for initial and getting data
def data_thread():
    global data_time
    global humidity_value, temperature_value, pressure_value
    global light_value, uv_value, soil_value
	
    spi = proj_adc.init_adc(0, 0)
    
    while True:
        humidity_value, temperature_value = proj_sensors.get_dht22('4')	
        pressure_value = proj_sensors.get_bmp180()

        light_value = proj_adc.get_light(0, 2, spi)
        uv_value = proj_adc.get_uv(1, 2, spi)
        soil_value = proj_adc.get_soil(2, 2, spi)
	
        data_time = str(datetime.now())
        print(data_time)
        print("--------------------")
        time.sleep(10)

#define the status thread
#for initial and getting status
def status_thread():
    global IP, CPU, MemUsage, status_time

    while True:
        # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
        cmd = "hostname -I | cut -d\' \' -f1 | head --bytes -1"
        IP = subprocess.check_output(cmd, shell = True )
        cmd = "top -bn1 | grep load | awk '{printf \"%.2f\", $(NF-2)}'"
        CPU = subprocess.check_output(cmd, shell = True )
        cmd = "free -m | awk 'NR==2{printf \"MEM: %.2f%%\", $3*100/$2 }'"
        MemUsage = subprocess.check_output(cmd, shell = True )

        status_time = str(datetime.now())
        time.sleep(5)
	

#define the oled display thread
#for initial and oled display
def oled_thread():
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
        disp.display()

#define send data thread
#for the sending data operation with publish error detect
def send_data_thread():
    global temperature_value, humidity_value, pressure_value
    global light_value, uv_value, soil_value
    global client_data, instance_data, topic_data, data_time, IP

    while True:
        time.sleep(10) #fix to 60
        temperature = ' / Temperature:{0:0.1f} '.format(temperature_value)
        humidity = '/ Humidity:{0:0.1f} '.format(humidity_value)
        light = '/ Light:{0:0.2f} '.format(light_value)
        uv = '/ UV:{0:0.2f} '.format(uv_value)
        soil = '/ Soil:{0:0.2f} '.format(soil_value)
        pressure = '/ Air Pressure:{0:0.3f} '.format(pressure_value/1000.0)    

        line_data = instance_data + ' / ' + IP + temperature + humidity + light + uv + soil + pressure + '/ Time:' + data_time
	
        info = client_data.publish(topic_data, line_data)

        if info.rc is not 0:
            #save to .txt
            with open('data.txt', 'a') as file:
                file.write(line_data + '\n')
                print("Save to data.txt file.")
                print("--------------------")
            

#define send status thread
#for the sending data operation with publish error detect
def send_status_thread():
    global status_time, topic_status, client_status
    global IP, CPU, MemUsage, instance_status

    while True:
        time.sleep(10) #fix to 30
        line_status = instance_status + ' / ' + IP + ' / CPU:' + CPU + ' / ' + MemUsage + ' / ' + wifi_signal + ' / ' + str(wifi_quality) + ' / ' +status_time
        info = client_status.publish(topic_status, line_status)
        
        if info.rc is not 0:
            #save to .txt
            with open('status.txt', 'a') as file:
                file.write(line_status + '\n')
                print("Save to status.txt file.")
                print("--------------------")
            

#define wifi connection detect thread
#for the wifi connection signal and quality detect
def wifi_connection_detect_thread():
	
    global wifi_quality, wifi_signal

    while True:
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

	time.sleep(5)	

data_t = Thread(target=data_thread, name="data_t")
data_t.start()

status_t = Thread(target=status_thread, name="status_t")
status_t.start()

#oled_t = Thread(target=oled_thread, name="oled_t")
#oled_t.start()

send_data_t = Thread(target=send_data_thread, name="send_data_t")
send_data_t.start()

send_status_t = Thread(target=send_status_thread, name="send_status_t")
send_status_t.start()

wifi_connection_detect_t = Thread(target=wifi_connection_detect_thread, name="connection_detect_t")
wifi_connection_detect_t.start()

