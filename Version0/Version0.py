import numpy as np

##--------------Paramètres globaux du problème----------------------

#Nombre max de boissons par commande
A_max = 10

#Nombre de type de boissons différentes
N_boissons = 10

##

class boisson:
    def __init__(self, id, Commande, num):
        #identifiant du type de boisson
        self.id = id
        
        #commande à laquelle la boisson appartient
        self.commande = Commande
        
        #numero de boisson dans la commande (j)
        self.num = num
        
        #instant de commande
        self.instantCommande = Commande.instantCommande
        
        #instant de début de préparation : vaut -1 à l'initialisation
        self.debut = -1
        
        #instant de fin de préparation : vaut -1 à l'initialisation
        self.fin = -1
        
        #instant de livraison : vaut -1 à l'initialisation
        self.livraison = -1
    
    def affecteCommande(self, Commande, num):
        #change l'affectation de la boisson à une commande donnée
        self.commande = Commande
        self.num = num
        self.instantCommande





class commande:
    def __init__(self, numCommande, instantCom):
        #numero de la commande (i)
        self.num = numCommande
        
        #instant où la commande est passée
        self.instantCommande = instantCom
        
        #instant où la commande est livrée : vaut -1 à l'initialisation
        self.livraison = -1
        
        #liste des boissons associées à cette commande
        #--initialisé à que des zéros
        self.listeBoissons = []
        
        #nombre de boissons contenues par la commande
        self.nbBoissons = 0
    
    def ajouteBoisson(self, b):
        #vérifie que la commande n'est pas déjà pleine
        if (self.nbBoissons < A_max):
            self.listeBoissons.append(b)
            b.affecteCommande(self, self.nbBoissons)
            self.nbBoissons += 1
    
    def afficheBoissons(self):
        aff = []
        for b in self.listeBoissons:
            aff.append(b.id)
        print(aff)
    
    def idBoisson(self, indice):
        #retourne le type de boisson numero 'indice' dans listeBoisson
        if (indice < 0) or (indice >= self.nbBoissons):
            return -1
        else:
            return self.listeBoissons[indice].id
    
    def getBoisson(self, indice):
        #retourne la boisson d'index 'indice' dans listeBoissons
        return self.listeBoissons[indice]


class planProduction:
    def __init__(self):
        #nombre de sous-unités de production
        self.nbClusters = 0
        
        #liste des clusters de boissons à produire
        self.clusters = []
    
    def ajouteCommande(self, com):
        #ajoute une commande donnée à la fin du plan de production,
        #  en scindant la commande en petits clusters de boissons de meme type
        
        triIntraCommandes(com)
        
        listeClusters = []
        indice = 0
        cluster = []
        cluster.append(com.getBoisson(indice))
        indice += 1
        while (indice < com.nbBoissons):
            if (com.idBoisson(indice) == cluster[-1].id):
                cluster.append(com.getBoisson(indice))
            else:
                listeClusters.append(cluster)
                cluster = []
                cluster.append(com.getBoisson(indice))
            indice += 1
        listeClusters.append(cluster)
        
        #concaténation des listes de clusters
        if (self.clusters == []):
            self.clusters = listeClusters
            self.nbClusters = len(listeClusters)
        elif (self.clusters[-1][0].id == listeClusters[0][0]):
            self.clusters[-1] += listeClusters[0]
            self.clusters += listeClusters[1:]
            self.nbClusters = len(self.clusters)
        else:
            self.clusters += listeClusters
            self.nbClusters = len(self.clusters)
    
    def affichePlan(self):
        for cl in self.clusters:
            print(len(cl)*[cl[0].id])
    
    def getCluster(self, indice):
        return self.clusters[indice]
    
    def copy(self):
        '''copie indépendante'''
        copie = planProduction()
        copie.nbClusters = self.nbClusters
        copie.clusters = []
        for cl in self.clusters:
            copie.clusters.append(cl.copy())
        return copie
    
    def ajouteCommandeUltraOpti(self, com):
        #ajoute une commande supplémentaire au plan de production
        # groupe les boissons de même type par cluster
        
        triIntraCommandes(com)
        
        indice = 0
        while (indice < com.nbBoissons):
            b = com.listeBoissons[indice]
            k = 0
            while (k < len(self.clusters)):
                cl = self.clusters[k]
                if (cl[-1].id == b.id):
                    cl.append(b)
                    k = len(self.clusters) + 1
                else:
                    k += 1
            if (k == len(self.clusters)):
                self.clusters.append([b])
                self.nbClusters = len(self.clusters)
            indice += 1
    
    def getNombreBoissons(self):
        #retourne le nombre total de boissons concernées par ce plan de production
        k = 0
        for cl in self.clusters:
            k += len(cl)
        return k



