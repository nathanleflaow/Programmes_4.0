from tkinter import *
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import paho.mqtt.client as mqtt
import time
import xlsxwriter

"""Reste à faire :
    - Changer les couleurs en fonction de l'objectif
    - Recalibrer graphique, courbes pour passer le temps de seconde à minutes
"""

"""création feuille excel"""
workbook = xlsxwriter.Workbook('C:/Users/natha/Desktop/ECAM/ECAM/Usine_4.0/Programmes_Python/Main_program/tracabilite.xlsx')
sheet = workbook.add_worksheet()

#initialisation nom colonne
sheet.write(0, 0, 'ID') #nom colonne write(ligne, colonne, "texte")
sheet.write(0, 1, 'date')
sheet.write(0, 2, 'heure entrée')
sheet.write(0, 3, 'heure M1')
sheet.write(0, 4, 'heure M2')
sheet.write(0, 5, 'heure sortie')
sheet.write(0, 6, 'conformité')

#initialisation de la ligne = numero de la porte
numero_porte = 1

#garder uniquement la date dans heure:minutes:seconde:jour:mois:annee
def date(heure):
    date = heure.split(":")
    return str(date[3]+"/"+date[4]+"/"+date[5])

#garder uniquement l'heure dans heure:minutes:seconde:jour:mois:annee
def heure(heure):
    heure_split = heure.split(":")
    return str(heure_split[0]+":"+heure_split[1]+":"+heure_split[2])

#écrire dans le tableau excel les données correspondantes
def tracabilite(message_split):
    global numero_porte
    id = message_split[0]
    date_entree = date(message_split[1])
    heure_entree = heure(message_split[1])
    heure_m1 = heure(message_split[2])
    heure_m2 = heure(message_split[3])
    heure_sortie = heure(message_split[4])
    conformite = message_split[5]

    sheet.write(numero_porte,0, id)
    sheet.write(numero_porte,1, date_entree)
    sheet.write(numero_porte,2, heure_entree)
    sheet.write(numero_porte,3, heure_m1)
    sheet.write(numero_porte,4, heure_m2)
    sheet.write(numero_porte,5, heure_sortie)
    sheet.write(numero_porte,6, conformite)

    numero_porte += 1

"""Paramètres à modifier pour le run"""
duree_run = 1 #durée du run en min
objectif_qualite = "90%"

"""déclaration de variables"""
objectif_portes = 0
portes_realisees_avant = 0
portes_realisees_arriere = 0
retouches_avant = 0
retouches_arriere = 0
rebut_avant = 0
rebut_arriere = 0
defauts_toleres = 0
taux_qualite = 0
X_temps_retouches = []
X_temps_rebuts = []
Y_retouches = []
Y_rebuts = []
portes_realisees = portes_realisees_avant + portes_realisees_arriere


# Hauteur du canevas
lg=300
# Largeur du bord
ht=100
# Largeur de la zone de focus
bw=50

zf=7

t1 = []
y1 = []

for i in range (0,57):
    x = i*0.5
    y1.append(x)
    t1.append(i)

X_temps = [0]
Y_prod = [0]
liste_messages = [] #stock les messages reçus


L = []
"""Fonction qui convertit l'heure du message en secondes"""
def conversion_heure_sec(heure):
    heure = heure.split(":")
    heure_en_sec = heure[0]*3600 + heure[1]*60 + heure[0]
    return heure_en_sec

"""Reception des messages MQTT"""
def on_message(client, userdata, message):
    global portes_realisees_avant
    global portes_realisees_arriere
    global portes_realisees
    global liste_messages
    global X_temps
    global Y_prod
    global retouches_avant
    global retouches_arriere
    global rebut_avant
    global rebut_arriere
    global taux_qualite
    global X_temps_retouches
    global X_temps_rebuts
    global Y_retouches
    global Y_rebuts
    message = str(message.payload.decode("utf-8"))
    tracabilite(message.split(";"))
    liste_messages.append(message)
    print(message)
    """Il faut réfléchir à la façon dont on envoie le message. Mettre au début numéro avant ou arriere (1 ou 2), delta_t puis 1 = conforme, 2 = retouche, 3 = rebut"""
    a = message.split(";")
    identifiant_porte = a[0]
    conformite = a[-1]
    if identifiant_porte[0] == 1 and conformite == "conforme": #avant conforme
        portes_realisees_avant += 1
        root.update()
    if identifiant_porte[0] == 2 and conformite == "conforme": #arriere conforme
        portes_realisees_arriere += 1
        root.update()
    if identifiant_porte[0] == 1 and conformite == "retouche": #avant retouché
        portes_realisees_arriere += 1
        retouches_avant += 1
        Y_retouches.append(portes_realisees + 1)
        X_temps_retouches.append(conversion_heure_sec(a[-2]) - conversion_heure_sec(a[1]))
        root.update()
    if identifiant_porte[0] == 2 and conformite == "retouche": #arriere retouche
        portes_realisees_arriere += 1
        retouches_arriere += 1
        Y_retouches.append(portes_realisees + 1)
        X_temps_retouches.append(conversion_heure_sec(a[-2]) - conversion_heure_sec(a[1]))
        root.update()
    if identifiant_porte[0] == 1 and conformite == "rebut": #avant_rebut
        rebut_avant += 1
        Y_rebuts.append(portes_realisees)
        X_temps_rebuts.append(conversion_heure_sec(a[-2]) - conversion_heure_sec(a[1]))
        root.update()
    if identifiant_porte[0] == 2 and conformite == "rebut": #arriere_rebut
        rebut_arriere += 1
        Y_rebuts.append(portes_realisees)
        X_temps_rebuts.append(conversion_heure_sec(a[-2]) - conversion_heure_sec(a[1]))
        root.update()
    portes_realisees = portes_realisees_avant + portes_realisees_arriere
    taux_qualite = (portes_realisees - retouche_avant - retouche_arriere)/(portes_realisees - rebut_avant - rebut_arriere)

    X_temps.append(conversion_heure_sec(a[-2]) - conversion_heure_sec(a[1]))
    Y_prod.append(portes_realisees)


