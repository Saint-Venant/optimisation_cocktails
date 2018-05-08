from StructuresProduction import *
import GlobalParam as gp
from AlgoRecuit import *
import GenerationDonnees as gend
import OutilsGraphiques as outg
import matplotlib.pyplot as plt
import numpy as np


listeCommandes = [x.copy() for x in gend.listeCommandes_statique]
listeParametres = [x.copy() for x in gend.listeParametres]


## Récupération des données initiales : plan basique

#plan basique : traite les commandes comme elles arrivent
planBasique = planProduction("buffer")
for com in listeCommandes:
    planBasique.ajouteCommande(com)
calculeProduction(planBasique, listeParametres)
tempsProdBasique = energie1(planBasique)

#temps d'attente par commande
attenteBasique = outg.attente_commandes(listeCommandes)

#fraicheur des boissons
fraicheurBasique = outg.attente_boissons(listeCommandes)

#nombre de commandes préparées en parallèle
paralleleBasique = nbTachesParalleles(planBasique)

## Récupération des données initiales : plan ultra opti

#plan ultra opti : groupe toutes les boissons par type
planOpti = planProduction("buffer")
for com in listeCommandes:
    planOpti.ajouteCommandeUltraOpti(com)
calculeProduction(planOpti, listeParametres)
tempsProdOpti = energie1(planOpti)

#temps d'attente par commande
attenteOpti = outg.attente_commandes(listeCommandes)

#fraicheur des boissons
fraicheurOpti = outg.attente_boissons(listeCommandes)

#nombre de commandes préparées en parallèle
paralleleOpti = nbTachesParalleles(planOpti)


## Test Recuit1

nbIterations = 40000

plan, listeEnergie = Recuit1(listeCommandes, listeParametres, nbIterations)

calculeProduction(plan, listeParametres)
tempsProdPlan = energie1(plan)

#temps d'attente par commande
attentePlan = outg.attente_commandes(listeCommandes)

#fraicheur des boissons
fraicheurPlan = outg.attente_boissons(listeCommandes)

#nombre de commandes préparées en parallèle
parallelePlan = nbTachesParalleles(plan)


## Résultats

#progression du recuit
plt.figure(1)
vect_energie = [listeEnergie]
vect_labels = ["temps total production"]
outg.plot_recuit(vect_energie, vect_labels)
plt.show()

#temps d'attente par commande
plt.figure(2)
vect_attentes = [attenteBasique, attenteOpti, attentePlan]
vect_labels = ["plan basique", "plan opti sans contrainte", "plan recuit sans contrainte"]
outg.plot_attente_commandes(vect_attentes, vect_labels)
plt.show()

#distribution (histogramme) des temps d'attente commandes
plt.figure(3)
vect_attentes = [attenteBasique, attenteOpti, attentePlan]
vect_titres = ["plan basique", "plan opti sans contrainte", "plan recuit sans contrainte"]
finesse = 6
outg.hist_attente_commandes(vect_attentes, vect_titres, finesse)
plt.show()

#fraicheur des boissons
plt.figure(4)
finesse = 20
vect_attentes = [fraicheurBasique, fraicheurOpti, fraicheurPlan]
vect_titres = ["plan basique", "plan opti sans contrainte", "plan recuit sans contrainte"]
outg.plot_attente_boissons(vect_attentes, vect_titres, finesse)


#affichage du gain de productivité
print("tempsProdBasique :", int(tempsProdBasique))
print("tempsProdOpti :", int(tempsProdOpti))
print("tempsProdPlan :", int(tempsProdPlan))
print("Gain de productivité : ", outg.arrondi((tempsProdBasique-tempsProdPlan)*100/tempsProdBasique, 2), "%")


#nombre de commandes préparées en parallèle
plt.figure(5)
vect_prep = [paralleleBasique, paralleleOpti, parallelePlan]
vect_labels = ["plan basique", "plan opti sans contrainte", "plan recuit sans contrainte"]
outg.plot_preparation_parallele(vect_prep, vect_labels)
plt.show()
