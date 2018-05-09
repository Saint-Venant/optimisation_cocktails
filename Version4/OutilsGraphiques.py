'''
Regroupe toutes les fonctions permettant d'afficher des informations ou de tracer des graphes pour visualiser des données
'''

from StructuresProduction import *
import numpy as np
import matplotlib.pyplot as plt


def arrondi(x, decimal):
    return int((10**decimal)*x)/10**decimal


def affiche_commandes(listeCommandes):
    '''
    affiche les informations d'une liste de commandes
    '''
    print("Afichage des commandes")
    print()
    for c in listeCommandes:
        print("commande num", c.num)
        print("instant de commande :", c.instantCommande)
        c.afficheBoissons()
        print()
    print()


def affiche_parametres(listeParametres):
    '''
    affiche les informations d'une liste de paramètres
    '''
    print("Affichage des paramètres de production des boissons")
    print()
    for param in listeParametres:
        print("boisson de type", param[0])
        print("taille cluster optimale :", param[1])
        print("coefficients :", [arrondi(x, 2) for x in param[2:]])
        print()

def attente_commandes(listeCommandes):
    '''
    Retourne la liste des temps d'attente livraison pour chaque commande
    Suppose que la fonction calculeProd ait été appelée précédemment
    '''
    N = len(listeCommandes)
    attente = np.zeros([N,2])
    i = 0
    for com in listeCommandes:
        attente[i, 0] = com.num
        attente[i, 1] = com.livraison - com.instantCommande
        i += 1
    return attente

def attente_boissons(listeCommandes):
    '''
    Retourne la liste des temps d'attente des boissons avant d'être servies
    Suppose que la fonction calculeProd ait été appelée précédemment
    '''
    N = 0
    for com in listeCommandes:
        N += com.nbBoissons
    attente = np.zeros([N,2])
    i = 0
    for com in listeCommandes:
        for b in com.listeBoissons:
            attente[i,0] = i
            attente[i,1] = b.livraison - b.debut
            i += 1
    return attente

def plot_attente_boissons(vect_attentes, vect_titres, taille_bin):
    N = len(vect_attentes)
    labelx = "temps d'attente"
    labely = "nombre de boissons"
    titre = "Distribution des temps d'attente avant livraison \n des boissons : "
    
    if N == 1:
        plt.title(titre+vect_titres[0])
        plt.xlabel(labelx)
        plt.ylabel(labely)
        plt.hist(vect_attentes[0][:,1], bins=taille_bin, facecolor='b')
    elif N == 2:
        plt.subplot(121)
        plt.title(titre+vect_titres[0])
        plt.xlabel(labelx)
        plt.ylabel(labely)
        plt.hist(vect_attentes[0][:,1], bins=taille_bin, facecolor='b')
        
        plt.subplot(122)
        plt.title(titre+vect_titres[1])
        plt.xlabel(labelx)
        plt.ylabel(labely)
        plt.hist(vect_attentes[1][:,1], bins=taille_bin, facecolor='r')
    elif N == 3:
        plt.subplot(131)
        plt.title(titre+vect_titres[0])
        plt.xlabel(labelx)
        plt.ylabel(labely)
        plt.hist(vect_attentes[0][:,1], bins=taille_bin, facecolor='b')
        
        plt.subplot(132)
        plt.title(titre+vect_titres[1])
        plt.xlabel(labelx)
        plt.ylabel(labely)
        plt.hist(vect_attentes[1][:,1], bins=taille_bin, facecolor='r')
        
        plt.subplot(133)
        plt.title(titre+vect_titres[2])
        plt.xlabel(labelx)
        plt.ylabel(labely)
        plt.hist(vect_attentes[2][:,1], bins=taille_bin, facecolor='g')
    else:
        print("problème avec la fonction plot_attente_boissons \n\n")

