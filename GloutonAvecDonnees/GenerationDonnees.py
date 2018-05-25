from StructuresProduction import *
import GlobalParam as gp
import numpy as np
import time

## Graine aléatoire

#np.random.seed(2)


## Outils génériques

def tire_nb_boissons(mu, sigma):
    '''
    tire un nombre de boissons selon une loi gaussienne tronquée
    '''
    nb = int(np.random.normal(loc=mu, scale=sigma))
    while (nb <= 0) or (nb > gp.A_max):
        nb = int(np.random.normal(loc=mu, scale=sigma))
    return nb


def genere_commandes_uniformes(instant, periode, nb_commandes):
    '''
    génère une liste de commandes à partir d'un instant donné
    instant d'arrivée des commandes tiré selon une loi uniforme entre [0, periode]
    '''
    liste = []
    temps = instant
    for i in range(nb_commandes):
        c = commande(i, temps)
        temps += np.random.randint(gp.periodeArrivee+1)
        nbBoissonsCommandees = tire_nb_boissons(gp.mu_distrib_b, gp.sigma_distrib_b)
        for j in range(nbBoissonsCommandees):
            b = boisson(np.random.randint(1, gp.N_boissons+1))
            c.ajouteBoisson(b)
        triIntraCommandes(c)
        liste.append(c)
    return liste

def genere_commandes_soiree(debut, fin, nb):
    '''
    génère une liste de commandes entre les intants debut et fin
    instant d'arrivée tirés selon une loi gaussienne tronquée
    '''
    # Distribution (gaussienne) des instants d'arrivée des commandes
    sigma_arrivees = gp.fin_soiree / 4
    distrib_gaussian = np.random.normal(gp.fin_soiree/2, sigma_arrivees, int(gp.nb_commandes_soiree*2/3))
    distrib_uniform = np.random.uniform(gp.debut_soiree, gp.fin_soiree, int(gp.nb_commandes_soiree/3))
    distrib_arrivees = np.concatenate((distrib_gaussian, distrib_uniform))
    for i in range(gp.nb_commandes_soiree):
        while (distrib_arrivees[i] < 0) or (distrib_arrivees[i] > gp.fin_soiree):
            distrib_arrivees[i] = np.random.normal(gp.fin_soiree/2, sigma_arrivees)
    distrib_arrivees = np.sort(distrib_arrivees)
    
    # liste des commandes de la soirée
    liste_commandes_soiree = []
    for i in range(gp.nb_commandes_soiree):
        temps = distrib_arrivees[i]
        c = commande(i, temps)
        nb_boissons = tire_nb_boissons(gp.mu_distrib_b, gp.sigma_distrib_b)
        for j in range(nb_boissons):
            b = boisson(np.random.randint(1, gp.N_boissons+1))
            c.ajouteBoisson(b)
        liste_commandes_soiree.append(c)
    
    return liste_commandes_soiree

## création des commandes statiques ("buffer")

'''
Crée une liste de commandes à l'arrivée selon une loi uniforme
statique >> destiné à une optimisation d'un seul coup (de type "buffer")
'''
listeCommandes_statique = genere_commandes_uniformes(0, gp.periodeArrivee, gp.nbCommandes_statique)



## génération des paramètres du temps de préparation

'''
Stockage des paramètres :
param = listeParametres[i] >> parametres des boissons de type i+1
param = [idTypeBoisson, nbOpti, coef1, coef2, coef3]


exemple d'un parametre : l
l = [idTypeBoisson, nbOpti, coef1, coef2, coef3]
nbOpti = nombre de boissons pour lequel le temps de préparation est le plus rentable (3 par déafaut)
'''

def genere_parametres(nb):
    '''
    Génère un jeu de paramètres (pour nb types de boissons différents) artificiels
    '''
    listeParam = []
    np.random.seed(1)
    for i in range(nb):
        l = [i+1]
        nbOpti = np.random.randint(1, 6)
        a = np.random.normal(20, 8)
        while (a > 40) or (a < 13):
            a = np.random.normal(20, 8)
        x = np.random.normal(0.2, 0.15)
        while (x < 0.05) or (x > 0.35):
            x = np.random.normal(0.2, 0.15)
        b = (1-x)*a
        c = 0.3*a + 0.7*b
        l += [nbOpti, a, b, c]
        listeParam.append(l)
        t = time.gmtime()
        s = int(time.mktime(t))
        np.random.seed(s)  
    return listeParam


listeParametres_California = []
#Blue Lagoon
listeParametres_California.append([1, 2, 22, 0.7*22, 0.85*22])
#California Petit
listeParametres_California.append([2, 2, 14, 10, 12])
#California Grand
listeParametres_California.append([3, 2, 26, 23, 25])
#Pinte
listeParametres_California.append([4, 5, 13, 12, 12])
#Pichet
listeParametres_California.append([5, 2, 40, 38, 38])



# bar Beho
listeParametresBeho = []
# Apple pie
listeParametresBeho.append([1, 4, 30, 23, 26])
# Brazil
listeParametresBeho.append([2, 2, 45, 25, 28])
# Cuba libre



## Création des commandes sur une soirée ("soiree")

# Distribution (gaussienne) des instants d'arrivée des commandes
sigma_arrivees = gp.fin_soiree / 4
distrib_gaussian = np.random.normal(gp.fin_soiree/2, sigma_arrivees, int(gp.nb_commandes_soiree*2/3))
distrib_uniform = np.random.uniform(gp.debut_soiree, gp.fin_soiree, int(gp.nb_commandes_soiree/3))
distrib_arrivees = np.concatenate((distrib_gaussian, distrib_uniform))
for i in range(gp.nb_commandes_soiree):
    while (distrib_arrivees[i] < 0) or (distrib_arrivees[i] > gp.fin_soiree):
        distrib_arrivees[i] = np.random.normal(gp.fin_soiree/2, sigma_arrivees)
distrib_arrivees = np.sort(distrib_arrivees)

# liste des commandes de la soirée
liste_commandes_soiree = []
for i in range(gp.nb_commandes_soiree):
    temps = distrib_arrivees[i]
    c = commande(i, temps)
    nb_boissons = tire_nb_boissons(gp.mu_distrib_b, gp.sigma_distrib_b)
    for j in range(nb_boissons):
        b = boisson(np.random.randint(1, gp.N_boissons+1))
        c.ajouteBoisson(b)
    liste_commandes_soiree.append(c)
    
t = time.gmtime()
s = int(time.mktime(t))
np.random.seed(s)    