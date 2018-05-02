from Version2 import *
import random
import numpy as np


## Définition des contraintes

#temps max d'attente d'une boisson préparée avant sa livraison (afin de garantir sa fraicheur)
tempsFraicheur = 200

#coefficient de pénalisation des attentes clients trop longues
penalisationAttente = 0#0.00005



'''
Fonction permettant de vérifier si un plan de production donné respecte les contraintes
'''
def verifieContraintes(plan):
    #suppose que la mise à jour des variables intermédiaires calculées selon le plan de production souhaité est faite
    
    respect = True
    '''indiceCommande = 0
    while respect and (indiceCommande < len(listeCommandes)):
        #contrainte fraicheur
        for b in listeCommandes[indiceCommande].listeBoissons:
            respect = respect and (b.livraison - b.fin <= tempsFraicheur)
        
        indiceCommande += 1
    
    return respect'''
    liste_b = list(plan.matProd.keys())
    indice = 0
    while respect and (indice < len(liste_b)):
        b = liste_b[indice]
        #contrainte fraicheur
        respect = respect and (b.livraison - b.fin <= tempsFraicheur)
        indice += 1
    
    return respect


## Fonction d'énergie

'''Définition de l'énergie = temps total de préparation
>> point de vue de la production uniquement
'''

def energie1(plan):
    #suppose que la mise à jour des variables intermédiaires calculées selon le plan de production souhaité est faite
    
    '''tempsFinProduction = 0
    for com in listeCommandes:
        tempsFinProduction = max(tempsFinProduction, com.livraison)'''
    tempsFinProduction = plan.instantProd
    for b in plan.matProd:
        tempsFinProduction = max(tempsFinProduction, b.livraison)
    
    return tempsFinProduction


'''Définition de l'énergie :
>> temps total de production
>> pénalisation du surcroît d'attente des clients
'''

def energie2(plan, tempsAttenteCommandeMoyen):
    #suppose que la mise à jour des variables intermédiaires calculées selon le plan de production souhaité est faite
    
    '''tempsFinProduction = 0
    coutAttente = 0
    for com in listeCommandes:
        tempsFinProduction = max(tempsFinProduction, com.livraison)
        attente = com.livraison - com.instantCommande
        if (attente > 1.1*tempsAttenteCommandeMoyen):
            coutAttente += penalisationAttente * (attente - 1.1*tempsAttenteCommandeMoyen)**2'''
    tempsFinProduction = 0
    coutAttente = 0
    for b in plan.matProd:
        com = b.commande
        tempsFinProduction = max(tempsFinProduction, com.livraison)
        attente = com.livraison - com.instantCommande
        if (attente > 1.1*tempsAttenteCommandeMoyen):
            coutAttente += penalisationAttente * (attente - 1.1*tempsAttenteCommandeMoyen)**2
    
    return tempsFinProduction, coutAttente



## Voisinage

'''Voisinage :
    * changer l'affectation d'un matProd[i][j]
    * peut conduire à ajouter ou supprimer un cluster
'''

