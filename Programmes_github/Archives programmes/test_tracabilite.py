##excel
import xlsxwriter

#création feuille excel
workbook = xlsxwriter.Workbook('C:/Users/natha/Desktop/ECAM/ECAM/Usine_4.0/Programmes_Python/Main_program/tracabilite.xlsx')
sheet = workbook.add_worksheet()

#nom colonne write(ligne, colonne, "texte")

#initialisation nom colonne
sheet.write(0, 0, 'ID')
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

#message = str(id;heureentree;heurem1;heurem2;heuresortie;conformite) avec heure:minutes:seconde:jour:mois:annee


#entree message + split + excel
while True:
    message = input("entrer message")
    if (message != "fin"):
        message_split = message.split(";")
        tracabilite(message_split)
        print ("porte",numero_porte-1,"enregistrée")
    else:
        workbook.close()
        print("fermeture excel")