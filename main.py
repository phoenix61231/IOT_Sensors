import time
import subprocess

from datetime import datetime

import proj_sensors
import proj_oled
import proj_mqtt
import proj_adc

ip_address = "140.116.82.42"
instance = "module_001"
topic_data = "mqtt/data"


client = proj_mqtt.init_mqtt(ip_address, instance, topic_data)
spi = proj_adc.init_adc(0, 0)
#RST = proj_oled.init_connect()
#font, font2, font_icon_big, font_text_big = proj_oled.load_font()

#disp = proj_oled.init_disp(RST)
#width, height = proj_oled.def_size(disp)
#x, top = proj_oled.draw_shape(height)
#image, draw = proj_oled.create_blank(width, height)


while True:
    humidity_value, temperature_value = proj_sensors.get_dht22('4')	
    pressure_value = proj_sensors.get_bmp180()
	
    light_value = proj_adc.get_light(0, 2, spi)
    uv_value = proj_adc.get_uv(1, 2, spi)
    soil_value = proj_adc.get_soil(2, 2, spi)
	
    """# Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)"""

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1 | head --bytes -1"
    IP = subprocess.check_output(cmd, shell = True )
    cmd = "top -bn1 | grep load | awk '{printf \"%.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell = True )
    cmd = "free -m | awk 'NR==2{printf \"MEM: %.2f%%\", $3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True )
	
    temperature = ' / Temperature:{0:0.1f} '.format(temperature_value)
    humidity = '/ Humidity:{0:0.1f} '.format(humidity_value)
    light = '/ Light:{0:0.2f} '.format(light_value)
    uv = '/ UV:{0:0.2f} '.format(uv_value)
    soil = '/ Soil:{0:0.2f} '.format(soil_value)
    pressure = '/ Air Pressure:{0:0.3f} '.format(pressure_value/1000.0)
    
    data_time = str(datetime.now())    
    print(data_time + '\n')

    line_data = instance + ' / ' + IP + temperature + humidity + light + uv + soil + pressure + '/ Time:' + data_time
	
    line_state = instance + ' / ' + IP + ' / CPU:' + CPU + ' / ' + MemUsage + ' / ' + data_time
 
    client.publish(topic_data, line_data)
		
    """# Icons
    draw.text((x, top),       unichr(61931),  font=font2, fill=255) #wifi icon
    draw.text((x, top+15),    unichr(62171),  font=font_icon_big, fill=255) #cpu icon
	
    draw.text((18, top),      str(IP),  font=font, fill=255) 
    draw.text((x+22, top+12), str(CPU), font=font_text_big, fill=255) 
    draw.text((x, top+36),    str(MemUsage),  font=font, fill=255)	
	
    # Display image.
    disp.image(image)
    disp.display()"""
	
    print "----------------------------------------"
    time.sleep(3)