def tireVoisin(plan):
    #fait une copie de l'ancien plan de production
    nouveauPlan = plan.copy()
    
    #tire au sort une boisson : repérée par i0 et j0 dans les matrices matBoissons
    #  où les commandes sont évidemment triées
    '''numBoisson = random.randint(0, len(indexBoissons)-1)
    [i0, j0] = indexBoissons[numBoisson]
    com = listeCommandes[i0]
    b = com.getBoisson(j0)'''
    j0 = random.randint(0, len(nouveauPlan.matProd)-1)
    b = list(nouveauPlan.matProd.keys())[j0]
    
    #tire au sort une nouvelle affectation de clusters : qui doit produire des boissons de même type que la boisson tirée
    '''ancienCluster = nouveauPlan.matProd[com][j0]'''
    ancienCluster = nouveauPlan.matProd[b]
    nouvCluster = random.randint(0, nouveauPlan.nbClusters)
    while (nouvCluster < nouveauPlan.nbClusters) and (b.id != nouveauPlan.clusters[nouvCluster][0].id):
        nouvCluster = random.randint(0, nouveauPlan.nbClusters)
    
    if (nouvCluster == ancienCluster):
        pass
    else:
        '''nouveauPlan.matProd[com][j0] = nouvCluster'''
        nouveauPlan.matProd[b] = nouvCluster
        decalage = 0
        if (nouvCluster == nouveauPlan.nbClusters):
            #crée un nouveau cluster à la fin de la liste (évite des problèmes d'indice plus tard)
            nouveauPlan.clusters.append([b])
        
        #vérifie que l'ancien cluster n'est pas vide
        if (len(nouveauPlan.clusters[ancienCluster]) == 1):
            #procède à un décalage d'indice
            decalage = 1
            
            if (ancienCluster > 0) and (ancienCluster < nouveauPlan.nbClusters-1):
                clAvant = nouveauPlan.clusters[ancienCluster-1]
                clApres = nouveauPlan.clusters[ancienCluster+1]
                if (clAvant[0].id == clApres[0].id):
                    #joint les deux clusters : décalage de 2
                    decalage = 2
            
            #décalage
            '''for i in range(0, len(listeCommandes)):
                c = listeCommandes[i]
                for j in range(0, len(c.listeBoissons)):
                    if (nouveauPlan.matProd[c][j] > ancienCluster):
                        nouveauPlan.matProd[c][j] -= decalage'''
            for bois in nouveauPlan.matProd:
                if (nouveauPlan.matProd[bois] > ancienCluster):
                    nouveauPlan.matProd[bois] -= decalage
                        
            
        #met à jour le nombre de clusters
        if (nouvCluster == nouveauPlan.nbClusters):
            nouveauPlan.nbClusters += (1 - decalage)
        else:
            nouveauPlan.nbClusters -= decalage
        
        '''
        nouveauPlan.matProd[b] = nouvCluster
        if nouvCluster == nouveauPlan.nbClusters:
            nouveauPlan.nbClusters += 1
    
        # met à jour la liste des clusters, avec des ajustements
        nouveauPlan.clusters = [[] for x in range(nouveauPlan.nbClusters)]
        for bois in nouveauPlan.matProd:
            nouveauPlan.clusters[nouveauPlan.matProd[bois]].append(bois)
        # vérifie que le décalage n'a pas créé de cluster vide
        decalage = 0
        if len(nouveauPlan.clusters[ancienCluster]) == 0:
            decalage += 1
        # vérifie que l'on ne crée pas deux clusters de types identiques côte à côte
        if (ancienCluster > 0) and (ancienCluster < nouveauPlan.nbClusters - 1):
            # l'ancien cluster était à l'intérieur
            clAvant = nouveauPlan.clusters[ancienCluster-1]
            clApres = nouveauPlan.clusters[ancienCluster+1]
            if (decalage == 1) and (clAvant[0].id == clApres[0].id):
                decalage += 1
        
        # procède au décalage d'indices
        nouveauPlan.nbClusters -= decalage
        nouveauPlan.clusters = [[] for x in range(nouveauPlan.nbClusters)]
        for bois in nouveauPlan.matProd:
            if nouveauPlan.matProd[bois] > ancienCluster:
                nouveauPlan.matProd[bois] -= decalage
            nouveauPlan.clusters[nouveauPlan.matProd[bois]].append(bois)'''
    
    
    nouveauPlan.updateClusters()
    return nouveauPlan



## Recuit simulé sans contrainte

def Recuit1(listeCommandes, listeParametres, indexBoissons, maxIter=100000):
    
    #initialisation
    plan = planProduction("buffer")
    for com in listeCommandes:
        plan.ajouteCommande(com)
    calculeProduction(plan, listeParametres)
    energie = energie1(plan)
    listeEnergie = []
    
    #paramètres initiaux
    temperatureInitiale = 10
    alphaRefroidissement = 0.99995
    
    #variables intermédiaires
    energieBis = energie
    planBis = plan.copy()
    iter = 0
    temperature = temperatureInitiale
    
    #maintien en mémoire du plan qui donne l'énergie minimum
    planMin = plan.copy()
    energieMin = energie
    
    while (iter < maxIter):
        
        #monitoring de la progression
        if (iter%5000 == 0):
            print("itération ", iter, "(", iter/maxIter*100, "%),  energie1 =", energie)
        
        #explore un plan de production voisin
        planBis = tireVoisin(plan)
        calculeProduction(planBis, listeParametres)
        energieBis = energie1(planBis)
        
        if (energieBis <= energie):
            #alors on accepte la transition
            plan = planBis
            energie = energieBis
        else:
            proba = random.random()
            deltaE = energieBis - energie
            seuil = np.exp(-deltaE/temperature)
            
            if (proba <= seuil):
                #accepte quand même la transition
                plan = planBis
                energie = energieBis
        
        #sauvegarde du minimum
        if (energie < energieMin):
            planMin = plan.copy()
            energieMin = energie
        
        #incrément de temps
        iter += 1
        temperature *= alphaRefroidissement
        listeEnergie.append(energie)
    
    return planMin, listeEnergie

## Recuit simulé avec contraintes


