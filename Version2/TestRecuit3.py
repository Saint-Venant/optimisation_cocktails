'''
But = étudier l'impact de l'ajout d'une nouvelle commande dans un plan de production déjà ordonné
'''

from Version2 import *
from Recuit2 import *
from GenerationDonnees2 import *
import matplotlib.pyplot as plt
import numpy as np

random.seed(5)



## Ordonne la production

#plan basique : traite les commandes comme elles arrivent
planBasique = planProduction("buffer")
for com in listeCommandes:
    planBasique.ajouteCommande(com)
calculeProduction(planBasique, listeParametres)
energieBasique = energie1(planBasique)

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


## Génère une nouvelle commande

temps = listeCommandes[-1].instantCommande
temps += random.randint(0, periodeArrivee)
nouvCom = commande(len(listeCommandes), temps)
a = tire_nb_boissons()
for j in range(0, a):
    b = boisson(random.randint(1, N_boissons), nouvCom, j)
    nouvCom.ajouteBoisson(b)
triIntraCommandes(nouvCom)

#ajout à listeCommandes
listeCommandes.append(nouvCom)

#ajout à indexBoissons
for j in range(0, len(nouvCom.listeBoissons)):
    indexBoissons.append([nouvCom.num, j])

#ajout de la nouvelle commande au plan de production
planDepart.ajouteCommande(nouvCom)


## Récupération des données initiales : plan de depart

#plan depart : traite la nouvelle commande comme elle arrive
calculeProduction(planDepart, listeParametres)
energieDepart = energie1(planDepart)

#temps d'attente par commande
Y_tempsAttenteDepart = []
for i in range(0, len(listeCommandes)):
    Y_tempsAttenteDepart.append(listeCommandes[i].livraison - listeCommandes[i].instantCommande)
tempsAttenteCommandeMoyen = 0
for t in Y_tempsAttenteDepart:
    tempsAttenteCommandeMoyen += t
tempsAttenteCommandeMoyen /= len(Y_tempsAttenteDepart)

#fraicheur des boissons
fraicheurDepart = []
for com in listeCommandes:
    for b in com.listeBoissons:
        fraicheurDepart.append(b.livraison - b.fin)

#nombre de commandes préparées en parallèle
paralleleDepart = nbTachesParalleles(planDepart)


## Test Recuit3

nbIterations = 40000
print("\n \n \nCalcul de la nouvelle solution")

plan, listeCoutProd, listeCoutAttente = Recuit3(planDepart, listeCommandes, listeParametres, indexBoissons, tempsAttenteCommandeMoyen, nbIterations)

calculeProduction(plan, listeParametres)
energiePlan = energie1(plan)
listeEnergieHybride = []
for i in range(0, len(listeCoutProd)):
    listeEnergieHybride.append(listeCoutProd[i]+listeCoutAttente[i])

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
parallelePlan = nbTachesParalleles(plan)

## Résultats

#progression du recuit
plt.figure(1)
plt.plot(listeCoutProd, 'bo', label="temps total production")
plt.plot(listeEnergieHybride, 'ro', label="energie hybride")
plt.xlabel("itération")
plt.ylabel("énergie")
plt.title("Progression du recuit 3")
plt.legend()
plt.show()

#temps d'attente par commande
plt.figure(2)
plt.plot(Y_tempsAttenteDepart, 'bo', label="plan depart")
plt.plot(Y_tempsAttentePlan, 'go', label="plan recuit3 avec contrainte")
plt.plot(len(listeCommandes)*[tempsAttenteCommandeMoyen], 'k-', label="temps d'attente moyen")
plt.plot(len(listeCommandes)*[1.1*tempsAttenteCommandeMoyen], 'k--', label="temps d'attente moyen + 10%")
xmin = 0
xmax = len(Y_tempsAttenteDepart)-1
ymin = 0
ymax = max([max(Y_tempsAttenteDepart), max(Y_tempsAttentePlan)]) + 50
plt.axis([xmin, xmax, ymin, ymax])
plt.xlabel("commandes")
plt.ylabel("temps d'attente")
plt.title("Temps d'attente par commande")
plt.legend()
plt.show()

plt.figure(3)
finesse = 6
plt.subplot(121)
plt.hist(Y_tempsAttenteDepart, finesse, facecolor='b')
plt.title("Distribution temps attente commande : plan depart")
plt.xlabel("temps d'attente clients")
plt.ylabel("effectif")
plt.subplot(122)
plt.hist(Y_tempsAttentePlan, finesse, facecolor='g')
plt.title("Distribution temps attente commande : plan recuit3 avec contrainte")
plt.xlabel("temps d'attente clients")
plt.ylabel("effectif")
plt.show()

#fraicheur des boissons
plt.figure(4)
finesse = 20
plt.subplot(121)
plt.hist(fraicheurDepart, finesse, facecolor='b')
plt.title("Distribution des fraicheurs : plan depart")
plt.xlabel("temps d'attente des boissons")
plt.ylabel("effectif")
plt.subplot(122)
plt.hist(fraicheurPlan, finesse, facecolor='g')
plt.title("Distribution des fraicheurs : plan recuit3 avec contrainte")
plt.xlabel("temps d'attente des boissons")
plt.ylabel("effectif")
plt.show()


#affichage du gain de productivité
instantDebutProd = listeCommandes[0].listeBoissons[0].debut
for com in listeCommandes:
    for b in com.listeBoissons:
        instantDebutProd = min(instantDebutProd, b.debut)
print("temps Prod Depart :", int(energieDepart) - instantDebutProd)
print("temps Prod Plan :", int(energiePlan) - instantDebutProd)
print("Gain de productivité Plan : ", int((energieDepart-energiePlan)*100/(energieDepart-instantDebutProd)), "%")
print()


#nombre de commandes préparées en parallèle
plt.figure(5)
plt.title("Nombre de commandes préparées en parallèle")
plt.xlabel("temps")
plt.ylabel("nombre de commandes différentes en cours de préparation")
plt.plot(paralleleDepart, 'b', label="au départ")
plt.plot(parallelePlan, 'g', label="optimisation nouvelle commande")
plt.legend()
plt.axis([0, len(paralleleDepart), min(paralleleDepart)-1, max(max(parallelePlan), max(paralleleDepart))+1])
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
plt.axis([instantDebutProd, energieDepart, -1, len(listeCommandes)])
plt.title("Planning de production des commandes")
plt.xlabel("temps")
plt.ylabel("indice de commande")
plt.show()