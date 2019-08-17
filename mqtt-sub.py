from simple import MQTTClient
from machine import Pin
import machine
import ubinascii
 
# Setup a GPIO Pin for output
pin = machine.Pin(2, machine.Pin.OUT) 
# Modify below section as required
CONFIG = {
     # Configuration details of the MQTT broker
     "MQTT_BROKER": "192.168.0.24",
     "USER": "",
     "PASSWORD": "",
     "PORT": 1883,
     "TOPIC": b"room/#",
     # unique identifier of the chip
     "CLIENT_ID": b"esp8266_" + ubinascii.hexlify(machine.unique_id())
}
 
# Method to act based on message received   
def onMessage(topic, msg):
    print("Topic: %s, Message: %s" % (topic, msg))
    if topic == b"room/light":
        if msg == b"on":
            pin.off()
            client.publish("raspberry_pi/notification", "success")
        elif msg == b"off":
            pin.on()

    if topic == b"room/fan":
        if msg == b"on":
            pin.off()
            client.publish("raspberry_pi/notification", "success")
        elif msg == b"off":
            pin.on()

  
def listen():
    #Create an instance of MQTTClient 
    # Attach call back handler to be called on receiving messages
    client.set_callback(onMessage)
    client.connect()
    client.publish("raspberry_pi/#", "ESP8266 is Connected:1")
    client.subscribe(CONFIG['TOPIC'])
    print("ESP8266 is Connected to %s and subscribed to %s topic" % (CONFIG['MQTT_BROKER'], str(CONFIG['TOPIC'])))
 
    try:
        while True:
            msg = client.wait_msg()
            #msg = (client.check_msg())
    finally:
        client.publish("raspberry_pi/#","Disconnected:0" )
        client.disconnect()  

client = MQTTClient(CONFIG['CLIENT_ID'], CONFIG['MQTT_BROKER'], user=CONFIG['USER'], password=CONFIG['PASSWORD'], port=CONFIG['PORT'])    
listen()        
