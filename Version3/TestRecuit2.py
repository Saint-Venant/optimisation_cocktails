from Version1 import *
from GenerationDonnees1 import *
from Recuit1 import *
import matplotlib.pyplot as plt
import numpy as np

random.seed(3)

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
tempsAttenteCommandeMoyen = 0
for t in Y_tempsAttenteBasique:
    tempsAttenteCommandeMoyen += t
tempsAttenteCommandeMoyen /= len(Y_tempsAttenteBasique)

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
moyTempsAttenteOpti = sum(Y_tempsAttenteOpti)/len(Y_tempsAttenteOpti)

#fraicheur des boissons
fraicheurOpti = []
for com in listeCommandes:
    for b in com.listeBoissons:
        fraicheurOpti.append(b.livraison - b.fin)

#nombre de commandes préparées en parallèle
paralleleOpti = nbTachesParallelles(listeCommandes)


## Test Recuit2

nbIterations = 50000

plan, listeCoutProd, listeCoutAttente = Recuit2(listeCommandes, listeParametres, indexBoissons, tempsAttenteCommandeMoyen, nbIterations)

calculeProduction(plan, listeCommandes, listeParametres)
energiePlan = energie1(listeCommandes)
listeEnergieHybride = []
for i in range(0, len(listeCoutProd)):
    listeEnergieHybride.append(listeCoutProd[i]+listeCoutAttente[i])

#temps d'attente par commande
Y_tempsAttentePlan = []
for i in range(0, len(listeCommandes)):
    Y_tempsAttentePlan.append(listeCommandes[i].livraison - listeCommandes[i].instantCommande)
moyTempsAttentePlan = sum(Y_tempsAttentePlan)/len(Y_tempsAttentePlan)

#fraicheur des boissons
fraicheurPlan = []
for com in listeCommandes:
    for b in com.listeBoissons:
        fraicheurPlan.append(b.livraison - b.fin)

#nombre de commandes préparées en parallèle
parallelePlan = nbTachesParallelles(listeCommandes)

## Résultats
'''
#progression du recuit
plt.figure(1)
plt.plot(listeCoutProd, 'bo', label="temps total production")
plt.plot(listeEnergieHybride, 'ro', label="energie hybride")
plt.xlabel("itération")
plt.ylabel("énergie")
plt.title("Progression du recuit")
plt.legend()
plt.show()

#temps d'attente par commande
plt.figure(2)
plt.plot(Y_tempsAttenteBasique, 'bo', label="plan basique")
plt.plot(Y_tempsAttenteOpti, 'ro', label="plan opti sans contrainte")
plt.plot(Y_tempsAttentePlan, 'go', label="plan recuit2 avec contrainte")
plt.plot(len(listeCommandes)*[tempsAttenteCommandeMoyen], 'k-', label="temps d'attente moyen")
plt.plot(len(listeCommandes)*[1.1*tempsAttenteCommandeMoyen], 'k--', label="temps d'attente moyen + 10%")
plt.plot(len(listeCommandes)*[moyTempsAttenteOpti], 'r-')
plt.plot(len(listeCommandes)*[moyTempsAttentePlan], 'g-')
xmin = 0
xmax = len(Y_tempsAttenteBasique)-1
ymin = 0
ymax = max([max(Y_tempsAttenteBasique), max(Y_tempsAttenteOpti), max(Y_tempsAttentePlan)]) + 50
plt.axis([xmin, xmax, ymin, ymax])
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
plt.title("Distribution temps attente commande : plan recuit2 avec contrainte")
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
plt.title("Distribution des fraicheurs : plan recuit2 avec contrainte")
plt.xlabel("temps d'attente des boissons")
plt.ylabel("effectif")
plt.show()
'''

#affichage du gain de productivité
instantDebutProd = listeCommandes[0].listeBoissons[0].debut
for com in listeCommandes:
    for b in com.listeBoissons:
        instantDebutProd = min(instantDebutProd, b.debut)
print("temps Prod Basique :", int(energieBasique) - instantDebutProd)
print("temps Prod Opti :", int(energieOpti) - instantDebutProd)
print("temps Prod Plan :", int(energiePlan) - instantDebutProd)
print("Gain de productivité Opti : ", int((energieBasique-energieOpti)*100/(energieBasique-instantDebutProd)), "%")
print("Gain de productivité Plan : ", int((energieBasique-energiePlan)*100/(energieBasique-instantDebutProd)), "%")
print()
print("tempsAttente :", tempsAttenteCommandeMoyen)
print(energie2(listeCommandes, tempsAttenteCommandeMoyen))
print()

'''
#nombre de commandes préparées en parallèle
plt.figure(5)
plt.title("Nombre de commandes préparées en parallèle")
plt.xlabel("temps")
plt.ylabel("nombre de commandes différentes en cours de préparation")
plt.plot(paralleleBasique, 'b', label="sans optimisation")
plt.plot(paralleleOpti, 'r', label="optimisation sans contrainte")
plt.plot(parallelePlan, 'g', label="optimisation avec contraintes")
plt.legend()
plt.axis([0, len(paralleleBasique), min(paralleleBasique)-1, max(paralleleOpti)+1])
plt.show()

#planning de production
plt.figure(6)
indexCouleurs = {}
for com in listeCommandes:
    c = np.random.rand(3,)
    indexCouleurs[com] = c
for cl in plan.clusters:
    b1 = cl[0]
    b2 = cl[-1]
    plt.plot([b1.debut, b1.debut], [-1, len(listeCommandes)], 'k--')
    plt.plot([b2.fin, b2.fin], [-1, len(listeCommandes)], 'k--')
    for b in cl:
        num = b.commande.num
        plt.plot([b1.debut, b2.fin], [num, num], color=indexCouleurs[b.commande], linewidth=10)
plt.axis([instantDebutProd, energieBasique, -1, len(listeCommandes)])
plt.title("Planning de production des commandes")
plt.xlabel("temps")
plt.ylabel("indice de commande")
plt.show()'''