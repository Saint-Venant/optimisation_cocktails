from StructuresProduction import *
import GenerationDonnees as gend
import OutilsGraphiques as outg
import matplotlib.pyplot as plt
import numpy as np


## Controle des affichages graphiques

plot_param = False
plot_fonction_prod = False
plot_all_param = False
plot_attente_boisson = False
plot_attente_commande = False
plot_preparation_parallele = False
plot_taille_commandes = False

aff_com = False
aff_param = False
aff_plan_basique = False
aff_plan_opti = False


## création des commandes

listeCommandes = gend.listeCommandes_statique

if aff_com:
    #affichage des commandes crées
    outg.affiche_commandes(listeCommandes)

## génération des paramètres du temps de préparation

listeParametres = gend.listeParametres_California

if aff_param:
    #affichage des paramètres
    outg.affiche_parametres(listeParametres)

## test de paramètres

if plot_param:
    #tracé de la représentation graphique de la fonction de production
    plt.figure(1)
    plt.title('Allure de la fonction de temps de production \n nbOpti=3')
    
    #  allure basique, pour différents paramètres mais avec nbOpti=3
    for i in range(0, gp.N_boissons):
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
    plt.xlabel("nombre de boissons")
    plt.ylabel("temps de production")
    plt.show()


if plot_fonction_prod:
    #test de la fonction de production
    plt.figure(2)
    plt.title('Test de la fonction de production')
    plt.xlabel("nombre de boissons")
    plt.ylabel("temps de production")
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
        plt.plot(x, y, label=gp.noms_boissons[param[0]-1])
    plt.legend()
    plt.show()

## Plan de production basique (pas d'optimisation)

plan = planProduction("buffer")
for com in listeCommandes:
    plan.ajouteCommande(com)

#affiche le plan de production basique
if aff_plan_basique:
    print()
    print("Plan de production basique")
    plan.affichePlan()
    print()


calculeProduction(plan, listeParametres)


#temps d'attente par commande
attenteComBasique = outg.attente_commandes(listeCommandes)

#instant de fin de production
finProduction = plan.clusters[-1][0].fin

#distribution des temps d'attente de chaque boisson = instantLivraison - instantFinPreparation
fraicheurBasique = outg.attente_boissons(listeCommandes)

#nombre de commandes préparées en parallèle
preparationsParallelesBasique = nbTachesParalleles(plan)


## Plan de production optimisé au max, sans contrainte

planUltraOpti = planProduction("buffer")
for com in listeCommandes:
    planUltraOpti.ajouteCommandeUltraOpti(com)

#affichage du plan optimisé sans contrainte
if aff_plan_opti:
    print()
    print("Plan de production optimisé sans contrainte")
    planUltraOpti.affichePlan()
    print()

calculeProduction(planUltraOpti, listeParametres)

#temps d'attente par commande
attenteComUltraOpti = outg.attente_commandes(listeCommandes)


#instant de fin de production
finProductionUltraOpti = planUltraOpti.clusters[-1][0].fin

#distribution des temps d'attente de chaque boisson = instantLivraison - instantFinPreparation
fraicheurUltraOpti = outg.attente_boissons(listeCommandes)

#nombre de commandes préparées en parallèle
preparationsParallelesUltraOpti = nbTachesParalleles(planUltraOpti)

## Bilan des deux méthodes

if plot_attente_boisson:
    #temps d'attente boisson, avant livraison
    plt.figure(4)
    vect_attentes = [fraicheurBasique, fraicheurUltraOpti]
    vect_titres = ["sans optimisation", "optimisation sans contrainte"]
    outg.plot_attente_boissons(vect_attentes, vect_titres, 20)
    plt.show()

if plot_attente_commande:
    #temps d'attente client, par commande
    plt.figure(5)
    vect_attentes = [attenteComBasique, attenteComUltraOpti]
    vect_labels = ["sans optimisation", "optimisation sans contrainte"]
    outg.plot_attente_commandes(vect_attentes, vect_labels)
    plt.show()


#temps total de production
print()
print("temps total de production :")
print("méthode basique --> ", outg.arrondi(finProduction, 2))
print("méthode optimisée sans contrainte -->", outg.arrondi(finProductionUltraOpti, 2))


if plot_preparation_parallele:
    #nombre de commandes préparées en parallèle
    plt.figure(6)
    vect_prep = [preparationsParallelesBasique, preparationsParallelesUltraOpti]
    vect_labels = ["sans optimisation", "optimisation sans contrainte"]
    outg.plot_preparation_parallele(vect_prep, vect_labels)
    plt.show()


if plot_taille_commandes:
    #taille des commandes passées
    plt.figure(7)
    outg.plot_taille_commandes(listeCommandes, gp.A_max+2)
    plt.show()