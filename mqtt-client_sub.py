import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    if rc==0:
        print(str(rc)+': successfully connected to broker!')
        client.subscribe("test")
        client.subscribe("raspberry_pi")
        print("subscribed to home/room1/#")
    else:
        print("bad connection, rc:" + str(rc))

def on_message(client, userdata, msg):
    
    payload = msg.payload.decode("utf-8")
    
    if msg.topic == "home/room1/light":
        handle_light(payload=payload)
    
    if msg.topic == "home/room1/fan":
        handle_fan(payload=payload)
    

    if msg.topic == "test":
        print(payload == 'success')
        print('topic: '+ str(msg.topic) +' , message: '+ payload)
    
    
    if msg.topic == "raspberry_pi":
        print(payload == 'success')
        print('topic: '+ str(msg.topic) +' , message: '+ payload)
    


def on_log(client, userdata, level, buf):
    print('log: '+buf)


def on_disconnect(client, userdata, flags, rc=0):
    print('Disconnected Returned code'+ str(rc))



def handle_light(payload):
    
    if payload == "on":
        print("room1 Light: ON")
        client.publish("notification" ,"success")
        
    elif payload == "off":
        print("room1 Light: OFF")
        client.publish("notification", "success")
        
    else:
        print("bad Input recieved..")
        client.publish("notification", "failed")


def handle_fan(payload):

    if payload == "on":
        print("room1 fan: ON")
        client.publish("notification" ,"success")

    elif payload == "off":
        print("room1 fan: OFF")
        client.publish("notification", "success")
        
    else:
        print("bad Input recieved..")
        client.publish("notification", "failed")
 
    



broker_address = '192.168.0.24'
client = mqtt.Client('subscriber')

client.on_connect = on_connect
client.on_message = on_message
client.on_log = on_log
client.on_disconnect = on_disconnect


print('connecting to broker'+ broker_address)
client.connect(broker_address)
client.loop_forever()







