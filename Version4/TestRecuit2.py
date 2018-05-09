from StructuresProduction import *
import GlobalParam as gp
from AlgoRecuit import *
import GenerationDonnees as gend
import OutilsGraphiques as outg
import matplotlib.pyplot as plt
import numpy as np


listeCommandes = gend.listeCommandes_statique
listeParametres = gend.listeParametres

## Récupération des données initiales : plan basique

#plan basique : traite les commandes comme elles arrivent
planBasique = planProduction("buffer")
for com in listeCommandes:
    planBasique.ajouteCommande(com)
calculeProduction(planBasique, listeParametres)
tempsProdBasique = energie1(planBasique)

#temps d'attente par commande
attenteBasique = outg.attente_commandes(listeCommandes)
attenteBasiqueMoy = np.mean(attenteBasique[:,1])

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

## Test Recuit2

nbIterations = 100000

plan, vectCoutProd, vectCoutAttente = Recuit2(listeCommandes, listeParametres, attenteBasiqueMoy, nbIterations)

calculeProduction(plan, listeParametres)
tempsProdPlan = energie1(plan)
vectEnergieHybride = vectCoutProd + vectCoutAttente

#temps d'attente par commande
attentePlan = outg.attente_commandes(listeCommandes)

#fraicheur des boissons
fraicheurPlan = outg.attente_boissons(listeCommandes)

#nombre de commandes préparées en parallèle
parallelePlan = nbTachesParalleles(plan)

## Résultats

#progression du recuit
plt.figure(1)
vect_energie = [vectCoutProd, vectEnergieHybride]
vect_labels = ["temps total production", "énergie hybride"]
outg.plot_recuit(vect_energie, vect_labels)
plt.show()

#temps d'attente par commande
plt.figure(2)
vect_attentes = [attenteBasique, attenteOpti, attentePlan]
vect_labels = ["sans optimisation", "optimisation sans contrainte", "optimisation avec contraintes"]
param_moy = [len(listeCommandes)*[attenteBasiqueMoy], len(listeCommandes)*[1.1*attenteBasiqueMoy], "temps d'attente moyen basique", "temps d'attente moyen + 10%"]
outg.plot_attente_commandes(vect_attentes, vect_labels, param_moy)
plt.show()

#distribution (histogramme) des temps d'attente commandes
plt.figure(3)
vect_attentes = [attenteBasique, attenteOpti, attentePlan]
vect_titres = ["sans optimisation", "optimisation sans contrainte", "optimisation avec contraintes"]
finesse = 6
outg.hist_attente_commandes(vect_attentes, vect_titres, finesse)
plt.show()

#fraicheur des boissons
plt.figure(4)
finesse = 20
vect_attentes = [fraicheurBasique, fraicheurOpti, fraicheurPlan]
vect_titres = ["sans optimisation", "optimisation sans contrainte", "optimisation avec contraintes"]
outg.plot_attente_boissons(vect_attentes, vect_titres, finesse)
plt.show()

#affichage du gain de productivité
print("temps Prod Basique :", int(tempsProdBasique))
print("temps Prod Opti :", int(tempsProdOpti))
print("temps Prod Plan :", int(tempsProdPlan))
print("Gain de productivité Opti : ", outg.arrondi((tempsProdBasique - tempsProdOpti)*100/tempsProdBasique, 2), "%")
print("Gain de productivité Plan : ", outg.arrondi((tempsProdBasique - tempsProdPlan)*100/tempsProdBasique, 2), "%")
print()
print("attenteBasiqueMoy :", attenteBasiqueMoy)
coutProd, coutAttente = energie2(plan, attenteBasiqueMoy)
print("temps de production :", coutProd, "\ncout d'attente client :", coutAttente)
print()

#nombre de commandes préparées en parallèle
plt.figure(5)
vect_prep = [paralleleBasique, paralleleOpti, parallelePlan]
vect_labels = ["sans optimisation", "optimisation sans contrainte", "optimisation avec contraintes"]
outg.plot_preparation_parallele(vect_prep, vect_labels)
plt.show()

#planning de production
plt.figure(6)
outg.plot_planning(plan)
plt.show()