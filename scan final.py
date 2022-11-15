##objectifs: entrée: code barre / sorties: id portes, heure entrée, avant/arrière
import datetime
import time
import serial
import paho.mqtt.client as mqtt

mqttBroker = "test.mosquitto.org"
client = mqtt.Client("Scanette")
topic_id = "ECAM_scanette"
#topic_heure = "ecamrennes_heure_entree_1"
client.connect(mqttBroker)



#print(time.asctime())
date = time.localtime()
annee = date[0]
mois = date[1]
jour = date[2]
heure = date[3]
minute = date[4]
secondes = date[5]


arduino = serial.Serial(port='COM4', baudrate=9600, timeout=.1)

def porte_avant():
    x="1"
    arduino.write(bytes(x, 'utf-8'))
    data = arduino.readline()
    return data

def porte_arriere():
    x="2"
    arduino.write(bytes(x, 'utf-8'))
    data = arduino.readline()
    return data

def get_time():
    temps = time.localtime()
    date = str(temps[3]) + ":" + str(temps[4]) + ":" + str(temps[5]) + ":" + str(temps[2]) + ":" + str(temps[1]) + ":" + str(temps[0])
    return date

while True:
    idporte = input("scanner une porte")
    heure_entree = get_time()
    message = str(idporte) +";"+str(heure_entree)
    client.publish(topic_id, message)
    print("Just published " + message + " to Topic " + topic_id)

    """Partie Cobot"""
    idporte = str(idporte)
    if idporte[0] == "1":
        porte_avant()
    elif idporte[0] == "2":
        porte_arriere()









