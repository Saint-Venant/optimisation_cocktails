# Données

import GlobalParam as gp
import GenerationDonnees as gend
import numpy as np

## Définition classes

class Boisson:
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

class Commande:
    def __init__(self,id,instant_commande, boissons_commandees):
        #identifiant de la commande
        self.id=id
        
        # instant de commande
        self.t=instant_commande
        
        # Nombre de boissons commandées pour chaque type de boisson existant
        self.c=boissons_commandees
        
        # instant de livraison : vaut -1 à l'initialisation
        self.l=-1
        
        
    def instant_livraison(self,clusters):
        self.l=max( clusters[id_clust].t_fin_prep() for id_clust in id_clusters_concernes(clusters,self.id) )
        return self.l
        
    def attente(self,clusters):
        return self.instant_livraison(clusters)-self.t

class Cluster:
    def __init__(self,id,t_debut_prep,id_boisson,nb_boisson,commandes_concernees):
        # indice du cluster
        self.id=id
        
        # indice de la boisson préparée dans le cluster
        self.id_boisson=id_boisson
        
        # nombre de boissons (de type I[k]) préparées dans chaque cluster
        self.nb_boisson=nb_boisson
        
        # instants de début de préparation du cluster
        self.t_debut_prep=t_debut_prep
        
        # Indices des commandes concernées par le cluster
        self.commandes_concernees=commandes_concernees
    
    # instant de fin de préparation du cluster
    def t_fin_prep(self):
        return self.t_debut_prep+F(self.nb_boisson, self.id_boisson)
        
    def afficheCluster(self):
        print("CLUSTER ", self.id, " : ","A l'instant ", self.t_debut_prep, ", préparer ", self.nb_boisson, " ",type_boisson[self.id_boisson],"correspondant(s) aux commandes", self.commandes_concernees)


#Donnees

type_boisson=['mojito','bière','caïpirinha','sex on the beach','white russian','long island','caipiroska','cuba libre', 'cosmopolitan']


nb_commandes= gp.nb_commandes_soiree
nb_boissons_diff=gp.N_boissons
nb_max_boissons_par_commmande = gp.A_max

listeParametres = [x.copy() for x in gend.genere_parametres(gp.nb_commandes_soiree)]
 
def matthieu2mailys(commandeMat): #Passe d'une classe Commande à une autre
    boissons=[(x.id)-1 for x in commandeMat.listeBoissons]
    boissons_par_id=[boissons.count(x) for x in range (nb_boissons_diff)]
    commandeMai=Commande(commandeMat.num, commandeMat.instantCommande, boissons_par_id)
    return (commandeMai)

commandes = [matthieu2mailys(x) for x in gend.liste_commandes_soiree]
#commandes = [matthieu2mailys(x) for x in gend.listeCommandes_statique]
print (np.shape(commandes))
t=[x.t for x in commandes]
c=[x.c for x in commandes]

    
    
def F(n,id_boisson):        #Temps de production en fonction du type et du nombre de boissons
    params=listeParametres[id_boisson]
    taille_shaker=params[1]
    if (n==0):
        return 0
    cost=params[2]
    if (n>1):
        for num_boisson in range (2,n+1):
            if (num_boisson%taille_shaker==1):      #On prend un autre shaker
                cost+=params[4]
            else:
                cost+=params[3]
    return cost     

attente_max_acceptee=600



## Fonctions annexes
def id_clusters_concernes(clusters,id_commande):
    id_clust_concernes=[]
    for k in range(len(clusters)):
        clust=clusters[k]
        for id_com in clust.commandes_concernees:
            if id_com==id_commande:
                id_clust_concernes.append(k)
    return id_clust_concernes

# fonction pas encore utilisée
def ajouter_nouvelle_commande(new_comm, instant_new_comm, c, t):
    '''Lorsqu'une nouvelle commande (de type liste) arrive, on l'ajoute à la liste des commandes avec l'instant de cette commande'''
    c.append(new_comm)
    t.append(instant_new_comm)