def plot_attente_commandes(vect_attentes, vect_labels, param_moy=None):
    '''
    Trace l'attente subies par les diférentes commandes
    param_moy = [l1, l2, label1, label2] où :
        l1 : liste de la moyenne
        l2 : moyenne + x = borne jugée acceptable
        labels : labels des 2 dernières courbes
    '''
    N = len(vect_attentes)
    plt.title("Temps d'attente par commande \n en fonction du type de plan de production")
    plt.xlabel("identifiant de commande")
    plt.ylabel("temps d'attente")
    
    if N == 2:
        plt.plot(vect_attentes[0][:,0], vect_attentes[0][:,1], 'bo', label=vect_labels[0])
        plt.plot(vect_attentes[1][:,0], vect_attentes[1][:,1], 'ro', label=vect_labels[1])
    elif N == 3:
        plt.plot(vect_attentes[0][:,0], vect_attentes[0][:,1], 'bo', label=vect_labels[0])
        plt.plot(vect_attentes[1][:,0], vect_attentes[1][:,1], 'ro', label=vect_labels[1])
        plt.plot(vect_attentes[2][:,0], vect_attentes[2][:,1], 'go', label=vect_labels[2])
    else:
        print("Problème dans la fonction plot_attente_commandes")
    
    if param_moy != None:
        plt.plot(param_moy[0], 'k-', label=param_moy[2])
        plt.plot(param_moy[1], 'k--', label=param_moy[3])
    
    plt.legend()

def hist_attente_commandes(vect_attentes, vect_titres, finesse):
    '''
    Trace l'histogramme de la distribution des temps d'attente commandes
    '''
    N = len(vect_attentes)
    titre = "Distribution des temps d'attente commande\n"
    
    if N == 3:
        plt.subplot(131)
        plt.title(titre + vect_titres[0])
        plt.hist(vect_attentes[0][:,1], finesse, facecolor='b')
        plt.xlabel("temps d'attente clients")
        plt.ylabel("effectif")
        
        plt.subplot(132)
        plt.title(titre + vect_titres[1])
        plt.hist(vect_attentes[1][:,1], finesse, facecolor='r')
        plt.xlabel("temps d'attente clients")
        plt.ylabel("effectif")
        
        plt.subplot(133)
        plt.title(titre + vect_titres[2])
        plt.hist(vect_attentes[2][:,1], finesse, facecolor='g')
        plt.xlabel("temps d'attente clients")
        plt.ylabel("effectif")

def plot_preparation_parallele(vect_prep, vect_labels):
    '''
    Trace l'évolution du nombre de commandes préparées en parallèle (non livrées, dont au moins une boisson à commencer à être produite)
    '''
    N = len(vect_prep)
    plt.title("Nombre de commandes préparées en parallèle")
    plt.xlabel("temps")
    plt.ylabel("nombre de commandes différentes en cours de préparation")
    
    if N == 2:
        plt.plot(vect_prep[0], 'b', label=vect_labels[0])
        plt.plot(vect_prep[1], 'r', label=vect_labels[1])
        plt.legend()
        xmin = 0
        xmax = max([len(x) for x in vect_prep])
        ymin = min([min(x) for x in vect_prep]) - 1
        ymax = max([max(x) for x in vect_prep]) + 1
        plt.axis([xmin, xmax, ymin, ymax])
    elif N == 3:
        plt.plot(vect_prep[0], 'b', label=vect_labels[0])
        plt.plot(vect_prep[1], 'r', label=vect_labels[1])
        plt.plot(vect_prep[2], 'g', label=vect_labels[2])
        plt.legend()
        xmin = 0
        xmax = max([len(x) for x in vect_prep])
        ymin = min([min(x) for x in vect_prep]) - 1
        ymax = max([max(x) for x in vect_prep]) + 1
        plt.axis([xmin, xmax, ymin, ymax])
    else:
        print("Problème dans la fonction plot_preparation_parallele")

def plot_taille_commandes(listeCommandes, tailleMax):
    '''
    Trace l'histogramme représentant la distribution de la taille des commandes
    '''
    taille = []
    for c in listeCommandes:
        taille.append(len(c.listeBoissons))
    choix_bins = list(range(1, tailleMax+2))
    plt.figure(7)
    plt.hist(taille, bins=choix_bins)
    plt.xlabel("nombre de boissons")
    plt.ylabel("effectif")
    plt.title("Distribution du nombre de boissons par commande")

