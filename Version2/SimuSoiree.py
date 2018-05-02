'''
Fournit les outils nécessaires pour simuler une soirée, étant donnée une simulation d'arrivées de commandes
Test de l'algorithme sur le long terme :
    * de nouvelles commandes sont passées
    * certaines sont livrées au fur et à mesure que le temps avance
'''


from Version2 import *
from Recuit2 import *
import OutilsTestSoiree as outs
import matplotlib.pyplot as plt
import numpy as np



def simuleSoiree(liste_commandes_soiree, listeParametres, debut_soiree, attenteCommandeMoy, opti=False):
    
    # le temps est discrétisé
    temps = debut_soiree
    
    # Initialisation
    liste_commandes_servies = []
    liste_commandes_en_cours = []
    liste_commandes_non_arrivees = outs.liste_commandes_soiree.copy()
    
    # plan de production initial
    plan = planProduction("soiree")
    com = liste_commandes_non_arrivees[0]
    cond = True
    while cond and (com.instantCommande == temps):
        plan.ajouteCommande(com)
        liste_commandes_en_cours.append(com)
        liste_commandes_non_arrivees.remove(com)
        cond = len(liste_commandes_non_arrivees) > 0
        if cond:
            com = liste_commandes_non_arrivees[0]
    
    #calcule la production initiale
    if len(liste_commandes_en_cours) > 0:
        calculeProduction(plan, listeParametres)
    
    # nombre de commandes que le barman doit gérer en parallèle
    vect_rush = [len(plan.commandes)]
    
    # poursuit le calcul tant qu'il reste des commandes à livrer
    cond_termine = len(liste_commandes_servies) == outs.nb_commandes_soiree
    
    while not(cond_termine):
        
        # incrémente le temps
        temps += 1
        if temps%10 == 0:
            print("instant :", temps)
            print(len(liste_commandes_servies), "commandes servies")
        
        # mise à jour du plan de production : sort les clusters déjà produits au moment considéré
        cl_supprimes = plan.update_livraison(temps)
        
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
            
            plan.ajouteCommande(com)
            
            cond2 = (len(liste_commandes_non_arrivees) > 0) and (liste_commandes_non_arrivees[0].instantCommande <= temps)
        
        # actualisation d'un paramètre de suivi
        vect_rush.append(len(plan.commandes))
        
        # lance un nouveau calcul d'optimisation/de la production si de nouvelles commandes sont arrivées
        if nouvArrivee:
            if opti:
                plan, lProd, lAttente = Recuit3(plan, listeParametres, attenteCommandeMoy, maxIter=30000)
            calculeProduction(plan, listeParametres)
        
        # condition de terminaison de la boucle temporelle
        cond_termine = len(liste_commandes_servies) == outs.nb_commandes_soiree
        
        if temps >= 100000:
            cond_termine = True
            print("problème")
    
    return plan, vect_rush


def calc_attenteCommande(liste_commandes_soiree):
    '''
    Calcule le temps d'attente avant livraison de chaque commande
    '''
    N = len(liste_commandes_soiree)
    Y_attente = np.zeros(N)
    for i in range(N):
        com = liste_commandes_soiree[i]
        Y_attente[i] = com.livraison - com.instantCommande
    attente_moy = np.mean(Y_attente)
    return Y_attente, attente_moy