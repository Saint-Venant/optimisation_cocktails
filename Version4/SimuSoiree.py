'''
Fournit les outils nécessaires pour simuler une soirée, étant donnée une simulation d'arrivées de commandes
Test de l'algorithme sur le long terme :
    * de nouvelles commandes sont passées
    * certaines sont livrées au fur et à mesure que le temps avance
'''

from StructuresProduction import *
import GlobalParam as gp
from AlgoRecuit import *
import GenerationDonnees as gend
import OutilsGraphiques as outg
import numpy as np
import matplotlib.pyplot as plt



def simuleSoiree(liste_commandes_soiree, listeParametres, debut_soiree, attenteCommandeMoy, opti=1):
    '''
    opti = 1 : basique, pas d'optimisation
    opti = 2 : optimisation sans contrainte, simple groupement de boissons
    opti = 3 : optimisation avec contraintes, recuit simulé
    '''
    
    # le temps est discrétisé
    temps = debut_soiree
    
    # Initialisation
    liste_commandes_servies = []
    liste_commandes_en_cours = []
    liste_commandes_non_arrivees = liste_commandes_soiree.copy()
    
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
    cond_termine = len(liste_commandes_servies) == gp.nb_commandes_soiree
    
    while not(cond_termine):
        
        # incrémente le temps
        temps += 1
        if temps%50 == 0:
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
            
            if opti == 2:
                plan.ajouteCommandeUltraOpti(com)
            else:
                plan.ajouteCommande(com)
            
            cond2 = (len(liste_commandes_non_arrivees) > 0) and (liste_commandes_non_arrivees[0].instantCommande <= temps)
        
        # actualisation d'un paramètre de suivi
        vect_rush.append(len(plan.commandes))
        
        # lance un nouveau calcul d'optimisation/de la production si de nouvelles commandes sont arrivées
        if nouvArrivee:
            if opti == 3:
                plan, lProd, lAttente = Recuit3(plan, listeParametres, attenteCommandeMoy, maxIter=30000)
            calculeProduction(plan, listeParametres)
        
        # condition de terminaison de la boucle temporelle
        cond_termine = len(liste_commandes_servies) == gp.nb_commandes_soiree
        
        if temps >= 1000000:
            cond_termine = True
            print("problème")
    
    return plan, vect_rush


def simuleSoiree_complement(liste_commandes_soiree, listeParametres, debut_soiree):
    '''
    0 : pas d'optimisation
    1 : optimisation sans contrainte
    2 : optimisation avec contraintes
    '''
    
    # le temps est discrétisé
    temps = debut_soiree
    
    # copies indépendantes de la liste de commandes
    listeCommandes = [[x.copy() for x in liste_commandes_soiree] for i in range(3)]
    
    # Initialisation
    liste_commandes_servies = [[] for i in range(3)]
    liste_commandes_en_cours = [[] for i in range(3)]
    liste_commandes_non_arrivees = [[x.copy() for x in listeCommandes[i]] for i in range(3)]
    
    # plans de production
    vect_plans = [planProduction("soiree") for i in range(3)]
    
    for i in range(3):
        plan = vect_plans[i]
        
        # plan de production initial
        com = liste_commandes_non_arrivees[i][0]
        cond = True
        while cond and (com.instantCommande == temps):
            if i == 1:
                plan.ajouteCommandeUltraOpti(com)
            else:
                plan.ajouteCommande(com)
            liste_commandes_en_cours[i].append(com)
            liste_commandes_non_arrivees[i].remove(com)
            cond = len(liste_commandes_non_arrivees[i]) > 0
            if cond:
                com = liste_commandes_non_arrivees[i][0]

        # calcule la production initiale
        if len(liste_commandes_en_cours[i]) > 0:
            calculeProduction(plan, listeParametres)
    
    # nombre de commandes que le barman doit gérer en parallèle
    vect_rush = [[len(vect_plans[i].commandes)] for i in range(3)]
    
    # évolution des recuits successifs
    vect_progression = []
    
    # évolution du temps d'attente moyen calculé sur la base d'une organisation sans optimisation
    vect_attenteMoy = []
    
    # poursuit le calcul tant qu'il reste des commandes à livrer
    cond_termine = True
    for i in range(3):
        cond_termine = cond_termine and (len(liste_commandes_servies[i]) == gp.nb_commandes_soiree)
    
    # tableau stockant les temps d'attente de référence
    referenceAttente = np.zeros(len(liste_commandes_soiree))
    
    while not(cond_termine):
        
        # incrémente le temps
        temps += 1
        if temps%50 == 0:
            print("instant :", temps)
            #print(len(liste_commandes_servies), "commandes servies")
        
        # variables intermédiaires
        nouvArrivee = [False for i in range(3)]
        attenteMoy = 0
        
        for i in range(3):
            plan = vect_plans[i]
            
            # mise à jour du plan de production : sort les clusters déjà produits au moment considéré
            plan.update_livraison(temps)
            
             # sort les commandes qui peuvent être livrées
            cond1 = (len(liste_commandes_en_cours[i]) > 0) and (liste_commandes_en_cours[i][0].livraison <= temps)
            while cond1:
                com = liste_commandes_en_cours[i][0]
                
                liste_commandes_servies[i].append(com)
                del liste_commandes_en_cours[i][0]
                
                cond1 = (len(liste_commandes_en_cours[i]) > 0) and (liste_commandes_en_cours[i][0].livraison <= temps)
            
            # ajoute les éventuelles commandes qui auraient pu arriver
            cond2 = (len(liste_commandes_non_arrivees[i]) > 0) and (liste_commandes_non_arrivees[i][0].instantCommande <= temps)
            nouvArrivee[i] = cond2
            while cond2:
                com = liste_commandes_non_arrivees[i][0]
                
                liste_commandes_en_cours[i].append(com)
                del liste_commandes_non_arrivees[i][0]
                
                if i == 1:
                    plan.ajouteCommandeUltraOpti(com)
                else:
                    plan.ajouteCommande(com)
                
                cond2 = (len(liste_commandes_non_arrivees[i]) > 0) and (liste_commandes_non_arrivees[i][0].instantCommande <= temps)
            
            # actualisation des paramètres de suivi
            vect_rush[i].append(len(plan.commandes))
        
            # lance un nouveau calcul d'optimisation/de la production si de nouvelles commandes sont arrivées
            if nouvArrivee[i]:
                calculeProduction(plan, listeParametres)
                if i == 0:
                    # calcule la référence des temps d'attente
                    for com in vect_plans[0].commandes:
                        referenceAttente[com.num] = com.livraison - com.instantCommande
                if i == 2:
                    vect_plans[i], lProd, lAttente = Recuit3(plan, listeParametres, referenceAttente, maxIter=15000)
                    plan = vect_plans[i]
                    vect_progression.append([lProd, lAttente])
                calculeProduction(plan, listeParametres)
        
            # condition de terminaison de la boucle temporelle
            if i == 0:
                cond_termine = True
            cond_termine = cond_termine and (len(liste_commandes_servies[i]) == gp.nb_commandes_soiree)
        
        if temps >= 1000000:
            cond_termine = True
            print("problème")
    
    return vect_plans, vect_rush, referenceAttente, liste_commandes_servies, vect_progression