def plot_recuit(vectEnergie, vect_labels):
    '''
    Trace la progression d'un recuit simulé
    '''
    N = len(vectEnergie)
    plt.title("Progression du recuit")
    plt.xlabel("itération")
    plt.ylabel("temps total de production")
    
    if N == 1:
        plt.plot(vectEnergie[0], 'bo', label=vect_labels[0])
    elif N == 2:
        plt.plot(vectEnergie[0], 'bo', label=vect_labels[0])
        plt.plot(vectEnergie[1], 'ro', label=vect_labels[1])
    else:
        print("Problème dans la fonction plot_recuit")
    plt.legend()

def plot_planning(plan):
    '''
    Trace le planning de production selon un plan de production donné
    >> permet de visualiser le groupement des commandes
    '''
    if plan.type_prod == "buffer":
        #lie une commande à une couleur
        indexCouleurs = OrderedDict()
        for com in plan.commandes:
            c = np.random.rand(3,)
            indexCouleurs[com] = c
        
        #affiche la production de chaque cluster
        for cl in plan.clusters:
            b1 = cl[0]
            b2 = cl[-1]
            plt.axvline(x=b1.debut, c='k', linestyle='--')
            plt.axvline(x=b2.fin, c='k', linestyle='--')
            for b in cl:
                num = b.commande.num
                plt.plot([b1.debut, b2.fin], [num, num], color=indexCouleurs[b.commande], linewidth=10)
        plt.axis([plan.instantProd, plan.clusters[-1][-1].fin, -1, len(plan.commandes)])
        plt.title("Planning de production des commandes :\nfonctionnement 'buffer'")
        plt.xlabel("temps")
        plt.ylabel("indice de commande")
    elif plan.type_prod == "soiree":
        #lie une commande à une couleur
        indexCouleurs = OrderedDict()
        for cl in plan.histoire:
            for b in cl:
                com = b.commande
                c = np.random.rand(3,)
                indexCouleurs[com] = c
        
        #affiche la production de chaque cluster (déjà produits dans le fonctionnement "soiree")
        for cl in plan.histoire:
            b1 = cl[0]
            b2 = cl[-1]
            plt.axvline(x=b1.debut, c='k', linestyle='--')
            plt.axvline(x=b2.fin, c='k', linestyle='--')
            for b in cl:
                num = b.commande.num
                plt.plot([b1.debut, b2.fin], [num, num], color=indexCouleurs[b.commande], linewidth=10)
        plt.axis([plan.instantDebutTotal, plan.histoire[-1][-1].fin, -1, len(indexCouleurs)])
        plt.title("Planning de production des commandes :\nfonctionnement 'soiree'")
        plt.xlabel("temps")
        plt.ylabel("indice de commande")
    else:
        print("Problème dans la fonction plot_planning")

def plot_rush(vect_rush, vect_labels):
    '''
    Trace le nombre de commandes de retard qu'a le barman (ie commandées mais non livrées) en fonction du temps
    >> permet de visualiser les périodes de pointe dans l'affluence
    '''
    N = len(vect_rush)
    
    plt.title("Nombre de commandes en attentes\n(commandées mais non livrées)")
    plt.xlabel("temps")
    plt.ylabel("nombre de commandes")
    
    if N == 1:
        plt.plot(vect_rush[0], c='b', label=vect_labels[0])
    elif N == 2:
        plt.plot(vect_rush[0], c='b', label=vect_labels[0])
        plt.plot(vect_rush[1], c='r', label=vect_labels[1])
    elif N == 3:
        plt.plot(vect_rush[0], c='b', label=vect_labels[0])
        plt.plot(vect_rush[1], c='r', label=vect_labels[1])
        plt.plot(vect_rush[2], c='g', label=vect_labels[2])
    else:
        print("Poblème dans la fonction plot_rush")
    plt.legend()