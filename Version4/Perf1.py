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
listeParametres = gend.listeParametres


vect_listeCommandes_soiree = []
for i in range(3):
    vect_listeCommandes_soiree.append(gend.genere_commandes_soiree(debut, fin, nb))

vect_alpha = np.linspace(0.999, 0.99995, 3)

vect_solutions = []

for i in range(2):
    print("données ", i)
    vect_solutions.append([])
    for alpha in vect_alpha:
        print("  alpha :", alpha)
        x1, x2, x3, x4, x5 = sims.simuleSoiree(vect_listeCommandes_soiree[i], listeParametres, debut, alphaRefroidissement=alpha, maxIter=30000)
    l = [x1, x2, x3, x4, x5]
    vect_solutions[i].append(l)
    print()


with open("etudePerf1.pickle", "wb") as f:
    pk.dump(vect_solutions, f)


analyse = [[] for j in range(3)]
for j in range(3):
    for i in range(2):
        plan = vect_solutions[i][j][0][-1]
        ref = vect_solutions[i][j][2]
        x = energie4(plan, ref)
        analyse[j].append(x)