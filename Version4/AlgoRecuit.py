from StructuresProduction import *
import GlobalParam as gp
import numpy as np


np.random.seed(1)



## Vérification du respect des contraintes

'''
Fonction permettant de vérifier si un plan de production donné respecte les contraintes
'''
def verifieContraintes(plan):
    #suppose que la mise à jour des variables intermédiaires calculées selon le plan de production souhaité est faite
    
    respect = True
    #parcourt les boissons en cours de production
    liste_b = list(plan.matProd.keys())
    indice = 0
    while respect and (indice < len(liste_b)):
        b = liste_b[indice]
        #contrainte fraicheur
        respect = respect and (b.livraison - b.fin <= gp.tempsFraicheur)
        indice += 1
    #parcourt les boissons déjà produites
    indiceCluster = len(plan.histoire)-1
    while respect and (indiceCluster >= 0):
        cl = plan.histoire[indiceCluster]
        for b in cl:
            #contrainte fraicheur
            respect = respect and (b.livraison - b.fin <= gp.tempsFraicheur)
        indiceCluster -= 1
    
    return respect


## Fonctions d'énergie

'''Définition de l'énergie = temps total de préparation
>> point de vue de la production uniquement
'''

def energie1(plan):
    #suppose que la mise à jour des variables intermédiaires calculées selon le plan de production souhaité est faite
    
    tempsProduction = 0
    if plan.nbClusters > 0:
        tempsProduction = plan.clusters[-1][-1].fin# - plan.instantProd
    
    return tempsProduction


'''Définition de l'énergie :
>> temps total de production
>> pénalisation du surcroît d'attente des clients par rapport à un temps de référence identique pour toutes les commandes
'''

def energie2(plan, tempsAttenteCommandeMoyen):
    #suppose que la mise à jour des variables intermédiaires calculées selon le plan de production souhaité est faite
    
    tempsProduction = 0
    if plan.nbClusters > 0:
        tempsProduction = plan.clusters[-1][-1].fin - plan.instantProd
    coutAttente = 0
    for com in plan.commandes:
        attente = com.livraison - com.instantCommande
        if (attente > 1.1*tempsAttenteCommandeMoyen):
            coutAttente += gp.penalisationAttente * (attente - 1.1*tempsAttenteCommandeMoyen)**2
    
    return tempsProduction, coutAttente

'''Définition de l'énergie :
>> temps total de production
>> pénalisation du surcroît d'attente des clients par rapport à un temps de référence spécifique à chaque commande
'''

def energie3(plan, referenceAttentes):
    #suppose que la mise à jour des variables intermédiaires calculées selon le plan de production souhaité est faite
    
    tempsProduction = 0
    coef = 1.2
    if plan.nbClusters > 0:
        tempsProduction = plan.clusters[-1][-1].fin - plan.instantProd
    coutAttente = 0
    for com in plan.commandes:
        attente = com.livraison - com.instantCommande
        borne = coef * referenceAttentes[com.num]
        if (attente > borne):
            coutAttente += gp.penalisationAttente * (attente - borne)**2
    
    return tempsProduction, coutAttente



## Voisinage

'''Voisinage :
    * changer l'affectation d'un matProd[b]
    * peut conduire à ajouter ou supprimer un cluster
'''

def tireVoisin(plan):
    #fait une copie de l'ancien plan de production
    nouveauPlan = plan.copy()
    
    #tire au sort une boisson
    j0 = np.random.randint(len(nouveauPlan.matProd))
    b = list(nouveauPlan.matProd.keys())[j0]
    
    #tire au sort une nouvelle affectation de clusters : qui doit produire des boissons de même type que la boisson tirée
    ancienCluster = nouveauPlan.matProd[b]
    nouvCluster = np.random.randint(nouveauPlan.nbClusters+1)
    while (nouvCluster < nouveauPlan.nbClusters) and (b.id != nouveauPlan.clusters[nouvCluster][0].id):
        nouvCluster = np.random.randint(nouveauPlan.nbClusters+1)
    
    if (nouvCluster == ancienCluster):
        pass
    else:
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
            for bois in nouveauPlan.matProd:
                if (nouveauPlan.matProd[bois] > ancienCluster):
                    nouveauPlan.matProd[bois] -= decalage
                        
            
        #met à jour le nombre de clusters
        if (nouvCluster == nouveauPlan.nbClusters):
            nouveauPlan.nbClusters += (1 - decalage)
        else:
            nouveauPlan.nbClusters -= decalage
    
    nouveauPlan.updateClusters()
    return nouveauPlan



