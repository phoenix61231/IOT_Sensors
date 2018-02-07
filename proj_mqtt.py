import paho.mqtt.client as mqtt
import thread


def on_message(client, userdata, message):
    print(str(message.payload.decode("utf-8") + " (" + message.topic + ")"))

def init_mqtt(broker_address, instance, topic):
    default_address = "140.116.82.42"
    default_topic = "mqtt/data"
	
    # Modify the broker ip here, default will be uscclab server	
    if broker_address is None:
	broker_address = default_address	

    # create new instance , change the instance name here to avoid crash
    print("creating new instance")	
    client = mqtt.Client(instance)
    client.on_message = on_message
    
    print("connecting to broker at " + broker_address)
    client.connect_async(broker_address, keepalive=15)  # connect to broker
    #if connect fail fix

    # Enter the topic to subscribe here, web default is "mqtt/demo"
    if topic is None:
	topic = default_topic		

    client.loop_start() # start the loop
    print("Subscribing to topic : " + topic)
    client.subscribe(topic)
	
    print('----------------------------------------')
	
    return client
