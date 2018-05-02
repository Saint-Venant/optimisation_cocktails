'''
Ensemble de petits outils, générations de données etc... utilisés pour tester l'algorithme en production sur une soirée
'''

import numpy as np
import matplotlib.pyplot as plt
import GenerationDonnees2 as gen2
from Version2 import *
import random

np.random.seed(1)

plot_distrib = True


## Paramètres du modèle

#distribution du nombre de boissons par commande
mu_distrib = 3
sigma_distrib = 2

# Générer une soirée d'arrivée de commandes
nb_commandes_soiree = 3*10

# Instant de début de la soirée
debut_soiree = 0

# Instant de fin de la soiree
fin_soiree = 20*60 #2h


## Création des commandes

# Distribution (gaussienne) des instants d'arrivée des commandes
sigma_arrivees = fin_soiree / 4
distrib_gaussian = np.random.normal(fin_soiree/2, sigma_arrivees, int(nb_commandes_soiree*2/3))
distrib_uniform = np.random.uniform(debut_soiree, fin_soiree, int(nb_commandes_soiree/3))
distrib_arrivees = np.concatenate((distrib_gaussian, distrib_uniform))
for i in range(0, nb_commandes_soiree):
    while (distrib_arrivees[i] < 0) or (distrib_arrivees[i] > fin_soiree):
        distrib_arrivees[i] = np.random.normal(fin_soiree/2, sigma_arrivees)
distrib_arrivees = np.sort(distrib_arrivees)

# -- vérification de la distribution obtenue
if plot_distrib:
    plt.figure()
    plt.hist(distrib_arrivees)
    plt.xlabel("instants d'arrivée")
    plt.ylabel("effetif")
    plt.title("Distribution des instants d'arrivée des commandes")
    plt.show()


# liste des commandes de la soirée
liste_commandes_soiree = []
for i in range(nb_commandes_soiree):
    temps = distrib_arrivees[i]
    c = commande(i, temps)
    nb_boissons = gen2.tire_nb_boissons(mu_distrib, sigma_distrib)
    for j in range(nb_boissons):
        b = boisson(random.randint(1, N_boissons), c, j)
        c.ajouteBoisson(b)
    liste_commandes_soiree.append(c)



