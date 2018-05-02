from Version2 import *
from GenerationDonnees2 import *
import matplotlib.pyplot as plt
import numpy as np


## affichages graphiques
plot_param = False
plot_fonction_prod = False
plot_all_param = False
plot_attente_boisson = False
plot_attente_commande = True
plot_preparation_parallele = False
plot_taille_commandes = False

aff_com = False
aff_param = False
aff_plan_basique = False
aff_plan_opti = False


## création des commandes

if aff_com:
    #affichage des commandes crées
    for c in listeCommandes:
        print("instant de commande :", c.instantCommande)
        c.afficheBoissons()
        triIntraCommandes(c)
        c.afficheBoissons()
        print()

## génération des paramètres du temps de préparation

if aff_param:
    print()
    print("liste des paramètres de production")
    for param in listeParametres:
        print(param)

## test de paramètres

if plot_param:
    #tracé de la représentation graphique de la fonction de production
    plt.figure(1)
    plt.title('Allure de la fonction de temps de production \n nbOpti=3')
    
    #  allure basique, pour différents paramètres mais avec nbOpti=3
    for i in range(0, N_boissons):
        X = list(range(0,7))
        a1 = listeParametres[i][2]
        a2 = listeParametres[i][3]
        a3 = listeParametres[i][4]
        Y = [0]
        Y.append(a1)
        for i in range(0, 2):
            Y.append(Y[-1] + a2)
        Y.append(Y[-1] + a3)
        for i in range(0, 2):
            Y.append(Y[-1] + a2)
        plt.plot(X, Y)
    plt.show()


if plot_fonction_prod:
    #test de la fonction de production
    plt.figure(2)
    plt.title('Test de la fonction de production')
    x = list(range(0, 30))
    y = []
    paramTest = [-1, 8, 6, 0.2, 2]
    for quantite in x:
        y.append(prod(quantite, paramTest))
    plt.plot(x, y)
    plt.show()

if plot_all_param:
    #tracé de la fonction de production pour l'ensemble du jeu de pramètres
    plt.figure(3)
    plt.title("Allure des fonctions de production \n pour tous les types de boisson")
    for param in listeParametres:
        x = list(range(0, 8))
        y = []
        for q in x:
            y.append(prod(q, param))
        plt.plot(x, y, label=noms_boissons[param[0]-1])
    plt.legend()
    plt.show()

## Plan de production basique (pas d'optimisation)

plan = planProduction("buffer")
for com in listeCommandes:
    plan.ajouteCommande(com)
if aff_plan_basique:
    print()
    print("Plan de production basique")
    plan.affichePlan()
calculeProduction(plan, listeParametres)


#tracé des temps d'attente par commande
X_commandes = []
Y_tempsAttente = []
for i in range(0, len(listeCommandes)):
    X_commandes.append(i+1)
    Y_tempsAttente.append(listeCommandes[i].livraison - listeCommandes[i].instantCommande)

#instant de fin de production
finProduction = plan.clusters[-1][0].fin

#distribution des temps d'attente de chaque boisson = instantLivraison - instantFinPreparation
fraicheurBasique = []
for com in listeCommandes:
    for b in com.listeBoissons:
        fraicheurBasique.append(b.livraison - b.fin)

#nombre de commandes préparées en parallèle
preparationsParallelesBasique = nbTachesParalleles(plan)


## Plan de production optimisé au max, sans contrainte

planUltraOpti = planProduction("buffer")
for com in listeCommandes:
    planUltraOpti.ajouteCommandeUltraOpti(com)
if aff_plan_opti:
    print()
    print("Plan de production optimisé sans contrainte")
    planUltraOpti.affichePlan()
calculeProduction(planUltraOpti, listeParametres)

#tracé des temps d'attente par commande
Y_tempsAttenteUltraOpti = []
for i in range(0, len(listeCommandes)):
    Y_tempsAttenteUltraOpti.append(listeCommandes[i].livraison - listeCommandes[i].instantCommande)


#instant de fin de production
finProductionUltraOpti = plan.clusters[-1][0].fin

#distribution des temps d'attente de chaque boisson = instantLivraison - instantFinPreparation
fraicheurUltraOpti = []
for com in listeCommandes:
    for b in com.listeBoissons:
        fraicheurUltraOpti.append(b.livraison - b.fin)

#nombre de commandes préparées en parallèle
preparationsParallelesUltraOpti = nbTachesParalleles(planUltraOpti)

## Bilan des deux méthodes

if plot_attente_boisson:
    #temps d'attente boisson, avant livraison
    plt.figure(4)
    
    plt.subplot(121)
    plt.title("Distribution des temps d'attente avant livraison \n des boissons : sans optimisation")
    plt.xlabel("temps d'attente")
    plt.ylabel("nombre de boissons")
    plt.hist(fraicheurBasique, 20, facecolor='b')
    
    plt.subplot(122)
    plt.title("Distribution des temps d'attente avant livraison \n des boissons : optimisation sans contrainte")
    plt.xlabel("temps d'attente")
    plt.ylabel("nombre de boissons")
    plt.hist(fraicheurUltraOpti, 20, facecolor='r')
    
    plt.show()

if plot_attente_commande:
    #temps d'attente client, par commande
    plt.figure(5)
    plt.title("Temps d'attente par commande \n en fonction du type de plan de production")
    plt.xlabel('identifiant de commande')
    plt.ylabel("temps d'attente")
    plt.plot(X_commandes, Y_tempsAttente, 'o', label="sans optimisation")
    plt.plot(X_commandes, Y_tempsAttenteUltraOpti, 'ro', label="avec optimisation sans contrainte")
    plt.legend()
    plt.show()


#temps total de production
print()
print("temps total de production :")
print("méthode basique --> ", finProduction)
print("méthode optimisée sans contrainte -->", finProductionUltraOpti)


if plot_preparation_parallele:
    #nombre de commandes préparées en parallèle
    plt.figure(6)
    plt.title("Nombre de commandes préparées en parallèle")
    plt.xlabel("temps")
    plt.ylabel("nombre de commandes différentes en cours de préparation")
    plt.plot(preparationsParallelesBasique, 'b', label="sans optimisation")
    plt.plot(preparationsParallelesUltraOpti, 'r', label="avec optimisation sans contrainte")
    plt.legend()
    plt.axis([0, len(preparationsParallelesBasique), min(preparationsParallelesBasique)-1, max(preparationsParallelesUltraOpti)+1])
    plt.show()


if plot_taille_commandes:
    #taille des commandes passées
    taille = []
    for c in listeCommandes:
        taille.append(len(c.listeBoissons))
    choix_bins = list(range(1, A_max+2))
    plt.figure(7)
    plt.hist(taille, bins=choix_bins)
    plt.xlabel("nombre de boissons")
    plt.ylabel("effectif")
    plt.title("Diistribution du nombre de boissons par commande")
    plt.show()