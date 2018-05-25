from collections import OrderedDict
import GlobalParam as gp

## Classes principales

class boisson:
    def __init__(self, id):
        #identifiant du type de boisson
        self.id = id
        
        #commande à laquelle la boisson appartient : vaut -1 à l'initialisation
        self.commande = -1
        
        #numero de boisson dans la commande (j) : vaut -1 à l'initialisation
        self.num = -1
        
        #instant de commande : vaut -1 à l'initialisation
        self.instantCommande = -1
        
        #instant de début de préparation : vaut -1 à l'initialisation
        self.debut = -1
        
        #instant de fin de préparation : vaut -1 à l'initialisation
        self.fin = -1
        
        #instant de livraison : vaut -1 à l'initialisation
        self.livraison = -1
    
    def affecteCommande(self, Commande):
        #affecte une boisson à une commande donnée
        self.commande = Commande
        self.num = Commande.nbBoissons
        self.instantCommande = Commande.instantCommande
    
    def reinitialise(self):
        '''
        Réinitialise un certain nombre de paramètres calculés (avec un plan de production)
        '''
        self.debut = -1
        self.fin = -1
        self.livraison = -1
    
    def copy(self):
        '''
        Faire une copie indépendante (d'un point de vue mémoire)
        '''
        copie = boisson(self.id)
        copie.commande = self.commande
        copie.num = self.num
        copie.instantCommande = self.instantCommande
        return copie





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
        if (self.nbBoissons < gp.A_max):
            self.listeBoissons.append(b)
            b.affecteCommande(self)
            self.nbBoissons += 1
        else:
            print("problème : commande déjà pleine")
    
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
    
    def reinitialise(self):
        '''
        Réinitialise les paramètres calculés avec un plan de production
        '''
        self.livraison = -1
    
    def copy(self):
        '''
        Fait une copie indépendante (d'un point de vue mémoire)
        '''
        copie = commande(self.num, self.instantCommande)
        copie.nbBoissons = self.nbBoissons
        for b in self.listeBoissons:
            b_copie = b.copy()
            b_copie.commande = copie
            copie.listeBoissons.append(b_copie)
        return copie


class planProduction:
    def __init__(self, type_prod):
        '''
        type_prod = "buffer", "soiree"
            * "buffer" : commence à produire lorsque la dernière commande est passée
            * "soiree" : commence à produire dès qu'une commandeest passée
        '''
        
        #nombre de sous-unités de production
        self.nbClusters = 0
        
        #matrice de production : indicée par la commande
        self.matProd = OrderedDict()
        
        #liste de clusters
        self.clusters = []
        
        #instant où le plan est mis en production
        self.instantProd = -1
        self.type_prod = type_prod
        
        #premier instant où le plan peut être mis en production
        self.instantDebutTotal = -1
        
        #ensemble des commandes préparées dans ce plan de production
        self.commandes = set()
        
        #stocke l'historique des clusters déjà produits
        self.histoire = []
    
    def updateClusters(self):
        #met à jour la liste des clusters
        self.clusters = [[] for x in range(self.nbClusters)]
        for b in self.matProd:
            self.clusters[self.matProd[b]].append(b)
    
    def ajouteCommande(self, com):
        #ajoute une commande donnée à la fin du plan de production,
        #  en scindant la commande en petits clusters de boissons de meme type
        
        # trie les boissons de la commande par type
        triIntraCommandes(com)
        
        #ajoute cette commande à l'ensemble des commandes préparées dans ce plan
        self.commandes.update([com])
        
        #ajuste l'instant de début de production
        if self.type_prod == "buffer":
            self.instantProd = max(self.instantProd, com.instantCommande)
            self.instantDebutTotal = self.instantProd
        elif self.type_prod == "soiree":
            if (self.nbClusters == 0) and len(self.histoire) == 0:
                self.instantProd = com.instantCommande
                self.instantDebutTotal = self.instantProd
            elif (self.nbClusters == 0):
                self.instantProd = com.instantCommande
        
        #ajoute chacune des boissons de la commande à un cluster
        for b in com.listeBoissons:
            #regarde si b est du même type que le dernier cluster
            if self.nbClusters == 0:
                self.clusters.append([b])
                self.matProd[b] = 0
                self.nbClusters += 1
            elif (b.id == self.clusters[-1][0].id):
                #alors ajoute cette boisson au dernier cluster
                self.clusters[-1].append(b)
                self.matProd[b] = self.nbClusters - 1
            else:
                #crée un nouveau cluster
                self.clusters.append([b])
                self.matProd[b] = self.nbClusters
                self.nbClusters += 1

    def affichePlan(self):
        self.updateClusters()
        for cl in self.clusters:
            print([b.id for b in cl])
    
    def copy(self):
        '''
        Objectif = faire une copie indépendante de ce plan de production
        '''
        copie = planProduction(self.type_prod)
        
        copie.nbClusters = self.nbClusters
        for b in self.matProd:
            copie.matProd[b] = self.matProd[b]
        for cl in self.clusters:
            copie.clusters.append(cl.copy())
        copie.instantProd = self.instantProd
        copie.instantDebutTotal = self.instantDebutTotal
        for com in self.commandes:
            copie.commandes.update([com])
        for cl in self.histoire:
            copie.histoire.append(cl.copy())
        
        return copie
    
    def getCluster(self, indice):
        return self.clusters[indice]
    
    def ajouteCommandeUltraOpti(self, com):
        #ajoute une commande supplémentaire au plan de production
        # groupe les boissons de même type par cluster
        # le numéro de cluster correspond à l'id de la boisson - 1
        
        # trie les boissons de la commande par type
        triIntraCommandes(com)
        
        #ajoute cette commande à l'ensemble des commandes préparées dans ce plan
        self.commandes.update([com])
        
        #ajuste l'instant de début de production
        if self.type_prod == "buffer":
            self.instantProd = max(self.instantProd, com.instantCommande)
            self.instantDebutTotal = self.instantProd
        elif self.type_prod == "soiree":
            if (self.nbClusters == 0) and len(self.histoire) == 0:
                self.instantProd = com.instantCommande
                self.instantDebutTotal = self.instantProd
            elif (self.nbClusters == 0):
                self.instantProd = com.instantCommande
        
        #parcours les boissons : établit la correspondance entre id et num de cluster
        correspondance = OrderedDict()
        for b in self.matProd:
            if not(b.id in correspondance):
                correspondance[b.id] = self.matProd[b]
        
        #ajoute les nouvelles boissons en s'aidant de cet index de correspondance
        for b in com.listeBoissons:
            if not(b.id in correspondance):
                #complète l'index de correspondance en y insérant l'id de la nouvelle boisson
                correspondance[b.id] = self.nbClusters
                self.nbClusters += 1
                self.clusters.append([])
            self.matProd[b] = correspondance[b.id]
            self.clusters[correspondance[b.id]].append(b)
    
    def get_finProdTotal(self):
        '''
        Retourne l'instant où toutes les boissons du plan de production ont pu être produites, histoire comprise
        Suppose que la fonction calculeProd a été appelée précédemment
        '''
        fin = -1
        if self.nbClusters > 0:
            fin = self.clusters[-1][-1].fin
        elif len(self.histoire) > 0:
            fin = self.histoire[-1][-1].fin
        else:
            fin = self.instantProd
        return fin
    
    def update_livraison(self, tempsCourant):
        '''
        Met à jour un plan de production à partir d'un tempsCourant. Supprime du plan de production toutes les boissons des clusters qui ont déjà été préparés à cette date.
        Actualise en conséquence l'instant de début de début de production au dernier instants de fin de production des clusters supprimés
        
        stocke les clusters qui ont déjà été produits (pour une sauvegarde du plan de production sur une soirée)
        '''
        cond = True
        while cond and (self.nbClusters > 0):
            #regarde si le premier cluster sur la liste de production a effectivement été produits
            cl = self.clusters[0]
            fin0 = cl[-1].fin
            if fin0 <= tempsCourant:
                self.histoire.append(cl)
                # retire ce cluster du plan de production
                for b in cl:
                    del self.matProd[b]
                for b in self.matProd:
                    self.matProd[b] -= 1
                self.nbClusters -= 1
                del self.clusters[0]
                # met à jour l'instant de début de production
                self.instantProd = fin0
                cond = True
            else:
                cond = False
        
        #met à jour la liste des commandes préparées dans ce cluster
        self.commandes = set()
        for b in self.matProd:
            com = b.commande
            self.commandes.update([com])