def Recuit2(listeCommandes, listeParametres, indexBoissons, tempsAttenteCommandeMoyen, maxIter=100000):
    '''
    Intègre la contrainte de fraîcheur dans le recuit
    '''
    random.seed(1)
    
    #initialisation
    plan = planProduction("buffer")
    for com in listeCommandes:
        plan.ajouteCommande(com)
    calculeProduction(plan, listeParametres)
    energie = energie1(plan)
    coutProd, coutAttente = energie2(plan, tempsAttenteCommandeMoyen)
    coutProdBis, coutAttenteBis = coutProd, coutAttente
    listeCoutProd = []
    listeCoutAttente = []
    
    #paramètres initiaux
    temperatureInitiale = 20
    alphaRefroidissement = 0.99996
    
    #variables intermédiaires
    energieBis = energie
    planBis = plan.copy()
    iter = 0
    temperature = temperatureInitiale
    
    #maintien en mémoire du plan qui donne l'énergie minimum
    planMin = plan.copy()
    energieMin = energie
    
    while (iter < maxIter):
        
        #monitoring de la progression
        if (iter%5000 == 0):
            print("itération ", iter, "(", iter/maxIter*100, "%),  energie2 =", energie)
            #print("energieMin = ", energieMin)
        
        #explore un plan de production voisin
        planBis = tireVoisin(plan)
        calculeProduction(planBis, listeParametres)
        
        respectContraintes = verifieContraintes(planBis)
        while not(respectContraintes):
            planBis = tireVoisin(plan)
            calculeProduction(planBis, listeParametres)
            respectContraintes = verifieContraintes(planBis)
        coutProdBis, coutAttenteBis = energie2(planBis, tempsAttenteCommandeMoyen)
        energieBis = coutProdBis + coutAttenteBis
        
        if (energieBis <= energie):
            #alors on accepte la transition
            plan = planBis
            energie = energieBis
            coutProd, coutAttente = coutProdBis, coutAttenteBis
        else:
            proba = random.random()
            deltaE = energieBis - energie
            seuil = np.exp(-deltaE/temperature)
            
            if (proba <= seuil):
                #accepte quand même la transition
                plan = planBis
                energie = energieBis
                coutProd, coutAttente = coutProdBis, coutAttenteBis
        
        #sauvegarde du minimum
        if (energie < energieMin):
            #print("sauvegarde")
            planMin = plan.copy()
            energieMin = energie
        
        #incrément de temps
        iter += 1
        temperature *= alphaRefroidissement
        listeCoutProd.append(coutProd)
        listeCoutAttente.append(coutAttente)
    
    #print("enerieMin =", energieMin)
        
    return planMin, listeCoutProd, listeCoutAttente


## Recuit simulé partant d'une solution déjà calculée



def Recuit3(planDepart, listeParametres, tempsAttenteCommandeMoyen, maxIter=100000):
    '''
    Initialisation au plan passé en paramètres
    '''
    
    #initialisation
    plan = planDepart.copy()
    calculeProduction(plan, listeParametres)
    energie = energie1(plan)
    coutProd, coutAttente = energie2(plan, tempsAttenteCommandeMoyen)
    coutProdBis, coutAttenteBis = coutProd, coutAttente
    listeCoutProd = []
    listeCoutAttente = []
    
    #paramètres initiaux
    temperatureInitiale = 20
    alphaRefroidissement = 0.9995
    
    #variables intermédiaires
    energieBis = energie
    planBis = plan.copy()
    iter = 0
    temperature = temperatureInitiale
    
    #maintien en mémoire du plan qui donne l'énergie minimum
    planMin = plan.copy()
    energieMin = energie
    
    while (iter < maxIter):
        
        #monitoring de la progression
        if (iter%5000 == 0):
            #print("itération ", iter, "(", iter/maxIter*100, "%),  energie2 =", energie)
            pass
        
        #explore un plan de production voisin
        planBis = tireVoisin(plan)
        calculeProduction(planBis, listeParametres)
        
        respectContraintes = verifieContraintes(planBis)
        while not(respectContraintes):
            planBis = tireVoisin(plan)
            calculeProduction(planBis, listeParametres)
            respectContraintes = verifieContraintes(planBis)
        coutProdBis, coutAttenteBis = energie2(planBis, tempsAttenteCommandeMoyen)
        energieBis = coutProdBis + coutAttenteBis
        
        if (energieBis <= energie):
            #alors on accepte la transition
            plan = planBis
            energie = energieBis
            coutProd, coutAttente = coutProdBis, coutAttenteBis
        else:
            proba = random.random()
            deltaE = energieBis - energie
            seuil = np.exp(-deltaE/temperature)
            
            if (proba <= seuil):
                #accepte quand même la transition
                plan = planBis
                energie = energieBis
                coutProd, coutAttente = coutProdBis, coutAttenteBis

        
        #incrément d'itération
        iter += 1
        temperature *= alphaRefroidissement
        listeCoutProd.append(coutProd)
        listeCoutAttente.append(coutAttente)
        
        #sauvegarde du minimum
        if (energie < energieMin):
            planMin = plan.copy()
            energieMin = energie
    
    return planMin, listeCoutProd, listeCoutAttente