mqttBroker = "test.mosquitto.org"
client = mqtt.Client("Affichage_prod")
client.connect(mqttBroker)
client.loop_start()
client.subscribe("ECAM_qualite")
client.on_message = on_message

"""Création de la fenêtre"""
root = Tk()
root.title("Suivi de production")
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight())) #affiche en mode fullscreen
root.configure(bg = '#7F8FA6')

"""Entrée des données"""
lalbel_entrer_obj_porte = Label(root, text = "Objectif de portes total : ", font=("Helvetica", 20), bg = '#7F8FA6')
lalbel_entrer_obj_porte.grid(row= 0, column = 0)
objectif_portes_entry = Entry(root, width = 10, bg = '#7F8FA6')
objectif_portes_entry.grid(row= 0, column = 0, sticky = E)

"""Affichage des KPI"""
#Portes réalisées
label_porte_realisees = Label(root, text = "Portes réalisées : ", font=("Helvetica", 20), bg = '#7F8FA6').grid(row=1, column=2)
canva1=Canvas(root, bg="ivory", width=lg,
        height=ht, bd=bw,highlightthickness=zf,
        highlightbackground="black")
canva1.grid(row=2, column=2, padx = 20)
text_canva1 = canva1.create_text(200, 100, text = portes_realisees, font=("Helvetica", 35))

#Objectif portes
label_objectif_portes = Label(root, text = "Objectif portes : ", font=("Helvetica", 20), bg = '#7F8FA6').grid(row=1, column=3)
canva2=Canvas(root, bg="ivory", width=lg,
        height=ht, bd=bw,highlightthickness=zf,
        highlightbackground="black")
canva2.grid(row=2, column=3)
text_canva2 = canva2.create_text(200, 100, text = objectif_portes, font=("Helvetica", 35))

#Portes avant réalisées
label_portes_avant = Label(root, text = "Portes avant : ", font=("Helvetica", 20), bg = '#7F8FA6').grid(row=3, column=2)
canva3=Canvas(root, bg="ivory", width=lg,
        height=ht, bd=bw,highlightthickness=zf,
        highlightbackground="black")
canva3.grid(row=4, column=2)
text_canva3 = canva3.create_text(200, 100, text = portes_realisees_avant, font=("Helvetica", 35))

#Portes arrières réalisées
label_portes_arrieres = Label(root, text = "Portes arrière : ", font=("Helvetica", 20), bg = '#7F8FA6').grid(row=3, column=3)
canva4=Canvas(root, bg="ivory", width=lg,
        height=ht, bd=bw,highlightthickness=zf,
        highlightbackground="black")
canva4.grid(row=4, column=3)
text_canva4 = canva4.create_text(200, 100, text = portes_realisees_arriere, font=("Helvetica", 35))

#Qualité
label_qualite = Label(root, text = "Qualité : ", font=("Helvetica", 20), bg = '#7F8FA6').grid(row=5, column=2)
canva5=Canvas(root, bg="ivory", width=lg,
        height=ht, bd=bw,highlightthickness=zf,
        highlightbackground="black")
canva5.grid(row=6, column=2)
text_canva5 = canva5.create_text(200, 100, text = str(taux_qualite)+"%", font=("Helvetica", 35))

#Objectif qualité
#label_defauts_toleres = Label(root, text = "Défauts tolérés : ", font=("Helvetica", 20)).grid(row=5, column=3)
label_objecitf_qualite = Label(root, text = "Objectif qualité : ", font=("Helvetica", 20), bg = '#7F8FA6').grid(row=5, column=3)
canva6=Canvas(root, bg="ivory", width=lg,
        height=ht, bd=bw,highlightthickness=zf,
        highlightbackground="black")
canva6.grid(row=6, column=3)
text_canva6 = canva6.create_text(200, 100, text = objectif_qualite, font=("Helvetica", 35))

"""Tracé du graphique"""
def plot_values():
    figure = plt.figure(figsize = (5,4), dpi = 100, facecolor = "#7F8FA6") ##figsize = dimensions graphique
    ax = plt.axes()
    ax.set_facecolor("#7F8FA6")
    chart = FigureCanvasTkAgg(figure, root)
    chart.get_tk_widget().grid(row = 2, column = 0, rowspan = 100, columnspan = 2)
    figure.add_subplot(111).plot(t1,y1)
    figure.add_subplot(111).plot(X_temps,Y_prod)
    figure.add_subplot(111).scatter(X_temps_retouches,X_temps_rebuts, marker="*", color="orange")
    figure.add_subplot(111).scatter(Y_retouches,Y_rebuts, marker="*", color="red")
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

    for i in range(duree_run * 60):
        canva1.itemconfig(text_canva1, text = portes_realisees)
        canva3.itemconfig(text_canva3, text = portes_realisees_avant)
        canva4.itemconfig(text_canva4, text = portes_realisees_arriere)
        update_values()
        root.update()
        time.sleep(1)

"""Création bouton"""
button_start = Button(root, text="Lancer le run", command = go, bg= "#7F8FA6") ##création boutton
button_start.grid(row=1, column=0) ##placement dans la fenêtre
root.bind("<Return>", update_values)
#plot_values() ##mise à jour du graphique



root.mainloop()