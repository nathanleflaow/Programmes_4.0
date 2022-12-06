from tkinter import *
import paho.mqtt.client as mqtt
from random import randrange, uniform
import time

liste_message = []
var_EPI = 0

"""Fonction pour obtenir l'heure"""
def get_time():
    temps = time.localtime()
    date = str(temps[3]) + ":" + str(temps[4]) + ":" + str(temps[5]) + ":" + str(temps[2]) + ":" + str(temps[1]) + ":" + str(temps[0])
    return date


"""Récéption message MQTT de la scanette"""
def on_message(client, userdata, message):
    global liste_message
    message = str(message.payload.decode("utf-8"))
    print(str(message))
    liste_message.append(message)


mqttBroker = "test.mosquitto.org"
client = mqtt.Client("Coulisse")
client.connect(mqttBroker)

client.loop_start()
client.subscribe("ECAM_LV")
client.on_message = on_message

"""Création de la fenêtre"""

root = Tk()
root.title("Montage coulisse")
root.config(bg='white')
root.geometry("1024x744")

root.columnconfigure(0, weight = 2)
root.columnconfigure(1, weight = 1)

"""Création d'image"""
incrementation = 0
def update_image():
    global incrementation
    global liste_message
    position = [1,1,1,-1,-1,-1]
    while var_EPI!= 1 and len(liste_message) == 0:
        canvas.itemconfigure(point, state='normal')
        canvas.move(point,position[incrementation%6]*50,0)
        time.sleep(0.2)
        incrementation += 1
        canvas.itemconfig(canvas_image,image=image_attente)
        canvas.update()
    if len(liste_message) != 0 and liste_message[0][0] == "1":
        canvas.itemconfigure(point, state='hidden')
        canvas.itemconfig(canvas_image,image=image_avant)
        root.update()
    elif len(liste_message) != 0 and liste_message[0][0] == "2":
        canvas.itemconfigure(point, state='hidden')
        canvas.itemconfig(canvas_image,image=image_arriere)
        root.update()

    return None

def valide():
    global liste_message
    client.publish("ECAM_coulisse", liste_message[0] + ";" + get_time())
    print("Publié : " + liste_message[0] + ";" + get_time())
    del liste_message[0]
    update_image()


width = 650
height = 600
image_avant = PhotoImage(file= "Montage_coulisse_avant.png").zoom(1).subsample(2)
image_arriere = PhotoImage(file= "Montage_coulisse_arriere.png").zoom(1).subsample(2)
image_attente = PhotoImage(file= "attente.png").zoom(1).subsample(2)
image_EPI = PhotoImage(file= "EPI.png").zoom(1).subsample(1)

def retour():
    global var_EPI
    var_EPI = 0
    button_EPI.config(text = "EPI", command = EPI)
    update_image()
def EPI():
    global var_EPI
    var_EPI = 1
    canvas.itemconfigure(point, state='hidden')
    canvas.itemconfig(canvas_image,image=image_EPI)
    button_EPI.config(text = "Retour", command = retour)

"""Canvas image"""
canvas = Canvas(root, width = width, height = height, bg="white", highlightthickness=0)
canvas_image = canvas.create_image(width/2, height/2, image = image_attente)
point = canvas.create_oval(230,450,240,460,fill = "black")
canvas.grid(row = 1, column = 0, sticky = W, padx = 25, rowspan = 2)


# """Logo ECAM Rennes"""
image_logo_ECAM = PhotoImage(file= "Logo_ECAM_Rennes.png").zoom(1).subsample(15)
my_label = Label(root, image = image_logo_ECAM, bg='white')
# my_label.place(x=1, y=500)
my_label.grid(row = 2, column = 1)

label_title = Label(root, text = "Montage coulisse", font=("Helvetica", 15), bg='white', pady = 20)
label_title.grid(row = 0, column = 0)


"""Création bouton"""
button_valide = Button(root, text = "Valider montage", font=("Helvetica", 15), width = 15, command = valide, bg = "#13B94D")
button_valide.grid(row = 1, column = 1, pady = 220)

button_EPI = Button(root, text = "EPI", font=("Helvetica", 10), height = 2, width = 10, command = EPI)
button_EPI.grid(row = 0, column = 1, padx = 10, pady = 21)


update_image()

root.mainloop()
