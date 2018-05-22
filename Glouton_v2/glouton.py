import numpy as np
import matplotlib.pyplot as plt
import time
import random
import copy
#from definition_classes import *

## Données
type_boisson=['mojito','bière','caïpirinha','sex on the beach','white russian','long island','caipiroska']

def F(n): #fonction de production (donne le temps de production de boissons en fonction du nb de boissons - et de son type- à préparer )
    assert(n>=0)
    a=0.15
    F_1=0.75
    if n==0:
        return 0
    if n==1:
        return F_1
    if n>1:
        return (a*n +F_1-a)

attente_max_acceptee=10

## Tracé de la fonction de production
plt.figure(1)
X=[i for i in range(13)]
plt.plot(X,[F(x) for x in X])
plt.xlabel("Nombre de boissons à préparer")
plt.ylabel("Temps de préparation")
plt.title("Fonction de production")
plt.show()

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
        return self.t_debut_prep+F(self.nb_boisson)
        
    def afficheCluster(self):
        print("CLUSTER ", self.id, " : ","A l'instant ", self.t_debut_prep, ", préparer ", self.nb_boisson, " ",type_boisson[self.id_boisson],"correspondant(s) aux commandes", self.commandes_concernees)

## Affichage du planning de production et des temps d'attente

def affiche_plan_prod(clusters,commandes):
    plt.clf()
    plt.figure(1)
    
    #indexCouleurs = {}
    #for id_boisson in range(len(c[0])):
    #    indexCouleurs[id_boisson] = np.random.rand(3,)
    indexCouleurs = [[1,0,0], [0,1,0], [0,0,1], [1,1,0], [1,0,1], [0,1,1], [1,1,1]]
    
    # Une ligne correspond à une commande
    for k in range(len(clusters)):
        clust=clusters[k]
        plt.plot([clust.t_debut_prep,clust.t_debut_prep],[-1,len(commandes)],'k--')
        for com in clust.commandes_concernees:
            plt.plot([clust.t_debut_prep,clust.t_fin_prep()],[com,com],color=indexCouleurs[clust.id_boisson],linewidth=10)
            plt.text(clust.t_debut_prep,com,str(commandes[com].c[clust.id_boisson]),fontsize=8)
        txt=str(clust.nb_boisson)
        plt.text(clust.t_debut_prep,-1,txt,fontsize=10)
        
    #légende
    for j in range(len(commandes[0].c)):
        plt.plot([0,0],[0,0],color=indexCouleurs[j],label=type_boisson[j])
    
    plt.title("Planning de production des commandes")
    plt.xlabel("temps")
    plt.ylabel("indice de commande")
    plt.legend()
    plt.show()
    
def affiche_attentes(clusters,commandes):
    clusters_sans_opti=planning_sans_opti(commandes)
    attente_tot=0
    attente_tot_sans_opti=0
    
    plt.figure(2)
    
    attentes_sans_opti=[]
    attentes=[]
    
    for comm in commandes:
        attente_sans_opti=comm.attente(clusters_sans_opti)
        attente=comm.attente(clusters)
        attentes_sans_opti.append(attente_sans_opti)
        attentes.append(attente)
        attente_tot_sans_opti+=attente_sans_opti
        attente_tot+=attente
    
    plt.plot(attentes_sans_opti, label="sans optimisation")
    plt.plot(attentes,label="avec optimisation")
    plt.title('Temps d attente pour chaque commandes')
    plt.xlabel('Indices commandes')
    plt.ylabel('Temps d attente')
    plt.legend()
    plt.show()
    
    print()
    print("Temps d'attente total sans optimisation: ",attente_tot_sans_opti)
    print("Temps d'attente total avec optimisation: ",attente_tot)
    gain_attente=(attente_tot_sans_opti-attente_tot)/attente_tot_sans_opti
    print("Gain sur l'attente: ", gain_attente)
    
    print()
    t_fin_prep_tot=clusters[-1].t_fin_prep()
    t_fin_prep_tot_sans_opti=clusters_sans_opti[-1].t_fin_prep()
    print("Temps de préparation total sans optimisation: ", clusters_sans_opti[-1].t_fin_prep())
    print("Temps de préparation total avec optimisation: ", clusters[-1].t_fin_prep())
    gain_prod = (t_fin_prep_tot_sans_opti-t_fin_prep_tot)/t_fin_prep_tot_sans_opti
    print("Gain de productivité: ", gain_prod)
    return gain_attente, gain_prod
    
