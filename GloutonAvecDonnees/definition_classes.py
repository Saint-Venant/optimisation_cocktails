# Définition des classes

from donnees import *

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
        return self.t_debut_prep+F(self.nb_boisson)
        
    def afficheCluster(self):
        print("CLUSTER ", self.id, " : ","A l'instant ", self.t_debut_prep, ", préparer ", self.nb_boisson, " ",type_boisson[self.id_boisson],"correspondant(s) aux commandes", self.commandes_concernees)
