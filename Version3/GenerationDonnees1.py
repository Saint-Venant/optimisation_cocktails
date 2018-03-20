from Version1 import *
import numpy as np
import random
import matplotlib.pyplot as plt

## Graine aléatoire

random.seed(3)


#nombre de commandes à optimiser
nbCommandes = 10

#période d'arrivée des commandes
periodeArrivee = 36


## création des commandes

listeCommandes = []
temps = 0
for i in range(0, nbCommandes):
    c = commande(i, temps)
    temps += random.randint(0, periodeArrivee)
    
    #tire un nombre aléatoire de boissons commandées
    nbBoissonsCommandees = random.randint(1, A_max)
    
    #crée ces boissons, et les affecte à la commande c
    for j in range(0, nbBoissonsCommandees):
        b = boisson(random.randint(1, N_boissons), c, j)
        c.ajouteBoisson(b)
    
    #ajoute la commande à la liste des commandes
    listeCommandes.append(c)


#creation de l'indexBoissons
for com in listeCommandes:
    triIntraCommandes(com)
indexBoissons = []
for i in range(0, len(listeCommandes)):
    com = listeCommandes[i]
    for j in range(0, len(com.listeBoissons)):
        indexBoissons.append([i, j])



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