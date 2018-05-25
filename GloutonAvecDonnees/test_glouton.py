# -*- coding: utf-8 -*-
"""
Created on Mon May 21 23:49:03 2018

@author: Diane
"""

from StructuresProduction import *
import GlobalParam as gp
import GenerationDonnees as gend
import OutilsGraphiques as outg
import matplotlib.pyplot as plt
import numpy as np

import time
import random
import copy
#from definition_classes import *

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

## Données
type_boisson=['mojito','bière','caïpirinha','sex on the beach','white russian','long island','caipiroska','cuba libre', 'cosompolitan']
#type_boisson= gp.noms_boissons


        
        # -----------  Génération aléatoire de données  -----------
# =============================================================================
# nb_commandes=10
# nb_boissons_diff=7
# nb_max_boissons_par_commmande=7
# c=[]
# t=[]
# 
# choix_nb_boissons=[]
# for i in range(nb_max_boissons_par_commmande):
#     choix_nb_boissons.append(0)
#     choix_nb_boissons.append(i)
#     
t_interv_commandes=abs(np.random.randn(20)*0.5+1) #les commandes se succèdent avec un intervalle de temps ~entre 0 et 2min (loi gaussienne de moyenne 1)
# 
# for i in range(nb_commandes):
#     c.append([])
#     for j in range(nb_boissons_diff):
#         c[i].append(random.choice(choix_nb_boissons))
#     if i==0:
#         t.append(0)
#     else:
#         t.append(t[-1]+t_interv_commandes[i]) 
# 
# commandes=[]
# for i in range (len(c)):
#     commandes.append(Commande(i,t[i],c[i]))
# =============================================================================
        
 #Données
 
#listeParametres = gend.genere_parametres(gp.nb_commandes_soiree)
#debut_soiree = gp.debut_soiree
 
#listeCommandes = [x.copy() for x in gend.listeCommandes_statique]
 
nb_commandes= gp.nb_commandes_soiree
nb_boissons_diff=gp.N_boissons
print (nb_boissons_diff)
nb_max_boissons_par_commmande = gp.A_max

listeParametres = [x.copy() for x in gend.genere_parametres(gp.nb_commandes_soiree)]

print (listeParametres[0])
 
def matthieu2mailys(commandeMat): #Passe d'une classe Commande à une autre
    boissons=[x.id for x in commandeMat.listeBoissons]
    boissons_par_id=[boissons.count(x) for x in range (nb_boissons_diff)]
    commandeMai=Commande(commandeMat.num, commandeMat.instantCommande, boissons_par_id)
    return (commandeMai)




#commandes = [matthieu2mailys(x) for x in gend.liste_commandes_soiree]
commandes = [matthieu2mailys(x) for x in gend.listeCommandes_statique]
print (np.shape(commandes))
t=[x.t for x in commandes]
c=[x.c for x in commandes]

        
        

# =============================================================================
# def matthieu2mailys(liste_com, nb_boissons):
# #Transforme une liste de commandes de la forme [idCommande1,...,idCommanden] en une liste de la forme [nbCommande1,...,nbCommandeN]
#     nb_com=len(liste_com)
#     c=np.zeros((nb_com, nb_boissons))
#     temps=[]
#     for num_com in range(nb_com):
#         temps.append((liste_com[num_com]).instantCommande)
#         for boisson in (liste_com[num_com]).listeBoissons:
#             c[num_com][boisson.id-1]+=1
#     return (np.array(c),temps)        
# 
# def mailys2matthieu(matrice_com, temps):
# #Transforme une liste de commandes de la forme[nbCommande1,...,nbCommandeN] en une liste de la forme [idCommande1,...,idCommanden]
#     liste_com=[]
#     (nb_com, nb_boissons)=np.shape(matrice_com)
#     for com in range(nb_com):
#         t=temps[com]
#         new_com=commande(com,t)
#         for id_boisson in range (nb_boissons):
#             for n in range(int(matrice_com[com][id_boisson])):
#                 b=boisson(id_boisson+1, new_com, n)
#                 new_com.ajouteBoisson(b)
#                 triIntraCommandes(new_com)
#         liste_com.append(new_com)
#     return (liste_com)  
#                 
# =============================================================================
# =============================================================================
# 
# def F(n): #fonction de production (donne le temps de production de boissons en fonction du nb de boissons - et de son type- à préparer )
#     assert(n>=0)
#     a=0.15
#     F_1=0.75
#     if n==0:
#         return 0
#     if n==1:
#         return F_1
#     if n>1:
#         return (a*n +F_1-a)
# =============================================================================

def F(n,id_boisson):
    params=listeParametres[id_boisson-1]
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

