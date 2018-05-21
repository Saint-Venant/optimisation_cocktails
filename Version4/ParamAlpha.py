'''
Teste le bon paramètre de refroidissement pour le recuit avec voisinage complet
'''

from StructuresProduction import *
import GlobalParam as gp
from AlgoRecuit import *
import GenerationDonnees as gend
import OutilsGraphiques as outg
import SimuSoiree as sims
import numpy as np
from collections import OrderedDict
import matplotlib.pyplot as plt
import pickle as pk


debut = gp.debut_soiree
fin = gp.fin_soiree
nb = gp.nb_commandes_soiree
listeParametres = gend.genere_parametres(gp.N_boissons)


listeCommandes_soiree = gend.genere_commandes_soiree(debut, fin, nb)

# voisinage complet
vect_plans_complet, vect_rush_complet, referenceAttente_complet, vect_listeCommandes_complet, vect_progression_complet, deltaTemps_complet = sims.simuleSoiree(listeCommandes_soiree, listeParametres, debut, maxIter=30000, alphaRefroidissement=0.9998, voisinage=tireVoisin_complet)

# voisinage réduit
vect_plans_reduit, vect_rush_reduit, referenceAttente_reduit, vect_listeCommandes_reduit, vect_progression_reduit, deltaTemps_reduit = sims.simuleSoiree(listeCommandes_soiree, listeParametres, debut, maxIter=30000, alphaRefroidissement=0.9998, voisinage=tireVoisin)


# Analyse
n_prog_complet = len(vect_progression_complet)
print(n_prog_complet)

i = 20
plt.figure()
plt.plot(vect_progression_complet[i][2], 'ro')
plt.figure()
plt.plot(vect_progression_complet[i][0] + vect_progression_complet[i][1], 'bo')
plt.show()

n_prog_reduit = len(vect_progression_reduit)
print(n_prog_reduit)

i = 20
plt.figure()
plt.plot(vect_progression_reduit[i][2], 'ro')
plt.figure()
plt.plot(vect_progression_reduit[i][0] + vect_progression_reduit[i][1], 'bo')
plt.show()