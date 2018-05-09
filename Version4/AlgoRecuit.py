from StructuresProduction import *
import GlobalParam as gp
import numpy as np



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

'''Définition de l'énergie
>> temps total de production
>> pénalisation du surcroît d'attente par rapport à un temps de référence
>> sur toute la durée de la soirée
'''

def energie4(plan, referenceAttentes):
    # suppose que la mise à jour des variables intermédiaires calculées selon le plan de production souhaité est faite
    
    tempsProduction = 0
    coef = 1.2
    if plan.nbClusters > 0:
        tempsProduction = plan.clusters[-1][-1].fin - plan.instantProd
    coutAttente = 0
    toutesCommandes = set()
    for cl in plan.clusters:
        for b in cl:
            com = b.commande
            toutesCommandes.update([com])
    for com in toutesCommandes:
        attente = com.livraison - com.instantCommande
        borne = 1.2*referenceAttentes[com.num]
        if (attente > borne):
            coutAttente += gp.penalisationAttente * (attente - borne)**2
    return tempsProduction + coutAttente



## Voisinage

'''Voisinage :
    * changer l'affectation d'un matProd[b]
    * peut conduire à ajouter ou supprimer un cluster
    * ne peut que créer un cluster en fin de production
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


'''Voisinage :
    * changer l'affectation d'un matProd[b]
    * peut conduire à ajouter ou supprimer un cluster
    * peut créer/insérer des clusters n'import où dans la production