def triIntraCommandes(Commande):
    #regroupe les boissons par type au sein de la commande
    #--revient à les classer par ordre croissant selon leur id
    
    l = Commande.listeBoissons
    Commande.listeBoissons = []
    Commande.nbBoissons = 0
    
    for i in range(1, N_boissons+1):
        #ajoute les boissons avec id=i
        for b in l:
            if b.id == i:
                Commande.ajouteBoisson(b)


#fonction de production
def prod(n, param):
    #n : nombre de boissons à préparer
    #retourne le temps qu'il faut pour préparer cette quantité
    nbOpti = param[1]
    coef1 = param[2]
    coef2 = param[3]
    coef3 = param[4]
    temps = 0
    
    if (n <= 0):
        temps = 0
        return temps
    
    if (n == 1):
        temps = coef1
        return temps
    
    for t in range(2, nbOpti+1):
        if (n == t):
            temps = coef1 + (t-1)*coef2
            return temps
    
    temps = coef1 + (nbOpti-1)*coef2
    
    n -= nbOpti
    while (n > 0):
        if (n == 1):
            temps += coef3
            return temps
        
        for t in range(2, nbOpti+1):
            if (n == t):
                temps += coef3 + (t-1)*coef2
                return temps
        
        temps += coef3 + (nbOpti-1)*coef2
        n -= nbOpti
    
    return temps


def appliqueProd(cluster, tempsDebut, listeParametres):
    #Etant donné un jeu de paramètre et un cluster de boissons à produire (toutes identiques)
    #  applique la fonction de production pour déterminer les instants de fin de préparation
    #  pour chaque boisson de la liste du cluster
    #
    #Retourne le temps courant à la fin de la préparation de ce cluster
    
    idBoisson = cluster[0].id
    param = listeParametres[idBoisson-1]
    assert(idBoisson == param[0])
    nbOpti = param[1]
    coef1 = param[2]
    coef2 = param[3]
    coef3 = param[4]
    n = len(cluster)
    
    temps = tempsDebut
    nbBoissonsPreparees = 0
    
    while (nbBoissonsPreparees < n):
        if (n - nbBoissonsPreparees < nbOpti):
            #on peut finir de tout préparer d'un coup
            tempsFin = temps + prod(n-nbBoissonsPreparees, param)
            for i in range(nbBoissonsPreparees, n):
                cluster[i].debut = temps
                cluster[i].fin = tempsFin
            temps = tempsFin
            nbBoissonsPreparees = n
        else:
            #on prepare les nbOpti boissons suivantes
            tempsFin = temps + prod(nbOpti, param)
            for i in range(nbBoissonsPreparees, nbBoissonsPreparees+nbOpti):
                cluster[i].debut = temps
                cluster[i].fin = tempsFin
            temps = tempsFin
            nbBoissonsPreparees += nbOpti
    
    return temps
    


'''fonction permettant de calculer les variables intermédiaires d'après un plan de production donné
'''
def calculeProduction(plan, listeCommandes, listeParametres):
    #instant de début de production global = instant de la dernière commande passée
    tempsCourant = listeCommandes[-1].instantCommande
    
    #instant de fin de preparation
    tempsFin = 0
    
    #indice du cluster en cours de traitement
    indice = 0
    
    while (indice < plan.nbClusters):
        #cluster en traitement
        cl = plan.getCluster(indice)
        
        #identifiant du type de boisson à produire dans ce cluster
        idBoisson = cl[0].id
        
        #paramètres de production spécifiques au type de boisson
        param = listeParametres[idBoisson-1]
        
        #met à jour les variables de traitement de chaque boisson du cluster
        tempsCourant = appliqueProd(cl, tempsCourant, listeParametres)
        
        indice += 1
    
    #calcule les instants de livraison de chaque commande
    for com in listeCommandes:
        instantLivraison = -1
        for b in com.listeBoissons:
            instantLivraison = max(instantLivraison, b.fin)
        com.livraison = instantLivraison
        for b in com.listeBoissons:
            b.livraison = instantLivraison