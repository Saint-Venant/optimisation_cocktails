from Version2 import *
from Recuit2 import *
from GenerationDonnees2 import *
import matplotlib.pyplot as plt
import numpy as np



## Récupération des données initiales : plan basique

#plan basique : traite les commandes comme elles arrivent
planBasique = planProduction()
for com in listeCommandes:
    planBasique.ajouteCommande(com)
calculeProduction(planBasique, listeCommandes, listeParametres)
energieBasique = energie1(listeCommandes)

#temps d'attente par commande
Y_tempsAttenteBasique = []
for i in range(0, len(listeCommandes)):
    Y_tempsAttenteBasique.append(listeCommandes[i].livraison - listeCommandes[i].instantCommande)

#fraicheur des boissons
fraicheurBasique = []
for com in listeCommandes:
    for b in com.listeBoissons:
        fraicheurBasique.append(b.livraison - b.fin)

#nombre de commandes préparées en parallèle
paralleleBasique = nbTachesParallelles(listeCommandes)

## Récupération des données initiales : plan ultra opti

#plan ultra opti : groupe toutes les boissons par type
planOpti = planProduction()
for com in listeCommandes:
    planOpti.ajouteCommandeUltraOpti(com)
calculeProduction(planOpti, listeCommandes, listeParametres)
energieOpti = energie1(listeCommandes)

#temps d'attente par commande
Y_tempsAttenteOpti = []
for i in range(0, len(listeCommandes)):
    Y_tempsAttenteOpti.append(listeCommandes[i].livraison - listeCommandes[i].instantCommande)

#fraicheur des boissons
fraicheurOpti = []
for com in listeCommandes:
    for b in com.listeBoissons:
        fraicheurOpti.append(b.livraison - b.fin)

#nombre de commandes préparées en parallèle
paralleleOpti = nbTachesParallelles(listeCommandes)


## Test Recuit1

nbIterations = 120000

plan, listeEnergie = Recuit1(listeCommandes, listeParametres, indexBoissons, nbIterations)

calculeProduction(plan, listeCommandes, listeParametres)
energiePlan = energie1(listeCommandes)

#temps d'attente par commande
Y_tempsAttentePlan = []
for i in range(0, len(listeCommandes)):
    Y_tempsAttentePlan.append(listeCommandes[i].livraison - listeCommandes[i].instantCommande)

#fraicheur des boissons
fraicheurPlan = []
for com in listeCommandes:
    for b in com.listeBoissons:
        fraicheurPlan.append(b.livraison - b.fin)

#nombre de commandes préparées en parallèle
parallelePlan = nbTachesParallelles(listeCommandes)


## Résultats

#progression du recuit
plt.figure(1)
plt.plot(listeEnergie, 'o')
plt.xlabel("itération")
plt.ylabel("temps total de production")
plt.title("Progression du recuit")
plt.show()

#temps d'attente par commande
plt.figure(2)
plt.plot(Y_tempsAttenteBasique, 'bo', label="plan basique")
plt.plot(Y_tempsAttenteOpti, 'ro', label="plan opti sans contrainte")
plt.plot(Y_tempsAttentePlan, 'go', label="plan recuit sans contrainte")
plt.xlabel("commandes")
plt.ylabel("temps d'attente")
plt.title("Temps d'attente par commande")
plt.legend()
plt.show()

plt.figure(3)
finesse = 6
plt.subplot(131)
plt.hist(Y_tempsAttenteBasique, finesse, facecolor='b')
plt.title("Distribution temps attente commande : plan basique")
plt.xlabel("temps d'attente clients")
plt.ylabel("effectif")
plt.subplot(132)
plt.hist(Y_tempsAttenteOpti, finesse, facecolor='r')
plt.title("Distribution temps attente commande : plan opti sans contrainte")
plt.xlabel("temps d'attente clients")
plt.ylabel("effectif")
plt.subplot(133)
plt.hist(Y_tempsAttentePlan, finesse, facecolor='g')
plt.title("Distribution temps attente commande : plan recuit sans contrainte")
plt.xlabel("temps d'attente clients")
plt.ylabel("effectif")
plt.show()

#fraicheur des boissons
plt.figure(4)
finesse = 20
plt.subplot(131)
plt.hist(fraicheurBasique, finesse, facecolor='b')
plt.title("Distribution des fraicheurs : plan basique")
plt.xlabel("temps d'attente des boissons")
plt.ylabel("effectif")
plt.subplot(132)
plt.hist(fraicheurOpti, finesse, facecolor='r')
plt.title("Distribution des fraicheurs : plan opti")
plt.xlabel("temps d'attente des boissons")
plt.ylabel("effectif")
plt.subplot(133)
plt.hist(fraicheurPlan, finesse, facecolor='g')
plt.title("Distribution des fraicheurs : plan recuit sans contrainte")
plt.xlabel("temps d'attente des boissons")
plt.ylabel("effectif")
plt.show()


#affichage du gain de productivité
print("energieBasique :", int(energieBasique))
print("energieOpti :", int(energieOpti))
print("energiePlan :", int(energiePlan))
print("Gain de productivité : ", (energieBasique-energiePlan)*100/energieBasique, "%")


#nombre de commandes préparées en parallèle
plt.figure(5)
plt.title("Nombre de commandes préparées en parallèle")
plt.xlabel("temps")
plt.ylabel("nombre de commandes différentes en cours de préparation")
plt.plot(paralleleBasique, 'b', label="sans optimisation")
plt.plot(paralleleOpti, 'r', label="avec optimisation sans contrainte")
plt.legend()
plt.axis([0, len(paralleleBasique), min(paralleleBasique)-1, max(paralleleOpti)+1])
plt.show()
