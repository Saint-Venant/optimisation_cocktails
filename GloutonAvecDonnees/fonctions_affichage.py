# Fonctions d'affichage

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
##

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