# -*- coding: utf-8 -*-
"""
Application to send and receive informations using mqtt.

@author: Victor
"""
import paho.mqtt.client as mqtt
import json
from time import sleep
import random


def on_connect(client, userdata, flags, rc):
    #This function will be performed by client when a connection is achieved
    global init
    init = 1
    print(f"Connected to {rc}")
    
def on_disconnect(client, userdata, flags):
    print("Disconnected from MQTT Broker")
    
def on_message(client, userdata, msg):
    #This function refers to the response upon receiving a message
    #since it will work in assync mode, this will be called at any moment
    #a message is received
    global msg_val
    topic = msg.topic
    if topic == "config":
        print(msg.payload)
        msg = msg.payload
        msg_val = json.loads(msg.decode('utf-8'))
    elif topic == "alerts":
        print("New alert received!")
    
    
    #on a side note, on_message method doens't return anything to the main app
    #so in order to retrieve some variable, I use a global to get the message 


def send_modbus(phase, size) -> int:
    """A dummy function to send modbus measurement command to power meter
    this function could use a separate file to store addresses and devices"""
    addr = ["C570","C572","C574"]
    device = "01"
    function = "03"
    size = f"{size:04x}"
    crc = "F8D6" # fake crc
    mod_msg = device+function+addr[int(phase)-1]+size+crc
    print(mod_msg)
    #returning a random value just to validate the alerts sent to mqtt broker
    return int(200*random.random())


default_payload = {
    "loadshifting" : False,
    "peakshaving" : 0,
    "charging" : False
}

#Broker address and port used in MQTT, if using MQTTX to monitor, this settings
#should be used there too
broker = "broker.emqx.io"
port = 1883

random.seed(2)# choosing random seed makes sure you get same number sequence

#upon creating an object client, the client_id (mqtt_t) can be anything, 
#just avoid using the same as another existing client in connection

client = mqtt.Client("mqtt_t") 
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.connect(broker,port)
#After connect, if action is succesfull, it will return whatever action defined
#in on_connect method
#subscribing will activate on_message to subbed topics
#decided to use topics: config and alerts
#config is going to be used to send loadshifting, peakshaving and charging info
#alerts will be used to post messages on thresholds exceeded
topics = ["config", "alerts"]

client.subscribe(topics[0])
client.subscribe(topics[1])
      
#loop_start handles automatically the looping to check for messages        
client.loop_start()


measure = 100
threshold = 80
#Here I send the whole dictionary of default payload just to prove that I can
client.publish(topics[0],json.dumps(default_payload))
sleep(1)
try:
    while True:
        #Created a unsofisticated user interface for testing the app
        #You can navigate through options to change stuff or to request cheking
        #the if thresholds have been reached
        option1 = input("What action would you like to perform: \n 1 - Change configuration \n 2 - Check measurement \n")
        if option1 == "1":
            option2 = input("Change which configuration: \n 1 - loadshifting \n 2 - peakshaving \n 3 - charging \n")
            if option2 == "1":
                value = input("Input new value (0 or 1): ")
                client.publish(topics[0],json.dumps({"loadshifting":bool(value)}))
            elif option2 == "2":
                value = input("Input new value: ")
                #notconcerned about value ranges here,but it has to change
                client.publish(topics[0],json.dumps({"peakshaving":int(value)}))
                threshold = int(value)
            elif option2 == "3":
                value = input("Input new value (0 or 1): ")
                client.publish(topics[0],json.dumps({"charging":bool(value)}))
            else:
                print("Invalid option")
        elif option1 == "2":
            option2 = input("Select a phase to measure: \n 1 - P1 \n 2 - P2 \n 3 - P3 \n")
            #in send modbus the number 2 corresponds to the number o bytes you
            #want to read, I left it like this because there is not much 
            #purpose of changing this for simples examples
            measure = send_modbus(option2,2) #a random value will be returned
            #and tested for threshold crossing, if crossed, an alert is sent
            print(f"Current threshold: {threshold}")
            print(f"Current measurement: {measure}")
            if measure > threshold:
                print(f"Threshold exceeded on P{option2}, sending alert")
                client.publish(topics[1],json.dumps({"message":"Power level exceeded"}))
        else:
            print("Invalid option")
        sleep(0.5)

except KeyboardInterrupt:
    print("User Interruption")
    client.loop_stop()
    client.disconnect()
else:
    print("Error Occurred")
    client.loop_stop()
    client.disconnect()