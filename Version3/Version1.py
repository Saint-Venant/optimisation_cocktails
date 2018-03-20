from collections import OrderedDict

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
        
        #matrice de production
        self.matProd = OrderedDict()
        
        #liste de clusters
        self.clusters = []
    
    def updateClusters(self):
        #met à jour la liste des clusters
        self.clusters = [[] for x in range(0, self.nbClusters)]
        for c in self.matProd:
            for j in range(0, len(self.matProd[c])):
                b = c.getBoisson(j)
                self.clusters[self.matProd[c][j]].append(b)
    
    def ajouteCommande(self, com):
        #ajoute une commande donnée à la fin du plan de production,
        #  en scindant la commande en petits clusters de boissons de meme type
        
        triIntraCommandes(com)
        
        ligneMatProd = []
        
        indice = 0
        b1 = com.getBoisson(indice)
        
        ligneMatProd.append(self.nbClusters)
        
        nbNouvClusters = 1
        indice += 1
        
        while (indice < com.nbBoissons):
            b2 = com.getBoisson(indice)
            if (b2.id == b1.id):
                ligneMatProd.append(ligneMatProd[-1])
            else:
                ligneMatProd.append(ligneMatProd[-1] + 1)
                nbNouvClusters += 1
            indice += 1
            b1 = b2
        
        #concaténation de la matrice de production avec sa nouvelle ligne
        if (self.nbClusters == 0):
            self.nbClusters = nbNouvClusters
            self.matProd[com] = ligneMatProd
        elif (self.clusters[-1][-1].id == com.getBoisson(0).id):
            ligneMatProd = [k-1 for k in ligneMatProd]
            self.matProd[com] = ligneMatProd
            self.nbClusters += (nbNouvClusters - 1)
        else:
            self.matProd[com] = ligneMatProd
            self.nbClusters += nbNouvClusters
        
        #mise à jour de la liste des clusters
        self.updateClusters()

    def affichePlan(self):
        self.updateClusters()
        for cl in self.clusters:
            print([b.id for b in cl])
    
    def copy(self):
        '''copie indépendante'''
        copie = planProduction()
        copie.nbClusters = self.nbClusters
        for c in self.matProd:
            copie.matProd[c] = self.matProd[c].copy()
        for i in range(0, len(self.clusters)):
            copie.clusters.append(self.clusters[i].copy())
        return copie
    
    def getCluster(self, indice):
        return self.clusters[indice]
    
    def ajouteCommandeUltraOpti(self, com):
        #ajoute une commande supplémentaire au plan de production
        # groupe les boissons de même type par cluster
        # le numéro de cluster correspond à l'id de la boisson - 1
        
        triIntraCommandes(com)
        
        #parcours les boissons : établit la correspondance entre id et num de cluster
        correspondance = OrderedDict()
        for c in self.matProd:
            for j in range(0, len(self.matProd[c])):
                b = c.getBoisson(j)
                if not(b.id in correspondance):
                    correspondance[b.id] = self.matProd[c][j]
        
        indice = 0
        ligneMatProd = []
        while (indice < com.nbBoissons):
            b = com.listeBoissons[indice]
            if not(b.id in correspondance):
                correspondance[b.id] = self.nbClusters
                self.nbClusters += 1
            ligneMatProd.append(correspondance[b.id])
            indice += 1
        self.matProd[com] = ligneMatProd
        
        #mise à jour de la liste des clusters
        self.updateClusters()
    
    def getNombreBoissons(self):
        #retourne le nombre total de boissons concernées par ce plan de production
        k = 0
        for c in self.matProd:
            k += len(c.listeBoissons)
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


def appliqueProd(cluster, tempsDebut, param):
    #Etant donné un jeu de paramètre et un cluster de boissons à produire (toutes identiques)
    #  applique la fonction de production pour déterminer les instants de fin de préparation
    #  pour chaque boisson de la liste du cluster
    #
    #Retourne le temps courant à la fin de la préparation de ce cluster
    
    idBoisson = cluster[0].id
    assert(idBoisson == param[0])
    nbOpti = param[1]
    coef1 = param[2]
    coef2 = param[3]
    coef3 = param[4]
    n = len(cluster)
    
    temps = tempsDebut
    tempsFin = temps
    nbBoissonsPreparees = 0
    
    if (n <= nbOpti):
        if (n == 1):
            tempsFin = temps + coef1
            cluster[0].debut = temps
            cluster[0].fin = tempsFin
        else:
            for t in range(2, nbOpti+1):
                if (t == n):
                    tempsFin = temps + coef1 + (t-1)*coef2
            for b in cluster:
                b.debut = temps
                b.fin = tempsFin
        nbBoissonsPreparees = n
    else:
        #on prépare les nbOpti premières boissons
        tempsFin = temps + coef1 + (nbOpti-1)*coef2
        for i in range(0, nbOpti):
            cluster[i].debut = temps
            cluster[i].fin = tempsFin
        nbBoissonsPreparees = nbOpti
    
    temps = tempsFin
    
    while (nbBoissonsPreparees < n):
        if (n - nbBoissonsPreparees == 1):
            #il reste une seule boisson à préparer
            tempsFin = temps + coef3
            cluster[n-1].debut = temps
            cluster[n-1].fin = tempsFin
            nbBoissonsPreparees = n
        elif (n - nbBoissonsPreparees <= nbOpti):
            #on peut tout finir de préparer d'un coup
            for t in range(2, nbOpti+1):
                if (n - nbBoissonsPreparees == t):
                    tempsFin = temps + coef3 + (t-1)*coef2
                    for i in range(nbBoissonsPreparees, n):
                        cluster[i].debut = temps
                        cluster[i].fin = tempsFin
            nbBoissonsPreparees = n
        else:
            #on prépare les nbOpti boissons suivantes
            tempsFin = temps + coef3 + (nbOpti-1)*coef2
            for i in range(nbBoissonsPreparees, nbBoissonsPreparees+nbOpti):
                cluster[i].debut = temps
                cluster[i].fin = tempsFin
            nbBoissonsPreparees += nbOpti
        temps = tempsFin
    
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
        tempsCourant = appliqueProd(cl, tempsCourant, param)
        
        indice += 1
    
    #calcule les instants de livraison de chaque commande
    for com in listeCommandes:
        instantLivraison = -1
        for b in com.listeBoissons:
            instantLivraison = max(instantLivraison, b.fin)
        com.livraison = instantLivraison
        for b in com.listeBoissons:
            b.livraison = instantLivraison


'''
Obtenir la liste du nombre de tâches effectuées en parallèle pour chaque instant d'un plan de production
>> doit avoir fait appel à la fonction calculeProduction avant
'''

def nbTachesParallelles(listeCommandes):
    #instant de début de production
    instantDebut = listeCommandes[0].listeBoissons[0].debut
    #instant de fin de production
    instantFin = 0
    for com in listeCommandes:
        instantFin = max(instantFin, com.livraison)
        for b in com.listeBoissons:
            instantDebut = min(instantDebut, b.debut)
    instantDebut = int(instantDebut)
    instantFin = int(instantFin)
    
    listeNbTaches = []
    for t in range(instantDebut, instantFin+1):
        nbTaches = 0
        for com in listeCommandes:
            enPreparation = False
            for b in com.listeBoissons:
                enPreparation = enPreparation or ((b.debut <= t) and (com.livraison > t))
            if enPreparation:
                nbTaches += 1
        listeNbTaches.append(nbTaches)
    
    return listeNbTaches