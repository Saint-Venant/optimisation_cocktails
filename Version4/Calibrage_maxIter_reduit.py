'''
Teste le bon paramètre maxIter pour le voisinage complet
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


#simulation de plusieurs soirées
nb_soirees = 2
vect_soirees = []
for i in range(nb_soirees):
    vect_soirees.append(gend.genere_commandes_soiree(debut, fin, gp.nb_commandes_soiree)

#stockage des solutions
vect_solutions = []


for i in range(nb_soirees):
    vect_plans, vect_rush, referenceAttente, vect_listeCommandes, vect_progression, deltaTemps = sims.simuleSoiree(listeCommandes_soiree, listeParametres, debut, maxIter=30000, voisinage=tireVoisin_complet)



