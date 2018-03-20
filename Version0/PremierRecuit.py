from Version0 import *
import random


'''PremierRecuit :
    * contraintes rigides
    * énergie simple
    * peu d'itérations
'''

## Définition des contraintes

#temps max d'attente d'une boisson préparée avant sa livraison (afin de garantir sa fraicheur)
tempsFraicheur = 500

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



## Voisinage

'''
Voisinage A :
    * bouger une boisson d'un cluster à l'autre
    * possibilité de faire disparaître des clusters
'''

def tireVoisinA(plan):
    #fait une copie de l'ancien plan de production
    nouveauPlan = plan.copy()
    
    #tire un cluster
    indiceCl = random.randint(0, len(nouveauPlan.clusters)-1)
    cl = nouveauPlan.clusters[indiceCl]
    
    #tire une boisson dans ce cluster
    b = cl[random.randint(0, len(cl)-1)]
    
    #tire au sort un nouveau cluster dans lequel rajouter b
    #  > ce nouveau cluster doit contenir des boissons de même type
    indiceNouveauCl = random.randint(0, len(nouveauPlan.clusters)-1)
    while (nouveauPlan.clusters[indiceNouveauCl][0].id != b.id):
        indiceNouveauCl = random.randint(0, len(nouveauPlan.clusters)-1)
    
    if (indiceNouveauCl != indiceCl):
        #retire b de cl
        cl.remove(b)
        
        #insère b dans son nouveau cluster
        nouveauCl = nouveauPlan.clusters[indiceNouveauCl]
        indice = random.randint(0, len(nouveauCl))
        if (indice == len(nouveauCl)):
            nouveauCl += [b]
            nouveauPlan.clusters[indiceNouveauCl] = nouveauCl
        else:
            nouveauCl = nouveauCl[:indice] + [b] + nouveauCl[indice:]
            nouveauPlan.clusters[indiceNouveauCl] = nouveauCl
        
        #supprime le cluster cl s'il est devenu vide
        if (cl == []):
            nouveauPlan.clusters.remove(cl)
            nouveauPlan.nbClusters -= 1
    
    return nouveauPlan


'''
Voisinage B :
    * permuter deux clusters
'''

def tireVoisinB(plan):
    #fait une copie de l'ancien plan de production
    nouveauPlan = plan.copy()
    
    #tire au sort les indices de deux clusters
    indice1 = random.randint(0, nouveauPlan.nbClusters-1)
    indice2 = random.randint(0, nouveauPlan.nbClusters-1)
    
    #permute les deux clusters
    nouveauPlan.clusters[indice1], nouveauPlan.clusters[indice2] = nouveauPlan.clusters[indice2], nouveauPlan.clusters[indice1]
    
    return nouveauPlan


'''
Voisinage C :
    * fusionner 2 clusters
'''

def tireVoisinC(plan):
    #fait une copie de l'ancien plan de production
    nouveauPlan = plan.copy()
    
    #tire au sort les indices de deux clusters
    indice1 = random.randint(0, nouveauPlan.nbClusters-1)
    indice2 = random.randint(0, nouveauPlan.nbClusters-1)
    
    #limite le nombre de tentatives de recherche de 2 clusters de meme type
    compt = 0
    maxCompt = 10
    
    while (compt < maxCompt) and (nouveauPlan.clusters[indice1][0].id != nouveauPlan.clusters[indice2][0].id) and (indice1 == indice2):
        indice1 = random.randint(0, nouveauPlan.nbClusters-1)
        indice2 = random.randint(0, nouveauPlan.nbClusters-1)
        compt += 1
    
    #fusionne les deux clusters si les types correspondent
    if (nouveauPlan.clusters[indice1][0].id == nouveauPlan.clusters[indice2][0].id) and (indice1 != indice2):
        #fusionne dans l'un ou dans l'autre avec proba 0.5
        fusion = random.randint(1,2)
        
        if (fusion == 1):
            #garde le cluster d'indice1
            nouveauPlan.clusters[indice1] += nouveauPlan.clusters[indice2]
            del nouveauPlan.clusters[indice2]
        else:
            #garde le cluster d'indice2
            nouveauPlan.clusters[indice2] += nouveauPlan.clusters[indice1]
            del nouveauPlan.clusters[indice1]

        nouveauPlan.nbClusters -= 1
    
    return nouveauPlan


'''
Voisinage D :
    * scinder un cluster
'''

