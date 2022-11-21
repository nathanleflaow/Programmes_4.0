from tkinter import *
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import paho.mqtt.client as mqtt
import time

"""Reste à faire :
    - Changer les couleurs en fonction de l'objectif
    -
"""

duree_run = 1 #durée du run en min
taux_defaut_accepte = 0.1

objectif_portes = 0
portes_realisees_avant = 0
portes_realisees_arriere = 0
portes_realisees = portes_realisees_avant + portes_realisees_arriere
defauts_constates = 0
defauts_toleres = 0

# Hauteur du canevas
lg=300
# Largeur du bord
ht=100
# Largeur de la zone de focus
bw=50

zf=7

t1 = []
y1 = []
t2 = []
y2 = []

for i in range (0,57):
    x = i*0.5
    y1.append(x)
    t1.append(i)


for j in range(0,50):
    t2.append(j)
    y2.append(j)

temps = []
temps_total = [0]
id_porte = []
y_nombre_porte = [0]


L = []

"""Reception des messages MQTT"""
def on_message(client, userdata, message):
    global portes_realisees_avant
    global portes_realisees_arriere
    global portes_realisees
    message = str(message.payload.decode("utf-8"))
    print(message)
    """Il faut réfléchir à la façon dont on envoie le message. Mettre au début numéro avant ou arriere (1 ou 2), delta_t puis 1 = conforme, 2 = retouche, 3 = rebut"""
    a = message.split(";")
    identifiant_porte = a[0]
    if identifiant_porte == "1":
        print("avant =" + str(portes_realisees_avant))
        portes_realisees_avant += 1
    if identifiant_porte == "2":
        print("arriere" + str(portes_realisees_arriere))
        portes_realisees_arriere += 1
    portes_realisees = portes_realisees_avant + portes_realisees_arriere
    id_porte.append(identifiant_porte)
    delta_t = a[1]
    delta_t = float(delta_t)
    temps.append(delta_t)
    nombre_porte = len(id_porte)
    y_nombre_porte.append(nombre_porte)
    temps_total.append(temps_total[-1] + temps[-1])
    print("delta_t = " + str(temps) + "; id porte = " + str(id_porte))
    print("temps total = " + str(temps_total) + "; nombre portes = " + str(y_nombre_porte))


mqttBroker = "test.mosquitto.org"
client = mqtt.Client("Smartphone")
client.connect(mqttBroker)
client.loop_start()
client.subscribe("ECAM_porte")
client.on_message = on_message

"""Création de la fenêtre"""
root = Tk()
root.title("Suivi de production")
root.geometry('1950x950')

"""Entrée des données"""
lalbel_entrer_obj_porte = Label(root, text = "Objectif de portes total : ", font=("Helvetica", 20))
lalbel_entrer_obj_porte.grid(row= 0, column = 0)
objectif_portes_entry = Entry(root, width = 5)
objectif_portes_entry.grid(row= 0, column = 0, sticky = E)

"""Affichage des KPI"""
#Portes réalisées
label_porte_realisees = Label(root, text = "Portes réalisées : ", font=("Helvetica", 20)).grid(row=1, column=2)
canva1=Canvas(root, bg="ivory", width=lg,
        height=ht, bd=bw,highlightthickness=zf,
        highlightbackground="black")
canva1.grid(row=2, column=2)
text_canva1 = canva1.create_text(200, 100, text = portes_realisees, font=("Helvetica", 35))

#Objectif portes
label_objectif_portes = Label(root, text = "Objectif portes : ", font=("Helvetica", 20)).grid(row=1, column=3)
canva2=Canvas(root, bg="ivory", width=lg,
        height=ht, bd=bw,highlightthickness=zf,
        highlightbackground="black")
canva2.grid(row=2, column=3)
text_canva2 = canva2.create_text(200, 100, text = objectif_portes, font=("Helvetica", 35))

#Portes avant réalisées
label_portes_avant = Label(root, text = "Portes avant : ", font=("Helvetica", 20)).grid(row=3, column=2)
canva3=Canvas(root, bg="ivory", width=lg,
        height=ht, bd=bw,highlightthickness=zf,
        highlightbackground="black")
canva3.grid(row=4, column=2)
text_canva3 = canva3.create_text(200, 100, text = portes_realisees_avant, font=("Helvetica", 35))

#Portes arrières réalisées
label_portes_arrieres = Label(root, text = "Portes arrière : ", font=("Helvetica", 20)).grid(row=3, column=3)
canva4=Canvas(root, bg="ivory", width=lg,
        height=ht, bd=bw,highlightthickness=zf,
        highlightbackground="black")
canva4.grid(row=4, column=3)
text_canva4 = canva4.create_text(200, 100, text = portes_realisees_arriere, font=("Helvetica", 35))

#Défauts constatés
label_defauts_constates = Label(root, text = "Défauts constatés : ", font=("Helvetica", 20)).grid(row=5, column=2)
canva5=Canvas(root, bg="ivory", width=lg,
        height=ht, bd=bw,highlightthickness=zf,
        highlightbackground="black")
canva5.grid(row=6, column=2)
text_canva5 = canva5.create_text(200, 100, text = defauts_constates, font=("Helvetica", 35))

#Défauts tolérés
label_defauts_toleres = Label(root, text = "Défauts tolérés : ", font=("Helvetica", 20)).grid(row=5, column=3)
canva6=Canvas(root, bg="ivory", width=lg,
        height=ht, bd=bw,highlightthickness=zf,
        highlightbackground="black")
canva6.grid(row=6, column=3)
text_canva6 = canva6.create_text(200, 100, text = defauts_toleres, font=("Helvetica", 35))

"""Tracé du graphique"""
def plot_values():
    figure = plt.figure(figsize = (5,4), dpi = 100) ##figsize = dimensions graphique
    chart = FigureCanvasTkAgg(figure, root)
    chart.get_tk_widget().grid(row = 2, column = 0, rowspan = 100, columnspan = 2)
    figure.add_subplot(111).plot(t1,y1)
    figure.add_subplot(111).plot(temps_total,y_nombre_porte)
    plt.grid()
    plt.xlabel("temps (min)")
    plt.ylabel("nombre de portières produites")
    plt.xlim([0, 60])
    plt.ylim([0,30])

plot_values()

def update_values():
    plot_values()
    return None

"""Lance le programme lorsque l'on appui sur le bouton lancer le run"""
def go():
    objectif_porte = str(objectif_portes_entry.get())
    canva2.itemconfig(text_canva2, text = objectif_porte)
    defauts_toleres = int(int(objectif_porte) * taux_defaut_accepte)

    for i in range(duree_run * 60):
        canva1.itemconfig(text_canva1, text = portes_realisees)
        canva3.itemconfig(text_canva3, text = portes_realisees_avant)
        canva4.itemconfig(text_canva4, text = portes_realisees_arriere)
        canva6.itemconfig(text_canva6, text = defauts_toleres)
        update_values()
        root.update()
        time.sleep(1)

"""Création bouton"""
#button_start = Button(root, text="Lancer le run", command = update_values) ##création boutton
button_start = Button(root, text="Lancer le run", command = go) ##création boutton
button_start.grid(row=1, column=0) ##placement dans la fenêtre
root.bind("<Return>", update_values)
#plot_values() ##mise à jour du graphique



root.mainloop()