def triIntraCommandes(Commande):
    #regroupe les boissons par type au sein de la commande
    #--revient à les classer par ordre croissant selon leur id
    
    l = Commande.listeBoissons
    Commande.listeBoissons = []
    Commande.nbBoissons = 0
    
    for i in range(1, gp.N_boissons+1):
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
        for i in range(nbOpti):
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
def calculeProduction(plan, listeParametres):
    #instant de début de production
    tempsCourant = plan.instantProd
    
    #calcule les instants de début et de fin de production de chaque cluster
    for cl in plan.clusters:
        #identifiant du type de boisson à produire dans ce cluster
        idBoisson = cl[0].id
        
        #paramètres de production spécifiques au type de boisson
        param = listeParametres[idBoisson-1]
        
        #met à jour les variables de traitement de chaque boisson du cluster
        tempsCourant = appliqueProd(cl, tempsCourant, param)
    
    #calcule les instants de livraison de chaque commande/boisson
    for com in plan.commandes:
        instantLivraison = -1
        for b in com.listeBoissons:
            instantLivraison = max(instantLivraison, b.fin)
        # on ne livre pas une commande avant que celle-ci n'ait été passée
        instantLivraison = max(instantLivraison, com.instantCommande)
        com.livraison = instantLivraison
        for b in com.listeBoissons:
            b.livraison = instantLivraison


'''
Obtenir la liste du nombre de tâches effectuées en parallèle pour chaque instant d'un plan de production
>> doit avoir fait appel à la fonction calculeProduction avant
'''

def nbTachesParalleles(plan):
    #instant de début de production
    instantDebut = int(plan.instantDebutTotal)
    #instant de fin de production
    instantFin = int(plan.get_finProdTotal())
    
    
    listeNbTaches = []
    
    #ensemble de commandes traitées ou à traiter
    toutesCommandes = set()
    for cl in plan.histoire:
        for b in cl:
            com = b.commande
            toutesCommandes.update([com])
    toutesCommandes.update(plan.commandes)
    
    for t in range(instantDebut, instantFin+1):
        nbTaches = 0
        for com in toutesCommandes:
            enPreparation = False
            for b in com.listeBoissons:
                enPreparation = enPreparation or ((b.debut <= t) and (com.livraison > t))
            if enPreparation:
                nbTaches += 1
        listeNbTaches.append(nbTaches)
    
    return listeNbTaches