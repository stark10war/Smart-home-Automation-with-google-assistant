
import paho.mqtt.client as mqtt
import time


broker_address = '192.168.0.24'
client = mqtt.Client('publisher')


print('connecting to broker '+ broker_address)
client.connect(broker_address)
client.publish("room/fan", "off")