## Tracé de la fonction de production
plt.figure(1)
X=[i for i in range(13)]
for id_boisson in range (nb_boissons_diff):
    plt.plot(X,[F(x,id_boisson) for x in X])
    plt.xlabel("Nombre de boissons à préparer")
    plt.ylabel("Temps de préparation")
    titre = "Fonction de production du " + str(type_boisson[id_boisson])
    plt.title(titre)
    plt.show()

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

## Affichage du planning de production

def affiche_plan_prod(clusters,commandes):
    plt.clf()
    plt.figure(1)
    
    indexCouleurs = {}
    for id_boisson in range(len(c[0])):
        indexCouleurs[id_boisson] = np.random.rand(3,)
    #indexCouleurs = [[1,0,0], [0,1,0], [0,0,1], [1,1,0], [1,0,1], [0,1,1], [1,1,1]]
    
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
    print("Gain sur l'attente: ", (attente_tot_sans_opti-attente_tot)/attente_tot_sans_opti)
    
    print()
    t_fin_prep_tot=clusters[-1].t_fin_prep()
    t_fin_prep_tot_sans_opti=clusters_sans_opti[-1].t_fin_prep()
    print("Temps de préparation total sans optimisation: ", clusters_sans_opti[-1].t_fin_prep())
    print("Temps de préparation total avec optimisation: ", clusters[-1].t_fin_prep())
    print("Gain de productivité: ", (t_fin_prep_tot_sans_opti-t_fin_prep_tot)/t_fin_prep_tot_sans_opti)
    
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
    print ("1er", clusters[0].id_boisson)
    clusters_par_boisson[prem_boiss].append(0)
    
    #----------------------------------------------------------
    
    # On parcourt chaque groupes de boissons pour chaque commandes et on place au mieux ce groupe dans le plan de production
    print (np.shape(commandes))
    print (j_max)
    for ind_commande in range(nb_commandes): 
        for ind_boisson in range(j_max):
            
            if(commandes[ind_commande].c[ind_boisson]!=0 and (ind_commande!=0 or ind_boisson!=0)):
                
                clusters_opti=copy.deepcopy(clusters)
                clusters_par_boisson_explo=copy.deepcopy(clusters_par_boisson)
                
                # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                # On ajoute d'abord la boisson dans un nouveau cluster à la suite des autres,
                # sans grouper les préparations
                clust_prec=clusters[-1]
                
                id_new_cluster=len(clusters)
                clusters.append( Cluster(id_new_cluster,clust_prec.t_fin_prep(),ind_boisson,commandes[ind_commande].c[ind_boisson],[ind_commande]) )
                clusters_par_boisson[ind_boisson].append(id_new_cluster)
                
                # on calcule le temps d'attente total induit
                attente_tot_ssOpti=0
                for comm in commandes[0:ind_commande+1]:
                    attente_tot_ssOpti+=comm.attente(clusters)
                # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                
                
                # Si c'est possible, on groupe la préparation de la boisson d'indice 'ind_boisson' dans le cluster le plus proche (le plus récent)
                
                if (clusters_par_boisson_explo[ind_boisson]!=[]):
                    ind_nearest_cluster=clusters_par_boisson_explo[ind_boisson][-1]
                    nearest_clust=clusters_opti[ind_nearest_cluster]
                    ancien_nb_boisson=nearest_clust.nb_boisson
                    nearest_clust.nb_boisson+=commandes[ind_commande].c[ind_boisson]
                    nearest_clust.commandes_concernees.append(ind_commande)
                    # on décale ainsi les instants de début de préparation des clusters suivants

                    # (on ajoute le temps de préparation supplémentaire)
                    tps_ajout=F(nearest_clust.nb_boisson,ind_boisson)- F(ancien_nb_boisson,ind_boisson)
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
    affiche_plan_prod(clusters,commandes)
    affiche_attentes(clusters,commandes)
    return clusters
    
## Test algo
#t=[0,1,1.5,2] #,2.2,2.4,3,3.3] # instants de commande
#c=[[1,1,0], [2,0,3], [4,2,1], [0,0,1]] # tableau de commandes (x4 commandes)
#liste_clusters=glouton(c,t)
#c=[[1,0,1], [1,2,0], [0,0,1], [4,0,1], [1,2,1], [8,0,0], [0,1,1], [1,2,0], [1,2,0], [0,0,1], [4,0,1], [1,2,1]]
#c=[[0,1,4,1],[1,0,3,1],[1,1,4,1]] 
#t=[0,1,1.5,2,2.2,2.4,3,3.3,4,4.1,4.8,5.2]


# -------------------------------------------------------------

liste_clusters2=glouton(commandes)
