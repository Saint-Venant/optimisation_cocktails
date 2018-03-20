from Version0 import *
import random
import matplotlib.pyplot as plt

#nombre de commandes à optimiser
nbCommandes = 200

## création des commandes
listeCommandes = []
temps = 0
for i in range(0, nbCommandes):
    c = commande(i, temps)
    temps += random.randint(0, 36)
    
    #tire un nombre aléatoire de boissons commandées
    nbBoissonsCommandees = random.randint(1, A_max)
    
    #crée ces boissons, et les affecte à la commande c
    for j in range(0, nbBoissonsCommandees):
        b = boisson(random.randint(1, N_boissons), c, j)
        c.ajouteBoisson(b)
    
    #ajoute la commande à la liste des commandes
    listeCommandes.append(c)

#affichage des commandes crées
for c in listeCommandes:
    print("instant de commande :", c.instantCommande)
    c.afficheBoissons()
    triIntraCommandes(c)
    c.afficheBoissons()
    print()

## génération des paramètres du temps de préparation
listeParametres = []
'''exemple d'un parametre : l
    l = [idTypeBoisson, nbOpti, coef1, coef2, coef3]
    nbOpti = nombre de boissons pour lequel le temps de préparation est le plus rentable (3 par déafaut)
'''
for i in range(0, N_boissons):
    l = []
    l.append(i+1)
    nbOpti = random.randint(1, 5)
    l.append(nbOpti)
    a = 5*(0.5+random.random())/1.5
    l.append(a)
    b = (0.5+random.random())*(1/1.5)*0.6*a
    l.append(b)
    l.append(0.3*a + 0.7*b)
    listeParametres.append(l)
print()
print("liste des paramètres de production")
for param in listeParametres:
    print(param)

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

#tracé de la fonction de production pour l'ensemble du jeu de pramètres
plt.figure(3)
plt.title("Allure des fonctions de production \n pour tous les types de boisson")
for param in listeParametres:
    x = list(range(0, 15))
    y = []
    for q in x:
        y.append(prod(q, param))
    plt.plot(x, y)
plt.show()


## Plan de production basique (pas d'optimisation)

plan = planProduction()
for com in listeCommandes:
    plan.ajouteCommande(com)
print()
print("Plan de production basique")
plan.affichePlan()
calculeProduction(plan, listeCommandes, listeParametres)


#tracé des temps d'attente par commande
X_commandes = []
Y_tempsAttente = []
for i in range(0, nbCommandes):
    X_commandes.append(i+1)
    Y_tempsAttente.append(listeCommandes[i].livraison - listeCommandes[i].instantCommande)

#instant de fin de production
finProduction = plan.clusters[-1][0].fin

#distribution des temps d'attente de chaque boisson = instantLivraison - instantFinPreparation
fraicheurBasique = []
for com in listeCommandes:
    for b in com.listeBoissons:
        fraicheurBasique.append(b.livraison - b.fin)

## Plan de production optimisé au max, sans contrainte

planUltraOpti = planProduction()
for com in listeCommandes:
    planUltraOpti.ajouteCommandeUltraOpti(com)
print()
print("Plan de production optimisé sans contrainte")
planUltraOpti.affichePlan()
calculeProduction(planUltraOpti, listeCommandes, listeParametres)

#tracé des temps d'attente par commande
Y_tempsAttenteUltraOpti = []
for i in range(0, nbCommandes):
    Y_tempsAttenteUltraOpti.append(listeCommandes[i].livraison - listeCommandes[i].instantCommande)


#instant de fin de production
finProductionUltraOpti = plan.clusters[-1][0].fin

#distribution des temps d'attente de chaque boisson = instantLivraison - instantFinPreparation
fraicheurUltraOpti = []
for com in listeCommandes:
    for b in com.listeBoissons:
        fraicheurUltraOpti.append(b.livraison - b.fin)

## Bilan des deux méthodes

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