## Recuit simulé sans contrainte

def Recuit1(listeCommandes, listeParametres, maxIter=100000):
    
    #initialisation
    plan = planProduction("buffer")
    for com in listeCommandes:
        plan.ajouteCommande(com)
    calculeProduction(plan, listeParametres)
    energie = energie1(plan)
    vectEnergie = np.zeros(maxIter)
    
    #paramètres initiaux
    temperatureInitiale = 20
    alphaRefroidissement = 0.9998
    
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
            proba = np.random.random()
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
        vectEnergie[iter] = energie
        iter += 1
        temperature *= alphaRefroidissement
    
    return planMin, vectEnergie

## Recuit simulé avec contraintes


def Recuit2(listeCommandes, listeParametres, tempsAttenteCommandeMoyen, maxIter=100000):
    '''
    Intègre la contrainte de fraîcheur dans le recuit
    '''
    np.random.seed(1)
    
    #initialisation
    plan = planProduction("buffer")
    for com in listeCommandes:
        plan.ajouteCommande(com)
    calculeProduction(plan, listeParametres)
    coutProd, coutAttente = energie2(plan, tempsAttenteCommandeMoyen)
    energie = coutProd + coutAttente
    coutProdBis, coutAttenteBis = coutProd, coutAttente
    listeCoutProd = np.zeros(maxIter)
    listeCoutAttente = np.zeros(maxIter)
    
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
            proba = np.random.random()
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
        listeCoutProd[iter] = coutProd
        listeCoutAttente[iter] = coutAttente
        iter += 1
        temperature *= alphaRefroidissement
        
    return planMin, listeCoutProd, listeCoutAttente


## Recuit simulé partant d'une solution déjà calculée



def Recuit3(planDepart, listeParametres, referenceAttentes, maxIter=100000):
    '''
    Initialisation au plan passé en paramètres
    '''
    
    np.random.seed(1)
    
    #initialisation
    plan = planDepart.copy()
    calculeProduction(plan, listeParametres)
    coutProd, coutAttente = energie3(plan, referenceAttentes)
    energie = coutProd + coutAttente
    
    #stockage de certaines valeurs intermédiaires
    facteurReduction = 10
    listeCoutProd = np.zeros(maxIter//facteurReduction)
    listeCoutAttente = np.zeros(maxIter//facteurReduction)
    
    #paramètres initiaux
    temperatureInitiale = 20
    alphaRefroidissement = 0.9995
    
    #variables intermédiaires
    coutProdBis, coutAttenteBis = coutProd, coutAttente
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
        coutProdBis, coutAttenteBis = energie3(planBis, referenceAttentes)
        energieBis = coutProdBis + coutAttenteBis
        
        if (energieBis <= energie):
            #alors on accepte la transition
            plan = planBis
            energie = energieBis
            coutProd, coutAttente = coutProdBis, coutAttenteBis
        else:
            proba = np.random.random()
            deltaE = energieBis - energie
            seuil = np.exp(-deltaE/temperature)
            
            if (proba <= seuil):
                #accepte quand même la transition
                plan = planBis
                energie = energieBis
                coutProd, coutAttente = coutProdBis, coutAttenteBis

        
        #incrément d'itération
        if iter % facteurReduction == 0:
            listeCoutProd[iter//facteurReduction] = coutProd
            listeCoutAttente[iter//facteurReduction] = coutAttente
        iter += 1
        temperature *= alphaRefroidissement
        
        #sauvegarde du minimum
        if (energie < energieMin):
            planMin = plan.copy()
            energieMin = energie
    
    return planMin, listeCoutProd, listeCoutAttente












