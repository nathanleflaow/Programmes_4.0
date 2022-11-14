import paho.mqtt.client as mqtt
from random import randrange, uniform, randint
import time

def heure_simulation(min_debut):
    heure_entree = str(min_debut//60) + (":") + str(min_debut%60) + (":00")
    min_debut += 1
    print(heure_entree)
    heure_M1 = str(min_debut//60) + (":") + str(min_debut%60) + (":00")
    min_debut += 1
    print(heure_M1)
    heure_M2 = str(min_debut//60) + (":") + str(min_debut%60) + (":00")
    print(heure_M2)

#print(time.asctime())
date = time.localtime()
annee = date[0]
mois = date[1]
jour = date[2]
heure = date[3]
minute = date[4]
secondes = date[5]

mqttBroker = "test.mosquitto.org"
client = mqtt.Client("Scanette_NLF")
client.connect(mqttBroker)

def get_time():
    temps = time.localtime()
    date = str(temps[3]) + ":" + str(temps[4]) + ":" + str(temps[5]) + ":" + str(temps[2]) + ":" + str(temps[1]) + ":" + str(temps[0])
    return date
heure_debut = get_time()

while True:
    text = ""
    text += str(randint(1, 2))
    text += str(randint(0, 9))
    text += str(randint(0, 9))
    text += str(randint(0, 9))
    text += str(randint(0, 9))

    #randNumber = randint(1, 2)
    #start = time.time()
    time.sleep(randint(5,6))
    #stop = time.time()
    #delta_t = stop - start
    heure_entree = get_time()
    message = str(text) + ";" + str(heure_entree)
    client.publish("ECAM_scanette_NLF", message)
    print(str(message))