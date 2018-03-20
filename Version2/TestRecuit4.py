'''
Test de l'algorithme sur le long terme :
    * de nouvelles commandes sont passées
    * certaines sont livrées au fur et à mesure que le temps avance
'''

from Version2 import *
from Recuit2 import *
from GenerationDonnees2 import *
import matplotlib.pyplot as plt
import numpy as np

#nombre de nouvelles commandes que l'on va rajouter
nbNouvCommandes = 10


## Ordonne la production

#plan basique : traite les commandes comme elles arrivent
planBasique = planProduction()
for com in listeCommandes:
    planBasique.ajouteCommande(com)
calculeProduction(planBasique, listeCommandes, listeParametres)
energieBasique = energie1(listeCommandes)

#temps d'attente par commande
Y_tempsAttente = []
for i in range(0, len(listeCommandes)):
    Y_tempsAttente.append(listeCommandes[i].livraison - listeCommandes[i].instantCommande)
tempsAttenteCommandeMoyen = 0
for t in Y_tempsAttente:
    tempsAttenteCommandeMoyen += t
tempsAttenteCommandeMoyen /= len(Y_tempsAttente)

nbIterations = 100000
print("Initialisation")
planDepart, listeCoutProd, listeCoutAttente = Recuit2(listeCommandes, listeParametres, indexBoissons, tempsAttenteCommandeMoyen, nbIterations)


## Génère de nouvelles commandes

temps = listeCommandes[-1].instantCommande + 1
listeNouvCommandes = []
for i in range(0, nbNouvCommandes):
    temps += random.randint(0, periodeArrivee)
    nouvCom = commande(len(listeCommandes) + i, temps)
    nbBoissonsCommandees = random.randint(1, A_max)
    for j in range(0, nbBoissonsCommandees):
        b = boisson(random.randint(1, N_boissons), nouvCom, j)
        nouvCom.ajouteBoisson(b)
    triIntraCommandes(nouvCom)
    listeNouvCommandes.append(nouvCom)



## Laisse courir le temps

temps = listeCommandes[-1].instantCommande
plan = planDepart.copy()
while (len(nbNouvCommandes) > 0):
    temps += 1
    
    #livre une commande si elle est prête
    l = []
    commandesPretes = []
    for i in range(0, len(listeCommandes)):
        com = listeCommandes[i]
        if (com.livraison == temps):
            commandesPretes.append(com)
        else:
            l.append(com)
    listeCommandes = l
    if (len(commandesPretes) > 0):
        #supprime les commandes qui peuvent être livrées
        
    
    #ajoute les commandes qui viennent d'arriver
    l = []
    for i in range(0, len(listeNouvComandes)):
        nouvCom = listeNouvCommandes[i]
        if (nouvCom.instantCommande == temps):
            listeCommandes.append(nouvCom)
        else:
            l.append(nouvCom)
    listeNouvCommandes = l
    
    #calcule le nouveau plan de production
    nbIterations = 60000
    