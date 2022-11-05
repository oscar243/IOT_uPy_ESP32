#from http import server
#from tkinter import EXCEPTION

def connect_wifi(ssid,pw):
    from network import WLAN
    from network import STA_IF
    import machine

    wlan = WLAN(STA_IF)
    wlan.active(True)
    
    nets = wlan.scan()
    
    if (wlan.isconnected()):
        wlan.disconnect()
        
    wlan.connect(ssid, pw)

    while not wlan.isconnected():
        machine.idle()
        
    print('Connected:', wlan.ifconfig())


def connect_mqtt():
    from umqtt.simple import MQTTClient

    global mqtt_client

    try:
        with open(KEY_FILE, "r") as f:
            key = f.read()
        print("Go Key")
        
        with open(CERT_FILE, "r") as f:
            cert = f.read()  
        print("Go Cert")

        mqtt_client = MQTTClient(client_id = MQTT_CLIENT_ID, server = MQTT_HOST, port = MQTT_PORT, keepalive=5000, ssl=True, ssl_params={"cert":cert, "key":key, "server_side":False})
        mqtt_client.connect()
        print('MQTT Connected')

    except Exception as e:
        print('cannot connect MQTT:' + str(e))
        raise

def pub_msg(msg):
    global mqtt_client
    try:
        mqtt_client.publish(MQTT_TOPIC, msg)
        print("Sent: " + msg)
    except Exception as e:
        print("Exception publish: " + str(e))
        raise

CERT_FILE = "/flash/cert"
KEY_FILE = "flash/key"
MQTT_CLIENT_ID = "basicPubSub"
MQTT_PORT = 8883
MQTT_TOPIC = "sdk/test/Python"
MQTT_HOST = "a2wcwx5a1jazso-ats.iot.us-east-1.amazonaws.com" #Host/configuraci'on/punto de enlace

import time

try:
    print("Connecting WI-FI")
    connect_wifi("Net","123456780")
    #connect_wifi("SAN MARINO*","VILLABLANCA")
    print("Connecting MQTT")
    connect_mqtt()
    print("Publishing")
    pub_msg("\{AWS-MQTT-8266-01\:" + str(time.time()) + "}")
    print("OK")
except Exception as e:
    print(str(e))


