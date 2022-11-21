"""
Programme qui :
    - reçoit la liste des portières
    - affiche les gamme portière avant, arrière ou attendre prochaine portiere
    - demande à l'opérateur : conforme/non conforme
        - si non conforme : retouché ou rebut
    - envoie un message MQTT avec n° pièce (1 = avant, 2 = arrière) et dit si elle était conforme ou non conforme
"""

from tkinter import *
import paho.mqtt.client as mqtt
from random import randrange, uniform
import time

identifiant = []
liste_portiere = []
heure_entree = []

"""Fonction pour obtenir l'heure"""
def get_time():
    temps = time.localtime()
    date = str(temps[3]) + ":" + str(temps[4]) + ":" + str(temps[5]) + ":" + str(temps[2]) + ":" + str(temps[1]) + ":" + str(temps[0])
    return date


"""Récéption message MQTT de la scanette"""
def on_message(client, userdata, message):
    global identifiant
    global heure_entree
    global liste_portiere
    message = str(message.payload.decode("utf-8"))
    print(str(message))
    a = message.split(";")
    identifiant.append(a[0])
    liste_portiere.append(a[0])
    heure_entree.append(a[1])
    print(liste_portiere)
    # temps_entree = entree[0] * 3600 + entree[1] * 60 + entree[2]
    # heure_debut.append(temps_entree)

mqttBroker = "test.mosquitto.org"
client = mqtt.Client("Controle_qualite")
client.connect(mqttBroker)

client.loop_start()
client.subscribe("ECAM_scanette")
client.on_message = on_message

"""Création de la fenêtre"""

root = Tk()

root.title("Contrôle qualité")
root.geometry('1950x950')
root.iconbitmap("C:/Users/natha/Desktop/ECAM/ECAM/Usine_4.0/Programmes_Python/Main_program/Logo_ECAM_Rennes.ico")

root.columnconfigure(0, weight = 2)
root.columnconfigure(1, weight = 1)

portiere_actuelle = "?"
"""Création des frame"""
#frame = Frame(root)
right_frame= Frame(root)
left_frame = Frame(root)

"""Création d'image"""

def update_image():
    global liste_portiere
    global portiere_actuelle
    if len(liste_portiere) == 0:
        canvas.itemconfig(canvas_image,image=image_attente)
        time.sleep(0.02)
        root.update()
        update_image()
    elif liste_portiere[0][0] == "1":
        portiere_actuelle = liste_portiere[0]
        canvas.itemconfig(canvas_image,image=image_avant)
        root.update()
    elif liste_portiere[0][0] == "2":
        portiere_actuelle = liste_portiere[0]
        canvas.itemconfig(canvas_image,image=image_arriere)
        root.update()

    return None

def conforme():
    global heure_entree
    client.publish("ECAM_qualite", str(liste_portiere[0]) + ";" + str(heure_entree[0]) + ";" + get_time() + ";" + "conforme")
    print(str(liste_portiere[0]) + ";" + str(heure_entree[0]) + ";" + get_time() + ";" + "conforme")
    del liste_portiere[0]
    del heure_entree[0]
    update_image()

def non_conforme():
    global heure_entree
    button_conforme.config(text = "Retouché", command = retouche, bg = "orange")
    button_non_conforme.config(text = "Rebut", command = rebut)
    root.update()

def retouche():
    global heure_entree
    button_conforme.config(text = "Conforme", command = conforme, bg = "green")
    button_non_conforme.config(text = "Non conforme", command = non_conforme)
    client.publish("ECAM_qualite", str(liste_portiere[0]) + ";" + str(heure_entree[0]) + ";" + get_time() + ";" + "retouche")
    print(str(liste_portiere[0]) + ";" + str(heure_entree[0]) + ";" + get_time() + ";" + "retouche")
    del heure_entree[0]
    del liste_portiere[0]
    update_image()

def rebut():
    global heure_entree
    button_conforme.config(text = "Conforme", command = conforme, bg = "green")
    button_non_conforme.config(text = "Non conforme", command = non_conforme)
    client.publish("ECAM_qualite", str(liste_portiere[0]) + ";" + str(heure_entree[0]) + ";" + get_time() + ";" + "rebut")
    print(str(liste_portiere[0]) + ";" + str(heure_entree[0]) + ";" + get_time() + ";" + "rebut")
    del heure_entree[0]
    del liste_portiere[0]
    update_image()


width = 900
height = 900
image_avant = PhotoImage(file= "C:/Users/natha/Desktop/ECAM/ECAM/Usine_4.0/Programmes_Python/Main_program/porte_avant_qualite.png").zoom(16).subsample(10)
image_arriere = PhotoImage(file= "C:/Users/natha/Desktop/ECAM/ECAM/Usine_4.0/Programmes_Python/Main_program/porte_arriere_qualite.png").zoom(16).subsample(10)
image_attente = PhotoImage(file= "C:/Users/natha/Desktop/ECAM/ECAM/Usine_4.0/Programmes_Python/Main_program/attente.png").zoom(10).subsample(10)
canvas = Canvas(left_frame, width = width, height = height,)
canvas_image = canvas.create_image(width/2, height/2, image = image_attente)
canvas.grid(row = 1, column = 0, sticky = W)

label_title = Label(left_frame, text = "Contrôle qualité", font=("Helvetica", 20))
label_title.grid(row = 0, column = 0)


"""Création bouton"""
button_conforme = Button(right_frame, text = "Conforme", font=("Helvetica", 30), width = 15, command = conforme, bg = "green")
button_conforme.grid(row = 1, column = 0, pady = 100, columnspan = 3)

button_non_conforme = Button(right_frame, text = "Non conforme", font=("Helvetica", 30), height = 1, width = 15, bg = "red", command = non_conforme)
button_non_conforme.grid(row = 2, column = 0, pady = 100, columnspan = 3)

button_EPI1 = Button(right_frame, text = "EPI 1", font=("Helvetica", 20), height = 2, width = 5)
button_EPI1.grid(row = 0, column = 0, padx = 100, pady = 30)

button_EPI2 = Button(right_frame, text = "EPI 2", font=("Helvetica", 20), height = 2, width = 5)
button_EPI2.grid(row = 0, column = 1, padx = 100, pady = 30)

button_EPI3 = Button(right_frame, text = "EPI 3", font=("Helvetica", 20), height = 2, width = 5)
button_EPI3.grid(row = 0, column = 2, padx = 100, pady = 30)


left_frame.grid(row = 0, column = 0)
right_frame.grid(row = 0, column = 1, sticky = N)

update_image()
#frame.pack(expand = YES)

root.mainloop()