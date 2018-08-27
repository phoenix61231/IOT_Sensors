import paho.mqtt.client as mqtt
import thread
from datetime import datetime
import time

def on_message(client, userdata, message):
    print(str(message.payload.decode("utf-8") + " (" + message.topic + ")"))

def on_connect(client, userdata, flags, rc):
    with open('log.txt','a') as file:
        file.write('MQTT connect '+str(datetime.now())+' '+str(rc)+'\n')

def on_disconnect(client, userdata, rc):
    with open('log.txt','a') as file:
        file.write('MQTT disconnect '+str(datetime.now())+' '+str(rc)+'\n')


def init_mqtt(broker_address, instance):
    default_address = "140.116.82.42"
    	
    # Modify the broker ip here, default will be uscclab server	
    if broker_address is None:
	broker_address = default_address	

    # create new instance , change the instance name here to avoid crash
    print("creating new instance")	
    client = mqtt.Client(instance)

    client.on_message = on_message
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
   
    
    print("connecting to broker at " + broker_address)
    client.connect_async(broker_address, keepalive=15)  # connect to broker
    #if connect fail fix

    client.loop_start() # start the loop
    	
    print('----------------------------------------')
	
    return client
