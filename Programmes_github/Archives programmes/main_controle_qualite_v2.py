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

mqttBroker = "test.mosquitto.org"
client = mqtt.Client("Usine_4.0")
client.connect(mqttBroker)

"""Création de la fenêtre"""

root = Tk()

root.title("Contrôle qualité")
root.geometry('1950x950')
root.iconbitmap("C:/Users/natha/Desktop/ECAM/ECAM/Usine_4.0/Programmes_Python/Main_program/Logo_ECAM_Rennes.ico")

root.columnconfigure(0, weight = 2)
root.columnconfigure(1, weight = 1)

liste_portiere = ["1", "2", "1", "2"]
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
        time.sleep(1)
        root.update()
    elif liste_portiere[0] == "1":
        portiere_actuelle = "1"
        canvas.itemconfig(canvas_image,image=image_avant)
        root.update()
        del liste_portiere[0]
    elif liste_portiere[0] == "2":
        portiere_actuelle = "2"
        canvas.itemconfig(canvas_image,image=image_arriere)
        root.update()
        del liste_portiere[0]
    return None

def conforme():
    update_image()
    client.publish("ECAM_porte", portiere_actuelle + " conforme")
    print(portiere_actuelle + " conforme")

def non_conforme():
    button_conforme.config(text = "Retouché", command = retouche, bg = "orange")
    button_non_conforme.config(text = "Rebut", command = rebut)
    root.update()

def retouche():
    update_image()
    button_conforme.config(text = "Conforme", command = update_image, bg = "green")
    button_non_conforme.config(text = "Non conforme", command = non_conforme)
    client.publish("ECAM_porte", portiere_actuelle + " retouché")
    print(portiere_actuelle + " retouché")
    root.update()

def rebut():
    update_image()
    button_conforme.config(text = "Conforme", command = update_image, bg = "green")
    button_non_conforme.config(text = "Non conforme", command = non_conforme)
    client.publish("ECAM_porte", portiere_actuelle + " rebut")
    print(portiere_actuelle + " rebut")
    root.update()


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