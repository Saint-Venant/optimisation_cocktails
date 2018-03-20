from Version0 import *
from PremierRecuit import *
import matplotlib.pyplot as plt
import numpy as np

#nombre de commandes à optimiser
nbCommandes = 20

## création des commandes
listeCommandes = []
temps = 0
for i in range(0, nbCommandes):
    c = commande(i, temps)
    temps += random.randint(0, 36)
    
    #tire un nombre aléatoire de boissons commandées
    nbBoissonsCommandees = random.randint(1, A_max)
    
    #crée ces boissons, et les affecte à la commande c
    for j in range(0, nbBoissonsCommandees):
        b = boisson(random.randint(1, N_boissons), c, j)
        c.ajouteBoisson(b)
    
    #ajoute la commande à la liste des commandes
    listeCommandes.append(c)

#affichage des commandes crées
for c in listeCommandes:
    print("instant de commande :", c.instantCommande)
    c.afficheBoissons()
    triIntraCommandes(c)
    c.afficheBoissons()
    print()




## génération des paramètres du temps de préparation
listeParametres = []
'''exemple d'un parametre : l
    l = [idTypeBoisson, nbOpti, coef1, coef2, coef3]
    nbOpti = nombre de boissons pour lequel le temps de préparation est le plus rentable (3 par déafaut)
'''
for i in range(0, N_boissons):
    l = []
    l.append(i+1)
    nbOpti = random.randint(1, 5)
    l.append(nbOpti)
    a = 5*(0.5+random.random())/1.5
    l.append(a)
    b = (0.5+random.random())*(1/1.5)*0.6*a
    l.append(b)
    l.append(0.3*a + 0.7*b)
    listeParametres.append(l)
print()
print("liste des paramètres de production")
for param in listeParametres:
    print(param)



## Récupération des données initiales

#temps d'attente par commande
planBasique = planProduction()
for com in listeCommandes:
    planBasique.ajouteCommande(com)
calculeProduction(planBasique, listeCommandes, listeParametres)
X_commandes = []
Y_tempsAttenteBasique = []
for i in range(0, nbCommandes):
    X_commandes.append(i+1)
    Y_tempsAttenteBasique.append(listeCommandes[i].livraison - listeCommandes[i].instantCommande)

#fraicheur des boissons
fraicheurBasique = []
for com in listeCommandes:
    for b in com.listeBoissons:
        fraicheurBasique.append(b.livraison - b.fin)


## Test de PremierRecuit

nbIterations = 1500

#descenteLocale1
plan1, listeEnergie1 = descenteLocale1(listeCommandes, listeParametres, nbIterations)

Y_tempsAttenteDescenteLocale1 = []
for i in range(0, nbCommandes):
    Y_tempsAttenteDescenteLocale1.append(listeCommandes[i].livraison - listeCommandes[i].instantCommande)

fraicheurDescenteLocale1 = []
for com in listeCommandes:
    for b in com.listeBoissons:
        fraicheurDescenteLocale1.append(b.livraison - b.fin)

#descenteLocale2
plan2, listeEnergie2 = descenteLocale2(listeCommandes, listeParametres, nbIterations)

Y_tempsAttenteDescenteLocale2 = []
for i in range(0, nbCommandes):
    Y_tempsAttenteDescenteLocale2.append(listeCommandes[i].livraison - listeCommandes[i].instantCommande)

fraicheurDescenteLocale2 = []
for com in listeCommandes:
    for b in com.listeBoissons:
        fraicheurDescenteLocale2.append(b.livraison - b.fin)

#descenteLocale3
plan3, listeEnergie3 = descenteLocale3(listeCommandes, listeParametres, nbIterations)

Y_tempsAttenteDescenteLocale3 = []
for i in range(0, nbCommandes):
    Y_tempsAttenteDescenteLocale3.append(listeCommandes[i].livraison - listeCommandes[i].instantCommande)

fraicheurDescenteLocale3 = []
for com in listeCommandes:
    for b in com.listeBoissons:
        fraicheurDescenteLocale3.append(b.livraison - b.fin)

#affichage des perormances de l'algorithme
plt.figure(1)
plt.plot(listeEnergie1, 'r', label="descenteLocale1")
plt.plot(listeEnergie2, 'g', label="descenteLocale2")
plt.plot(listeEnergie3, 'y', label="descenteLocale3")
plt.title("Energie en fonction du nombre d'itérations")
plt.xlabel("nombre d'itérations")
plt.ylabel('énergie')
plt.legend()
plt.show()

#performance du point de vue du client
plt.figure(2)
plt.plot(X_commandes, Y_tempsAttenteBasique, 'bo', label="sans optimisation")
plt.plot(X_commandes, Y_tempsAttenteDescenteLocale1, 'ro', label="optimisation : DescenteLocale1")
plt.plot(X_commandes, Y_tempsAttenteDescenteLocale2, 'go', label="optimisation : DescenteLocale2")
plt.plot(X_commandes, Y_tempsAttenteDescenteLocale3, 'yo', label="optimisation : DescenteLocale3")
plt.xlabel("commande")
plt.ylabel("temps d'attente")
plt.legend()
plt.show()


#performance sur le temps d'attente des boissons avant livraison
plt.figure(3)
finesse = 15
plt.subplot(221)
plt.hist(fraicheurBasique, finesse, facecolor='b')
plt.xlabel("temps d'attente")
plt.ylabel('effectif')
plt.title("Distribution des temps d'attente \n avant livraison des boissons : \n sans optimisation")

plt.subplot(222)
plt.hist(fraicheurDescenteLocale1, finesse, facecolor='r')
plt.title("Distribution des temps d'attente \n avant livraison des boissons : \n optimisation en descenteLocale1")
plt.xlabel("temps d'attente")
plt.ylabel("effectif")

plt.subplot(223)
plt.hist(fraicheurDescenteLocale2, finesse, facecolor='g')
plt.title("Distribution des temps d'attente \n avant livraison des boissons : \n optimisation en descenteLocale2")
plt.xlabel("temps d'attente")
plt.ylabel("effectif")

plt.subplot(224)
plt.hist(fraicheurDescenteLocale3, finesse, facecolor='y')
plt.title("Distribution des temps d'attente \n avant livraison des boissons : \n optimisation en descenteLocale2")
plt.xlabel("temps d'attente")
plt.ylabel("effectif")

plt.show()


## plans de production
print()

print("Plan 1 :")
plan1.affichePlan()

print()
print("Plan 2 :")
plan2.affichePlan()

print()
print("Plan 3 :")
plan3.affichePlan()
