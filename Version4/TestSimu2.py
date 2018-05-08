'''
Test la simulation d'une soirée, avec une optimisation en continue, à chaque nouvelle arrivée de commande
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


## Données générées

listeCommandes_soiree = [x.copy() for x in gend.liste_commandes_soiree]
listeParametres = gend.listeParametres

debut_soiree = gp.debut_soiree


## Simulation d'une soirée

vect_plans, vect_rush, referenceAttente, vect_listeCommandes, vect_progression = sims.simuleSoiree_complement(listeCommandes_soiree, listeParametres, debut_soiree)

planBasique = vect_plans[0]
planOpti = vect_plans[1]
plan = vect_plans[2]

listeCommandesBasique = vect_listeCommandes[0]
listeCommandesOpti = vect_listeCommandes[1]
listeCommandesPlan = vect_listeCommandes[2]



# planning de production
plt.figure("planning de production : sans optimisation")
outg.plot_planning(planBasique)
plt.show()

plt.figure("planning de production : optimisation sans contrainte")
outg.plot_planning(planOpti)
plt.show()

plt.figure("planning de production : optimisation avec contraintes")
outg.plot_planning(plan)
plt.show()


# comparaison des performances : temps total de la soirée
tempsSoireeBasique = planBasique.histoire[-1][-1].fin - debut_soiree
tempsSoireeOpti = planOpti.histoire[-1][-1].fin - debut_soiree
tempsSoireePlan = plan.histoire[-1][-1].fin - debut_soiree
print()
print("temps soiree Basique :", tempsSoireeBasique)
print("temps soiree Opti :", tempsSoireeOpti)
print("temps soiree Plan :", tempsSoireePlan)
print("gain de productivité :")
print("  Opti > ", outg.arrondi((tempsSoireeBasique - tempsSoireeOpti)*100/tempsSoireeBasique, 2), "%")
print("  Plan > ", outg.arrondi((tempsSoireeBasique - tempsSoireePlan)*100/tempsSoireeBasique, 2), "%")


#temps d'attente par commande
plt.figure("attente commande")
vect_attentes = []
for i in range(3):
    vect_attentes.append(outg.attente_commandes(vect_listeCommandes[i]))
vect_labels = ["sans optimisation", "optimisation sans contrainte", "optimisation avec contraintes"]
param_moy = [referenceAttente, [1.1*x for x in referenceAttente], "temps d'attente moyen basique", "temps d'attente moyen + 10%"]
outg.plot_attente_commandes(vect_attentes, vect_labels, param_moy)
plt.show()


# nombre de commandes gérées en même temps
plt.figure("rush")
vect_labels = ["sans optimisation", "optimisation sans contrainte", "optimisation avec contraintes"]
outg.plot_rush(vect_rush, vect_labels)
plt.show()

'''# progression des recuits successifs
vect_labels = ["temps total production", "énergie hybride"]
for i in range(len(vect_progression)):
    lProd, lAttente = vect_progression[i]
    vectEnergie = [lProd, lProd+lAttente]
    plt.figure("progression du recuit " + str(i))
    outg.plot_recuit(vectEnergie, vect_labels)
    plt.show()'''