def tireVoisinD(plan):
    #fait une copie de l'ancien plan de production
    nouveauPlan = plan.copy()
    
    #tire au sort un cluster
    indiceCl = random.randint(0, len(nouveauPlan.clusters)-1)
    
    cl = nouveauPlan.clusters[indiceCl]
    while (len(cl) == 1):
        indiceCl = random.randint(0, len(nouveauPlan.clusters)-1)
        cl = nouveauPlan.clusters[indiceCl]
    
    #prend une boisson du cluster pour en faire un nouveau cluster
    indiceBoisson = random.randint(0, len(cl)-1)
    b = cl[indiceBoisson]
    del cl[indiceBoisson]
    
    indiceNouveauCl = random.randint(0, len(nouveauPlan.clusters))
    if (indiceNouveauCl == len(nouveauPlan.clusters)):
        nouveauPlan.clusters.append([b])
    else:
        nouveauPlan.clusters = nouveauPlan.clusters[:indiceNouveauCl] + [b] + nouveauPlan.clusters[indiceNouveauCl:]
    nouveauPlan.nbClusters = len(nouveauPlan.clusters)
    
    return nouveauPlan


## Simple descente locale

def descenteLocale1(listeCommandes, listeParametres, maxIter=100000):
    '''selon le voisinage A'''
    
    #maxIter = nombre max d'itérations
    
    #initialisation
    plan = planProduction()
    for com in listeCommandes:
        plan.ajouteCommande(com)
    calculeProduction(plan, listeCommandes, listeParametres)
    energie = energie1(listeCommandes)
    energieBis = energie
    
    iter = 0
    
    #suivi de progression
    listeEnergie = [energie]
    print()
    print("descenteLocale1")
    
    while (iter < maxIter):
        #monitoring des itérations
        if (iter%5000 == 0):
            print("progression :", iter/maxIter*100, "%  ; energie = ", energie)
        
        planBis = tireVoisinA(plan)
        calculeProduction(planBis, listeCommandes, listeParametres)
        energieBis = energie1(listeCommandes)
        
        if (energieBis <= energie) and verifieContraintes(listeCommandes):
            energie = energieBis
            plan = planBis
        
        iter += 1
        listeEnergie.append(energie)
    
    return plan, listeEnergie



def descenteLocale2(listeCommandes, listeParametres, maxIter=100000):
    '''selon les voisinages A et B'''
    
    #maxIter = nombre max d'itérations
    
    #initialisation
    plan = planProduction()
    for com in listeCommandes:
        plan.ajouteCommande(com)
    calculeProduction(plan, listeCommandes, listeParametres)
    energie = energie1(listeCommandes)
    energieBis = energie
    
    iter = 0
    
    #suivi de progression
    listeEnergie = [energie]
    print()
    print("descenteLocale2")
    
    while (iter < maxIter):
        #monitoring des itérations
        if (iter%5000 == 0):
            print("progression :", iter/maxIter*100, "%  ; energie = ", energie)
        
        #tire au sort un voisinage
        voisinage = random.random()
        if (voisinage < 0.05):
            planBis = tireVoisinB(plan)
        else:
            planBis = tireVoisinA(plan)
        calculeProduction(planBis, listeCommandes, listeParametres)
        energieBis = energie1(listeCommandes)
        
        if (energieBis <= energie) and verifieContraintes(listeCommandes):
            energie = energieBis
            plan = planBis
        
        iter += 1
        listeEnergie.append(energie)
    
    return plan, listeEnergie



def descenteLocale3(listeCommandes, listeParametres, maxIter=100000):
    '''selon le voisinage C'''
    
    #maxIter = nombre max d'itérations
    
    #initialisation
    plan = planProduction()
    for com in listeCommandes:
        plan.ajouteCommande(com)
    calculeProduction(plan, listeCommandes, listeParametres)
    energie = energie1(listeCommandes)
    energieBis = energie
    
    iter = 0
    
    #suivi de progression
    listeEnergie = [energie]
    print()
    print("descenteLocale3")
    
    while (iter < maxIter):
        #monitoring des itérations
        if (iter%500 == 0):
            print("progression :", iter/maxIter*100, "%  ; energie = ", energie)
        planBis = tireVoisinC(plan)
        calculeProduction(planBis, listeCommandes, listeParametres)
        energieBis = energie1(listeCommandes)
        
        if (energieBis <= energie) and verifieContraintes(listeCommandes):
            energie = energieBis
            plan = planBis
        
        iter += 1
        listeEnergie.append(energie)
    
    return plan, listeEnergie