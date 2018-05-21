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
listeParametres = gend.genere_parametres(gp.nb_commandes_soiree)


vect_maxIter = np.array([5000, 15000, 25000, 40000])
nbTest = len(vect_maxIter)

vect_listeCommandes_soiree = []
for i in range(nbTest):
    vect_listeCommandes_soiree.append(gend.genere_commandes_soiree(debut, fin, nb))

vect_solutions = []
for i in range(

