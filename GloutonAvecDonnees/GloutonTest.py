# -*- coding: utf-8 -*-
"""
Created on Thu May 24 16:21:13 2018

@author: Diane
"""

import numpy as np
import matplotlib.pyplot as plt
import time
import random
import copy
from StructuresProduction import *
import OutilsGraphiques as outg
from donnees import*



## Tracé de la fonction de production
plt.figure(1)
X=[i for i in range(13)]
for id_boisson in range (nb_boissons_diff):
    plt.plot(X,[F(x,id_boisson+1) for x in X])
    plt.xlabel("Nombre de boissons à préparer")
    plt.ylabel("Temps de préparation")
    titre = "Fonction de production du " + str(type_boisson[id_boisson])
    plt.title(titre)
    plt.show()
    
#Zoom sur la fonction de production du sex on the beach
X_zoom=[i for i in range(6)]
plt.plot(X_zoom,[F(x,3) for x in X_zoom])
plt.xlabel("Nombre de boissons à préparer")
plt.ylabel("Temps de préparation")
titre = "Fonction de production du sex on the beach"
plt.title(titre)
plt.show()

## Affichage du planning de production et des temps d'attente

def affiche_plan_prod(clusters,commandes):
    plt.clf()
    plt.figure(1,figsize=(60,30))
    
    indexCouleurs = {}
    for id_boisson in range(len(c[0])):
        indexCouleurs[id_boisson] = np.random.rand(3,)
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
    
def gain_total (clusters_sans_opti, clusters_opti):
    ecart=0
    for i in range (len(clusters_opti)):
        cluster_opti=clusters_opti[i]
        cluster_non_opti = clusters_sans_opti[i]
        tps_non_opti = cluster_non_opti.t_fin_prep()-cluster_non_opti.t_debut_prep
        tps_opti=cluster_opti.t_fin_prep()-cluster_opti.t_debut_prep
    for i in range (len(clusters_opti), len(clusters_sans_opti)):
        cluster_non_opti = clusters_sans_opti[i]
        ecart+=cluster_non_opti.t_fin_prep()-cluster_non_opti.t_debut_prep
    return (ecart)
    
def affiche_attentes(clusters,commandes):
    clusters_sans_opti=planning_sans_opti(commandes)
    print ("cb de clusters init ?", len(clusters_sans_opti))
    print ("cb de clusters opti ?", len(clusters))
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
    print("Gain de productivité final: ", gain_prod)
    
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

    

## Algo

def glouton(commandes,verbose=False):
    
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
    print (nb_commandes)
    for ind_commande in range(nb_commandes):
        if (ind_commande%30==0):
            print (ind_commande)
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
                    if (len(nearest_clust.commandes_concernees)<listeParametres[ind_boisson][1] and nearest_clust.t_debut_prep > comm.t):
                        ancien_nb_boisson=nearest_clust.nb_boisson
                        nearest_clust.nb_boisson+=comm.c[ind_boisson]
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
    if (verbose):
        for clust_final in clusters:
            clust_final.afficheCluster()
    
    print("Temps d'attente maximal par commande avec opti: ",max(comm.attente(clusters) for comm in commandes))
    return clusters


#liste_clusters2=glouton(commandes)
#debut_clusters=liste_clusters2[100:130]
#debut_commandes=commandes[100:130]
#affiche_plan_prod(debut_clusters,commandes)
#affiche_attentes(liste_clusters2, commandes)

gain_attente_moy=0
gain_prod_moy=0
gain_total_moy=0
n_moy=20
for i in range (n_moy):
    print (i)
    commandes_gen=gend.genere_commandes_soiree(gp.debut_soiree, gp.fin_soiree, 1)
    commandes = [matthieu2mailys(x) for x in commandes_gen]
    print (np.shape(commandes))
    t=[x.t for x in commandes]
    c=[x.c for x in commandes]
    plt.clf()
    clusters=glouton(commandes)
    affiche_plan_prod(clusters,commandes)
    gain_attente, gain_prod=affiche_attentes(clusters,commandes)
    gain_attente_moy+=gain_attente
    gain_prod_moy+=gain_prod
    

print("Gain moyen sur l'attente: ", gain_attente_moy/n_moy)
print("Gain de productivité moyen: ", gain_prod_moy/n_moy)

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