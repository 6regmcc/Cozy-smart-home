#!/usr/bin/env python
import json
import paho.mqtt.client as mqtt
import time

message_received = "test"

def on_log(client, userdata, level, buf):
    print("log: "+buf)


def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)

def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected resutl code " + str(rc))

def on_message(client, userdata, msg):
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    print("message received", m_decode)
    global message_received
    message_received = m_decode



def update_smart_plug_state(topic, state):
    broker="localhost"
    client=mqtt.Client("gmc_smart_home")
    client.on_connect=on_connect
    client.on_disconnect=on_disconnect
    #client.on_log=on_log
    client.on_message=on_message

    print("Connecting to broker ", broker)

    client.username_pw_set("greg", "szt7359")
    client.connect(broker)
    client.loop_start()
    client.subscribe("zigbee2mqtt/0xa4c138c138a2954d")
    print("this is the message" + message_received)
    client.publish(topic, f'{{"state":"{state}"}}')
    time.sleep(1)
    client.loop_stop()
    client.disconnect()



    






#"zigbee2mqtt/0xa4c138c138a2954d/set"