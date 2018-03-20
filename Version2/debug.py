from Version2 import *
from GenerationDonnees2 import *
import numpy as np
import random
import matplotlib.pyplot as plt

## Plan de production optimisé au max, sans contrainte

planUltraOpti = planProduction()
for com in listeCommandes:
    planUltraOpti.ajouteCommandeUltraOpti(com)
print()
print("Plan de production optimisé sans contrainte")
planUltraOpti.affichePlan()
calculeProduction(planUltraOpti, listeCommandes, listeParametres)