'''

def tireVoisin_complet(plan):
    #fait une copie de l'ancien plan de production
    nouveauPlan = plan.copy()
    
    #tire au sort une boisson
    j0 = np.random.randint(len(nouveauPlan.matProd))
    b = list(nouveauPlan.matProd.keys())[j0]
    
    #tire au sort une nouvelle affectation de clusters
    ancienCluster = nouveauPlan.matProd[b]
    nouvCluster = np.random.randint(nouveauPlan.nbClusters+1)
    
    if (nouvCluster == ancienCluster):
        pass
    elif (ancienCluster < nouvCluster-1):
        # decalage1 : ancien cluster vide, et fusion des deux clusters voisins si ils sont de même type
        decalage1 = 0
        if (len(nouveauPlan.clusters[ancienCluster]) == 1) and (ancienCluster == 0):
            decalage1 = 1
        elif (len(nouveauPlan.clusters[ancienCluster]) == 1):
            clAvant = nouveauPlan.clusters[ancienCluster-1]
            clApres = nouveauPlan.clusters[ancienCluster+1]
            if (clAvant[0].id == clApres[0].id):
                decalage1 = 2
            else:
                decalage1 = 1
        
        # decalage 2 : fusion possible entre le nouveau cluster et son voisin de gauche
        # decalage 3 : fusion possible entre le nouveau cluster et son voisin de droite
        decalage2 = 0
        decalage3 = 0
        if (nouvCluster < nouveauPlan.nbClusters):
            clAvant = nouveauPlan.clusters[nouvCluster-1]
            clApres = nouveauPlan.clusters[nouvCluster]
            if (b.id == clAvant[0].id):
                decalage2 = 1
            elif (b.id == clApres[0].id):
                decalage3 = 1
        elif (nouvCluster == nouveauPlan.nbClusters):
            clAvant = nouveauPlan.clusters[-1]
            if (b.id == clAvant[0].id):
                decalage2 = 1
        
        # actualisation de matProd
        for bois in nouveauPlan.matProd:
            if nouveauPlan.matProd[bois] < ancienCluster:
                pass
            elif (nouveauPlan.matProd[bois] > ancienCluster) and (nouveauPlan.matProd[bois] < nouvCluster):
                nouveauPlan.matProd[bois] -= decalage1
            elif (nouveauPlan.matProd[bois] >= nouvCluster):
                nouveauPlan.matProd[bois] += 1 - decalage1 - decalage2 - decalage3
        
        # actualisation du nombre de clusters
        nouveauPlan.nbClusters += 1 - decalage1 - decalage2 - decalage3
        
        # cluster de b
        nouveauPlan.matProd[b] = nouvCluster - decalage1 - decalage2
    elif (ancienCluster == nouvCluster - 1):
        pass
    elif (nouvCluster < ancienCluster -1):
        # decalage 1
        decalage1 = 0
        if (ancienCluster == nouveauPlan.nbClusters - 1) and (len(nouveauPlan.clusters[ancienCluster]) == 1):
            decalage1 = 1
        elif (len(nouveauPlan.clusters[ancienCluster]) == 1):
            clAvant = nouveauPlan.clusters[ancienCluster-1]
            clApres = nouveauPlan.clusters[ancienCluster+1]
            if (clAvant[0].id == clApres[0].id):
                decalage1 = 2
            else:
                decalage1 = 1
        
        # decalages 2 et 3
        decalage2 = 0
        decalage3 = 0
        if (nouvCluster == 0):
            clApres = nouveauPlan.clusters[0]
            if (b.id == clApres[0].id):
                decalage3 = 1
        else:
            clAvant = nouveauPlan.clusters[nouvCluster-1]
            clApres = nouveauPlan.clusters[nouvCluster]
            if (b.id == clAvant[0].id):
                decalage2 = 1
            elif (b.id == clApres[0].id):
                decalage3 = 1
        
        # actualisation de matProd
        for bois in nouveauPlan.matProd:
            if nouveauPlan.matProd[bois] < nouvCluster:
                pass
            elif (nouveauPlan.matProd[bois] >= nouvCluster) and (nouveauPlan.matProd[bois] < ancienCluster):
                nouveauPlan.matProd[bois] += 1 - decalage2 - decalage3
            else:
                nouveauPlan.matProd[bois] += 1 - decalage2 - decalage3 - decalage1
        
        # actualisation du nombre du clusters
        nouveauPlan.nbClusters += 1 - decalage1 - decalage2 - decalage3
        
        # cluster de b
        nouveauPlan.matProd[b] = nouvCluster - decalage2
    elif (nouvCluster == ancienCluster - 1):
        pass
    
    nouveauPlan.updateClusters()
    return nouveauPlan



## Recuit simulé sans contrainte

def Recuit1(listeCommandes, listeParametres, maxIter=100000, voisinage=tireVoisin_complet, T0=20, alphaRefroidissement=0.99996):
    '''
    maxIter : nombre d'itérations du recuit
    voisinage : fonction de voisinage
    T0 : température initiale
    alphaRefroidissement : coefficient de refroidissement de la temprérature
    '''
    
    #initialisation
    plan = planProduction("buffer")
    for com in listeCommandes:
        plan.ajouteCommande(com)
    calculeProduction(plan, listeParametres)
    energie = energie1(plan)
    vectEnergie = np.zeros(maxIter)
    
    #variables intermédiaires
    energieBis = energie
    planBis = plan.copy()
    iter = 0
    temperature = T0
    
    #maintien en mémoire du plan qui donne l'énergie minimum
    planMin = plan.copy()
    energieMin = energie
    
    while (iter < maxIter):
        
        #monitoring de la progression
        if (iter%5000 == 0):
            print("itération ", iter, "(", iter/maxIter*100, "%),  energie1 =", energie)
        
        #explore un plan de production voisin
        planBis = voisinage(plan)
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


def Recuit2(listeCommandes, listeParametres, tempsAttenteCommandeMoyen, maxIter=100000, voisinage=tireVoisin_complet, T0=20, alphaRefroidissement=0.99996):
    '''
    Intègre la contrainte de fraîcheur dans le recuit
    maxIter : nombre d'itérations du recuit
    voisinage : fonction de voisinage
    T0 : température initiale
    alphaRefroidissement : coefficient de refroidissement de la temprérature
    '''
    
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
    
    #variables intermédiaires
    energieBis = energie
    planBis = plan.copy()
    iter = 0
    temperature = T0
    
    #maintien en mémoire du plan qui donne l'énergie minimum
    planMin = plan.copy()
    energieMin = energie
    
    while (iter < maxIter):
        
        #monitoring de la progression
        if (iter%5000 == 0):
            print("itération ", iter, "(", iter/maxIter*100, "%),  energie2 =", energie)
            #print("energieMin = ", energieMin)
        
        #explore un plan de production voisin
        planBis = voisinage(plan)
        calculeProduction(planBis, listeParametres)
        
        respectContraintes = verifieContraintes(planBis)
        while not(respectContraintes):
            planBis = voisinage(plan)
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



def Recuit3(planDepart, listeParametres, referenceAttentes, maxIter=100000, voisinage=tireVoisin_complet, T0=20, alphaRefroidissement=0.9995):
    '''
    Initialisation au plan passé en paramètres
    referenceAttentes : liste d'attentes de référence, jugées encore tolérables
    maxIter : nombre d'itérations du recuit
    voisinage : fonction de voisinage
    T0 : température initiale
    alphaRefroidissement : coefficient de refroidissement de la temprérature
    '''
    
    #initialisation
    plan = planDepart.copy()
    calculeProduction(plan, listeParametres)
    coutProd, coutAttente = energie3(plan, referenceAttentes)
    energie = coutProd + coutAttente
    
    #stockage de certaines valeurs intermédiaires
    facteurReduction = 10
    listeCoutProd = np.zeros(maxIter//facteurReduction)
    listeCoutAttente = np.zeros(maxIter//facteurReduction)
    
    #variables intermédiaires
    coutProdBis, coutAttenteBis = coutProd, coutAttente
    energieBis = energie
    planBis = plan.copy()
    iter = 0
    temperature = T0
    
    #maintien en mémoire du plan qui donne l'énergie minimum
    planMin = plan.copy()
    energieMin = energie
    
    while (iter < maxIter):
        
        #monitoring de la progression
        if (iter%5000 == 0):
            #print("itération ", iter, "(", iter/maxIter*100, "%),  energie2 =", energie)
            pass
        
        #explore un plan de production voisin
        planBis = voisinage(plan)
        calculeProduction(planBis, listeParametres)
        
        respectContraintes = verifieContraintes(planBis)
        while not(respectContraintes):
            planBis = voisinage(plan)
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