## Voir la rentabilité de l'optimisation

def planning_sans_opti(commandes):
    clusters_sans_opti=[]    
    nb_commandes=len(commandes)
    j_max=len(commandes[0].c) # Nombre de types de boissons différents
    
    #--------------------- Initialisation ---------------------
    # Dans le premier cluster, on prépare la première boisson demandée à la première commande
    prem_boiss=0
    while commandes[0].c[prem_boiss]==0:
        prem_boiss+=1;
    
    clusters_sans_opti.append(Cluster(0,0,prem_boiss,c[0][prem_boiss],[0]))
        
    #----------------------------------------------------------
    i=1
    for ind_commande in range(nb_commandes):
        for ind_boisson in range(j_max):
            if(commandes[ind_commande].c[ind_boisson]!=0 and (ind_commande!=0 or ind_boisson!=0)):
                clusters_sans_opti.append(Cluster(i,clusters_sans_opti[-1].t_fin_prep(),ind_boisson,commandes[ind_commande].c[ind_boisson],[ind_commande]))
                i+=1
    return clusters_sans_opti
    
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
    

## Algo

def glouton(commandes):
    
    nb_commandes=len(commandes)
    j_max=len(commandes[0].c) # Nombre de types de boissons différents
    
    #--------------------- Initialisation ---------------------
    # Dans le premier cluster, on prépare la première boisson demandée à la première commande
    prem_boiss=0
    while commandes[0].c[prem_boiss]==0:
        prem_boiss+=1;
        
    # liste pour chaque boisson des clusters correspondant à cette boisson
    clusters_par_boisson=[]
    for j in range (j_max):
        clusters_par_boisson.append([])
    
    clusters=[]
    clusters.append(Cluster(0,0,prem_boiss,c[0][prem_boiss],[0]))
    clusters_par_boisson[prem_boiss].append(0)
    
    #----------------------------------------------------------
    
    # On parcourt chaque groupes de boissons pour chaque commandes et on place au mieux ce groupe dans le plan de production
    
    for ind_commande in range(nb_commandes):    
        for ind_boisson in range(j_max):
            comm=commandes[ind_commande]
            
            if(comm.c[ind_boisson]!=0 and (ind_commande!=0 or ind_boisson!=0)):
                
                clusters_opti=copy.deepcopy(clusters)
                clusters_par_boisson_explo=copy.deepcopy(clusters_par_boisson)
                
                # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                # On ajoute d'abord la boisson dans un nouveau cluster à la suite des autres,
                # sans grouper les préparations
                clust_prec=clusters[-1]
                
                id_new_cluster=len(clusters)
                clusters.append( Cluster(id_new_cluster,clust_prec.t_fin_prep(),ind_boisson,comm.c[ind_boisson],[ind_commande]) )
                
                clusters_par_boisson[ind_boisson].append(id_new_cluster)
                
                # on calcule le temps d'attente total induit
                attente_tot_ssOpti=0
                for commande in commandes[0:ind_commande+1]:
                    attente_tot_ssOpti+=commande.attente(clusters)
                # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                
                
                # Si c'est possible, on groupe la préparation de la boisson d'indice 'ind_boisson' dans le cluster le plus proche (le plus récent)
                
                if (clusters_par_boisson_explo[ind_boisson]!=[]):
                    ind_nearest_cluster=clusters_par_boisson_explo[ind_boisson][-1]
                    nearest_clust=clusters_opti[ind_nearest_cluster]
                    #if(len(nearest_clust.commandes_concernees)<5)
                    if (len(nearest_clust.commandes_concernees)<5 and nearest_clust.t_debut_prep > comm.t):
                        ancien_nb_boisson=nearest_clust.nb_boisson
                        nearest_clust.nb_boisson+=comm.c[ind_boisson]
                        nearest_clust.commandes_concernees.append(ind_commande)
                        # on décale ainsi les instants de début de préparation des clusters suivants
    
                        # (on ajoute le temps de préparation supplémentaire)
                        tps_ajout=F(nearest_clust.nb_boisson)- F(ancien_nb_boisson)
                        for k in range(ind_nearest_cluster +1,len(clusters_opti)):
                            clusters_opti[k].t_debut_prep+=tps_ajout
                            
                        clusters_par_boisson_explo[ind_boisson].append(ind_nearest_cluster)
                            
                        # et on calcule le temps d'attente total avec ce plan de production 
                        attente_tot_acOpti=0
                        for comm in commandes[0:ind_commande+1]:
                            attente_tot_acOpti+=comm.attente(clusters_opti)
                        
                        # on conserve le meilleur plan des deux
                        if attente_tot_acOpti<attente_tot_ssOpti:
                            # en vérifiant si ça ne fait pas dépasser le temps d'attente maximal
                            attente_max_ssOpti=max(comm.attente(clusters) for comm in commandes[0:ind_commande+1])
                            attente_max_acOpti=max(comm.attente(clusters_opti) for comm in commandes[0:ind_commande+1])
                            if (attente_max_acOpti<attente_max_acceptee or attente_max_ssOpti>attente_max_acceptee): 
                                clusters=copy.deepcopy(clusters_opti)
                                clusters_par_boisson=copy.deepcopy(clusters_par_boisson_explo)
        
    print()
    print("Plan de production final: ")
    for clust_final in clusters:
        clust_final.afficheCluster()
    
    print("Temps d'attente maximal par commande avec opti: ",max(comm.attente(clusters) for comm in commandes))
    return clusters
    
