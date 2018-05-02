from Version2 import *
import random
import matplotlib.pyplot as plt
import numpy as np

## Graine aléatoire

random.seed(5)
np.random.seed(1)


#nombre de commandes à optimiser
#nbCommandes = 10
nbCommandes = 12

#période d'arrivée des commandes
periodeArrivee = 115

#distribution du nombre de boissons par commande
mu_distrib = 3
sigma_distrib = 2

## création des commandes

#tire un nombre de boissons selon une loi gaussienne tronquée
def tire_nb_boissons(mu, sigma):
    nb = int(np.random.normal(loc=mu, scale=sigma))
    while (nb <= 0) or (nb > A_max):
        nb = int(np.random.normal(loc=mu, scale=sigma))
    return nb

#génère une liste de commandes à partir d'un instant donné
def genere_liste_commandes(instant, index_derniere, nb_commandes):
    liste = []
    temps = instant
    for i in range(index_derniere+1, nb_commandes+index_derniere+1):
        c = commande(i, temps)
        temps += random.randint(0, periodeArrivee)
        nbBoissonsCommandees = tire_nb_boissons(mu_distrib, sigma_distrib)
        for j in range(0, nbBoissonsCommandees):
            b = boisson(random.randint(1, N_boissons), c, j)
            c.ajouteBoisson(b)
        liste.append(c)
    return liste
    

listeCommandes = []
temps = 0
for i in range(0, nbCommandes):
    c = commande(i, temps)
    temps += random.randint(0, periodeArrivee)
    
    #tire un nombre aléatoire de boissons commandées
    nbBoissonsCommandees = tire_nb_boissons(mu_distrib, sigma_distrib)
    
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
'''


#Blue Lagoon
listeParametres.append([1, 2, 22, 0.7*22, 0.85*22])
#California Petit
listeParametres.append([2, 2, 14, 10, 12])
#California Grand
listeParametres.append([3, 2, 26, 23, 25])
#Pinte
listeParametres.append([4, 5, 13, 12, 12])
#Pichet
listeParametres.append([5, 2, 40, 38, 38])