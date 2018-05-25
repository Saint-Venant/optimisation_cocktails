'''
Contient l'ensemble des paramètres du système
'''


## Données du bar

# Nombre max de boissons par commande
A_max = 10

# Nombre de types de boissons différents
N_boissons = 8
noms_boissons = ["Blue Lagoon", "California Petit", "California Grand", "Pinte", "Pichet"]


## Contraintes

#temps d'attente max d'une boisson préparée avant sa livraison (afin de garantir sa fraicheur)
tempsFraicheur = 200

#coefficient de pénalisation des attentes clients trop longues
penalisationAttente = 0.005


## Données optimisation statique ("buffer")

# nombre de commandes à optimiser
nbCommandes_statique = 12


## Données optimisation dynamique ("soiree")

# Générer une soirée d'arrivée de commandes
nb_commandes_soiree = 3*10*10
#nb_commandes_soiree=30*10

# Instant de début de la soirée
debut_soiree = 0

# Instant de fin de la soiree
#fin_soiree = 20*60 #20 minutes
fin_soiree=60*60*3 #3 heures


## Calibration de la demande

# période d'arrivée des commandes
periodeArrivee = 115

# distribution du nombre de boissons par commande
mu_distrib_b = 3
sigma_distrib_b = 2