## Test algo
#t=[0,1,1.5,2] #,2.2,2.4,3,3.3] # instants de commande
#c=[[1,1,0], [2,0,3], [4,2,1], [0,0,1]] # tableau de commandes (x4 commandes)
#liste_clusters=glouton(c,t)
#c=[[1,0,1], [1,2,0], [0,0,1], [4,0,1], [1,2,1], [8,0,0], [0,1,1], [1,2,0], [1,2,0], [0,0,1], [4,0,1], [1,2,1]]
#c=[[0,1,4,1],[1,0,3,1],[1,1,4,1]] 
#t=[0,1,1.5,2,2.2,2.4,3,3.3,4,4.1,4.8,5.2]

# -----------  Génération aléatoire de données  -----------
nb_commandes=10
nb_boissons_diff=7
nb_max_boissons_par_commmande=7
c=[]
t=[]

choix_nb_boissons=[]
for i in range(nb_max_boissons_par_commmande):
    choix_nb_boissons.append(0)
    choix_nb_boissons.append(i)
   
def genere_comm():
    t_interv_commandes=abs(np.random.randn(20)*0.5+1) #les commandes se succèdent avec un intervalle de temps ~entre 0 et 2min (loi gaussienne de moyenne 1)
    
    for i in range(nb_commandes):
        c.append([])
        for j in range(nb_boissons_diff):
            c[i].append(random.choice(choix_nb_boissons))
        if i==0:
            t.append(0)
        else:
            t.append(t[-1]+t_interv_commandes[i])
            #t.append(0)
    
    commandes=[]
    for i in range (len(c)):
        commandes.append(Commande(i,t[i],c[i]))
    return commandes
# -------------------------------------------------------------
gain_attente_moy=0
gain_prod_moy=0
for i in range (10):
    commandes=genere_comm()
    plt.clf()
    clusters=glouton(commandes)
    affiche_plan_prod(clusters,commandes)
    gain_attente, gain_prod=affiche_attentes(clusters,commandes)
    gain_attente_moy+=gain_attente
    gain_prod_moy+=gain_prod

print("Gain moyen sur l'attente: ", gain_attente_moy)
print("Gain de productivité moyen: ", gain_prod_moy)

### idées pour insérer temps
# file_attente=[[1, 1, 0], [2, 0, 3], [4, 2, 1], [0, 0, 1],[1,1,1][0,1,0],[1,2,3]]
# c_test=[]
# t_test=[]
# glouton(c_test,t_test)
# 
# attente=0
# 
# for i in range(len(file_attente)):
#     t=time.clock()
#     
#     print("Nouvelle commande!")
#     ajouter_nouvelle_commande(file_attente[0],t+attente,c_test,t_test)
#     clusters_prov=glouton(c_test,t_test)
#     
#     attente=random.randint(0,18)/3
#     time.sleep(attente)
#     retirer_commandes_livrees(c_test,t_test)