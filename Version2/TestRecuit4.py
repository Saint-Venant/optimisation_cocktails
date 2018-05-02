'''
Test de l'algorithme sur le long terme :
    * de nouvelles commandes sont passées
    * certaines sont livrées au fur et à mesure que le temps avance
'''

from Version2 import *
from Recuit2 import *
from GenerationDonnees2 import *
import OutilsTestSoiree as outs
import matplotlib.pyplot as plt
import numpy as np



## Initialisation

liste_commandes_servies = []
liste_commandes_en_cours = []
liste_commandes_non_arrivees = outs.liste_commandes_soiree.copy()


## Laisse courir le temps

temps = outs.debut_soiree

# réalise le premier plan de production

#planBasique = planProduction("soiree")
planSimu = planProduction("soiree")
com = liste_commandes_non_arrivees[0]
cond = True
while cond and (com.instantCommande == temps):
    #planBasique.ajouteCommande(com)
    planSimu.ajouteCommande(com)
    liste_commandes_en_cours.append(com)
    liste_commandes_non_arrivees.remove(com)
    cond = len(liste_commandes_non_arrivees) > 0
    if cond:
        com = liste_commandes_non_arrivees[0]

#calcule la production
if len(liste_commandes_en_cours) > 0:
    #calculeProduction(planBasique, listeParametres)
    calculeProduction(planSimu, listeParametres)
    

# poursuit le calcul tant qu'il reste des commandes à livrer
cond_termine = len(liste_commandes_servies) == outs.nb_commandes_soiree

# nombre de commandes que le barman doit gérer en parallèle
#vect_rush_Basique = [len(planBasique.commandes)]
vect_rush_Simu = [len(planSimu.commandes)]


while not(cond_termine):
    
    # incrémente le temps
    temps += 1
    
    # mise à jour du plan de production : sort les clusters déjà produits au moment considéré
    #cl_supprimes = planBasique.update_livraison(temps)
    cl_supprimes = planSimu.update_livraison(temps)
    
    # sort les commandes qui peuvent être livrées
    cond1 = (len(liste_commandes_en_cours) > 0) and (liste_commandes_en_cours[0].livraison <= temps)
    while cond1:
        com = liste_commandes_en_cours[0]
        
        liste_commandes_servies.append(com)
        del liste_commandes_en_cours[0]
        
        cond1 = (len(liste_commandes_en_cours) > 0) and (liste_commandes_en_cours[0].livraison <= temps)
    
    # ajoute les éventuelles commandes qui auraient pu arriver
    cond2 = (len(liste_commandes_non_arrivees) > 0) and (liste_commandes_non_arrivees[0].instantCommande <= temps)
    nouvArrivee = False
    while cond2:
        nouvArrivee = True
        
        com = liste_commandes_non_arrivees[0]
        
        liste_commandes_en_cours.append(com)
        del liste_commandes_non_arrivees[0]
        
        #planBasique.ajouteCommande(com)
        planSimu.ajouteCommande(com)
        
        cond2 = (len(liste_commandes_non_arrivees) > 0) and (liste_commandes_non_arrivees[0].instantCommande <= temps)
    
    # actualisation d'un paramètre de suivi
    #vect_rush_Basique.append(len(planBasique.commandes))
    vect_rush_Simu.append(len(planSimu.commandes))
    
    # lance un nouveau calcul d'optimisation/de la production si de nouvelles commandes sont arrivées
    if nouvArrivee:
        #calculeProduction(planBasique, listeParametres)
        calculeProduction(planSimu, listeParametres)
    
    # condition de terminaison de la boucle temporelle
    cond_termine = len(liste_commandes_servies) == outs.nb_commandes_soiree
    
    if temps >= 100000:
        cond_termine = True
        print("problème")


## Performances sur le plan basique
'''
#temps d'attente par commande
Y_tempsAttenteBasique = []
for i in range(0, len(outs.liste_commandes_soiree)):
    com = outs.liste_commandes_soiree[i]
    Y_tempsAttenteBasique.append(com.livraison - com.instantCommande)
tempsAttenteCommandeMoyen = sum(Y_tempsAttenteBasique)/len(Y_tempsAttenteBasique)
'''

#temps d'attente par commande
Y_tempsAttenteSimu = []
for i in range(0, len(outs.liste_commandes_soiree)):
    com = outs.liste_commandes_soiree[i]
    Y_tempsAttenteSimu.append(com.livraison - com.instantCommande)
tempsAttenteCommandeMoyen = sum(Y_tempsAttenteSimu)/len(Y_tempsAttenteSimu)



#planning de production
plt.figure(1)
indexCouleurs = {}
for com in outs.liste_commandes_soiree:
    c = np.random.rand(3,)
    indexCouleurs[com] = c
for cl in planSimu.histoire:
    b1 = cl[0]
    b2 = cl[-1]
    plt.axvline(x=b1.debut, c='k', linestyle='--')
    plt.axvline(x=b2.fin, c='k', linestyle='--')
    for b in cl:
        num = b.commande.num
        plt.plot([b1.debut, b2.fin], [num, num], color=indexCouleurs[b.commande], linewidth=10)
fin = planSimu.histoire[-1][0].fin
plt.axis([outs.debut_soiree, fin, -1, len(outs.liste_commandes_soiree)])
plt.title("Planning de production des commandes : plan basique")
plt.xlabel("temps")
plt.ylabel("indice de commande")
plt.show()


#temps d'attente par commande
plt.figure(2)
plt.plot(Y_tempsAttenteSimu, 'bo', label="plan basique")
plt.plot(outs.nb_commandes_soiree*[tempsAttenteCommandeMoyen], 'k-', label="temps d'attente moyen")
plt.plot(outs.nb_commandes_soiree*[1.1*tempsAttenteCommandeMoyen], 'k--', label="temps d'attente moyen + 10%")
xmin = 0
xmax = len(Y_tempsAttenteSimu)-1
ymin = 0
ymax = max(Y_tempsAttenteSimu) + 50
plt.axis([xmin, xmax, ymin, ymax])
plt.xlabel("commandes")
plt.ylabel("temps d'attente")
plt.title("Temps d'attente par commande")
plt.legend()
plt.show()


# nombre de commandes gérées en même temps
plt.figure()
plt.plot(vect_rush_Simu, c='b', label='plan simulé')
plt.title("Nombre de commandes en attentes")
plt.xlabel("temps")
plt.ylabel("nombre de commandes")
plt.legend()
plt.show()