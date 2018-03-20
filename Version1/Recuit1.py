from Version1 import *
import random
import numpy as np

random.seed(3)

## Définition des contraintes

#temps max d'attente d'une boisson préparée avant sa livraison (afin de garantir sa fraicheur)
tempsFraicheur = 100

#coefficient de pénalisation des attentes clients trop longues
penalisationAttente = 0.05



'''
Fonction permettant de vérifier si un plan de production donné respecte les contraintes
'''
def verifieContraintes(listeCommandes):
    #suppose que la mise à jour des variables intermédiaires calculées selon le plan de production souhaité est faite
    
    respect = True
    indiceCommande = 0
    while respect and (indiceCommande < len(listeCommandes)):
        #contrainte fraicheur
        for b in listeCommandes[indiceCommande].listeBoissons:
            respect = respect and (b.livraison - b.fin <= tempsFraicheur)
        
        indiceCommande += 1
    
    return respect


## Fonction d'énergie

'''Définition de l'énergie = temps total de préparation
>> point de vue de la production uniquement
'''

def energie1(listeCommandes):
    #suppose que la mise à jour des variables intermédiaires calculées selon le plan de production souhaité est faite
    
    tempsFinProduction = 0
    for com in listeCommandes:
        tempsFinProduction = max(tempsFinProduction, com.livraison)
    
    return tempsFinProduction


'''Définition de l'énergie :
>> temps total de production
>> pénalisation du surcroît d'attente des clients
'''

def energie2(listeCommandes, tempsAttenteCommandeMoyen):
    #suppose que la mise à jour des variables intermédiaires calculées selon le plan de production souhaité est faite
    
    tempsFinProduction = 0
    coutAttente = 0
    for com in listeCommandes:
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

def tireVoisin(plan, indexBoissons):
    #fait une copie de l'ancien plan de production
    nouveauPlan = plan.copy()
    
    #tire au sort une boisson : repérée par i0 et j0 dans les matrices matBoissons
    #  où les commandes sont évidemment triées
    numBoisson = random.randint(0, len(indexBoissons)-1)
    #print(numBoisson)
    [i0, j0] = indexBoissons[numBoisson]
    #print("  ", i0, ",", j0)
    b = nouveauPlan.matBoissons[i0][j0]
    
    #tire au sort une nouvelle affectation de clusters : qui doit produire des boissons de même type que la boisson tirée
    ancienCluster = nouveauPlan.matProd[i0][j0]
    nouvCluster = random.randint(0, nouveauPlan.nbClusters)
    while (nouvCluster < nouveauPlan.nbClusters) and (b.id != nouveauPlan.clusters[nouvCluster][0].id):
        nouvCluster = random.randint(0, nouveauPlan.nbClusters)
    
    if (nouvCluster == ancienCluster):
        pass
    else:
        nouveauPlan.matProd[i0][j0] = nouvCluster
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
            for i in range(0, len(nouveauPlan.matProd)):
                for j in range(0, len(nouveauPlan.matProd[i])):
                    if (nouveauPlan.matProd[i][j] > ancienCluster):
                        nouveauPlan.matProd[i][j] -= decalage
                        
            
        #met à jour le nombre de clusters
        if (nouvCluster == nouveauPlan.nbClusters):
            nouveauPlan.nbClusters += (1 - decalage)
        else:
            nouveauPlan.nbClusters -= decalage
    
    nouveauPlan.updateClusters()
    return nouveauPlan



## Recuit simulé sans contrainte

def Recuit1(listeCommandes, listeParametres, indexBoissons, maxIter=100000):
    
    #initialisation
    plan = planProduction()
    for com in listeCommandes:
        plan.ajouteCommande(com)
    calculeProduction(plan, listeCommandes, listeParametres)
    energie = energie1(listeCommandes)
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
        planBis = tireVoisin(plan, indexBoissons)
        calculeProduction(planBis, listeCommandes, listeParametres)
        energieBis = energie1(listeCommandes)
        
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
        
        #incrément de temps
        iter += 1
        temperature *= alphaRefroidissement
        listeEnergie.append(energie)
        
        #sauvegarde du minimum
        if (energie < energieMin):
            planMin = plan.copy()
            energieMin = energie
    
    return planMin, listeEnergie

## Recuit simulé avec contraintes


def Recuit2(listeCommandes, listeParametres, indexBoissons, tempsAttenteCommandeMoyen, maxIter=100000):
    '''
    Intègre la contrainte de fraîcheur dans le recuit
    '''
    
    #initialisation
    plan = planProduction()
    for com in listeCommandes:
        plan.ajouteCommande(com)
    calculeProduction(plan, listeCommandes, listeParametres)
    energie = energie1(listeCommandes)
    coutProd, coutAttente = energie2(listeCommandes, tempsAttenteCommandeMoyen)
    coutProdBis, coutAttenteBis = coutProd, coutAttente
    listeCoutProd = []
    listeCoutAttente = []
    
    #paramètres initiaux
    temperatureInitiale = 20
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
            print("itération ", iter, "(", iter/maxIter*100, "%),  energie2 =", energie)
        
        #explore un plan de production voisin
        planBis = tireVoisin(plan, indexBoissons)
        calculeProduction(planBis, listeCommandes, listeParametres)
        
        respectContraintes = verifieContraintes(listeCommandes)
        while not(respectContraintes):
            planBis = tireVoisin(plan, indexBoissons)
            calculeProduction(planBis, listeCommandes, listeParametres)
            respectContraintes = verifieContraintes(listeCommandes)
        coutProdBis, coutAttenteBis = energie2(listeCommandes, tempsAttenteCommandeMoyen)
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

        
        #incrément de temps
        iter += 1
        temperature *= alphaRefroidissement
        listeCoutProd.append(coutProd)
        listeCoutAttente.append(coutAttente)
        
        #sauvegarde du minimum
        if (energie < energieMin):
            planMin = plan.copy()
            energieMin = energie
    
    return planMin, listeCoutProd, listeCoutAttente


## Recuit simulé partant d'une solution déjà calculée



def Recuit3(planDepart, listeCommandes, listeParametres, indexBoissons, tempsAttenteCommandeMoyen, maxIter=100000):
    '''
    Initialisation au plan passé en paramètres
    '''
    
    #initialisation
    plan = planDepart.copy()
    calculeProduction(plan, listeCommandes, listeParametres)
    energie = energie1(listeCommandes)
    coutProd, coutAttente = energie2(listeCommandes, tempsAttenteCommandeMoyen)
    coutProdBis, coutAttenteBis = coutProd, coutAttente
    listeCoutProd = []
    listeCoutAttente = []
    
    #paramètres initiaux
    temperatureInitiale = 20
    alphaRefroidissement = 0.9999
    
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
        
        #explore un plan de production voisin
        planBis = tireVoisin(plan, indexBoissons)
        calculeProduction(planBis, listeCommandes, listeParametres)
        
        respectContraintes = verifieContraintes(listeCommandes)
        while not(respectContraintes):
            planBis = tireVoisin(plan, indexBoissons)
            calculeProduction(planBis, listeCommandes, listeParametres)
            respectContraintes = verifieContraintes(listeCommandes)
        coutProdBis, coutAttenteBis = energie2(listeCommandes, tempsAttenteCommandeMoyen)
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

        
        #incrément de temps
        iter += 1
        temperature *= alphaRefroidissement
        listeCoutProd.append(coutProd)
        listeCoutAttente.append(coutAttente)
        
        #sauvegarde du minimum
        if (energie < energieMin):
            planMin = plan.copy()
            energieMin = energie
    
    return planMin, listeCoutProd, listeCoutAttente












