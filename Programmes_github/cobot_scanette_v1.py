import serial
import time
import paho.mqtt.client as mqtt

def on_message(client, userdata, message):
    message = str(message.payload.decode("utf-8"))
    a = message.split(";")
    if a[0][0] == 1 :
        porte_avant()
    elif a[0][0] == 2 :
        porte_arriere()

mqttBroker = "test.mosquitto.org"
client = mqtt.Client("Cobot")
client.connect(mqttBroker)

client.loop_start()
client.subscribe("ECAM_scanette")
client.on_message = on_message

def porte_avant():
    arduinoData = serial.Serial("com3", 9600)
    arduinoData.write(1)
    arduinoData.close()

def porte_arriere():
    arduinoData = serial.Serial("com3", 9600)
    arduinoData.write(2)
    arduinoData.close()


