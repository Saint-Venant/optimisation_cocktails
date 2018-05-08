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

listeCommandesBasique = [x.copy() for x in gend.liste_commandes_soiree]
listeCommandesOpti = [x.copy() for x in gend.liste_commandes_soiree]
listeCommandesPlan = [x.copy() for x in gend.liste_commandes_soiree]
listeParametres = gend.listeParametres

debut_soiree = gp.debut_soiree


## Simulation d'une soirée : pas d'optimisation


# plan basique
planBasique, rush_soiree_Basique = sims.simuleSoiree(listeCommandesBasique, listeParametres, debut_soiree, 600, opti=1)
attenteBasique = outg.attente_commandes(listeCommandesBasique)
attenteMoyBasique = np.mean(attenteBasique[:,1])


# planning de production
plt.figure("planning de production basique")
outg.plot_planning(planBasique)
plt.show()


## Simulation d'une soirée : optimisation sans contrainte

# plan optimisé sans contrainte
planOpti, rush_soiree_Opti = sims.simuleSoiree(listeCommandesOpti, listeParametres, debut_soiree, 600, opti=2)
attenteOpti = outg.attente_commandes(listeCommandesOpti)
attenteMoyOpti = np.mean(attenteOpti[:,1])


# planning de production
plt.figure("planning optimisé sans contrainte")
outg.plot_planning(planOpti)
plt.show()

## Simulation d'une soirée : optimisation avec contraintes

# plan optimisé avec contraintes
plan, rush_soiree_Plan = sims.simuleSoiree(listeCommandesPlan, listeParametres, debut_soiree, 600, opti=3)
attentePlan = outg.attente_commandes(listeCommandesPlan)
attenteMoyPlan = np.mean(attentePlan[:,1])


# planning de production
plt.figure("planning de production optimisé avec contraintes")
outg.plot_planning(plan)
plt.show()





#temps d'attente par commande
plt.figure("attente commande")
vect_attentes = [attenteBasique, attenteOpti, attentePlan]
vect_labels = ["sans optimisation", "optimisation sans contrainte", "optimisation avec contraintes"]
param_moy = [len(listeCommandesBasique)*[attenteMoyBasique], len(listeCommandesBasique)*[1.1*attenteMoyBasique], "temps d'attente moyen basique", "temps d'attente moyen + 10%"]
outg.plot_attente_commandes(vect_attentes, vect_labels, param_moy)
plt.show()


# nombre de commandes gérées en même temps
plt.figure("rush")
vect_rush = [rush_soiree_Basique, rush_soiree_Opti, rush_soiree_Plan]
vect_labels = ["sans optimisation", "optimisation sans contrainte", "optimisation avec contraintes"]
outg.plot_rush(vect_rush, vect_labels)
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