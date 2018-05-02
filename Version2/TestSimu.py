from SimuSoiree import *
import GenerationDonnees2 as gen2


# plan basique
#planBasique, rush_soiree_Basique = simuleSoiree(outs.liste_commandes_soiree, gen2.listeParametres, outs.debut_soiree, 600, opti=False)
#Y_attenteOpti, attenteMoyOpti = calc_attenteCommande(outs.liste_commandes_soiree)

# plan opti
planOpti, rush_soiree_Opti = simuleSoiree(outs.liste_commandes_soiree, gen2.listeParametres, outs.debut_soiree, 600, opti=True)
Y_attenteOpti, attenteMoyOpti = calc_attenteCommande(outs.liste_commandes_soiree)



#planning de production
plt.figure(1)
indexCouleurs = {}
for com in outs.liste_commandes_soiree:
    c = np.random.rand(3,)
    indexCouleurs[com] = c
for cl in planOpti.histoire:
    b1 = cl[0]
    b2 = cl[-1]
    plt.axvline(x=b1.debut, c='k', linestyle='--')
    plt.axvline(x=b2.fin, c='k', linestyle='--')
    for b in cl:
        num = b.commande.num
        plt.plot([b1.debut, b2.fin], [num, num], color=indexCouleurs[b.commande], linewidth=10)
fin = planOpti.histoire[-1][0].fin
plt.axis([outs.debut_soiree, fin, -1, len(outs.liste_commandes_soiree)])
plt.title("Planning de production des commandes : plan opti")
plt.xlabel("temps")
plt.ylabel("indice de commande")
plt.show()


#temps d'attente par commande
plt.figure(2)
plt.plot(Y_attenteOpti, 'bo', label="plan basique")
plt.plot(outs.nb_commandes_soiree*[attenteMoyOpti], 'k-', label="temps d'attente moyen")
plt.plot(outs.nb_commandes_soiree*[1.1*attenteMoyOpti], 'k--', label="temps d'attente moyen + 10%")
xmin = 0
xmax = len(Y_attenteOpti)-1
ymin = 0
ymax = max(Y_attenteOpti) + 50
plt.axis([xmin, xmax, ymin, ymax])
plt.xlabel("commandes")
plt.ylabel("temps d'attente")
plt.title("Temps d'attente par commande")
plt.legend()
plt.show()


# nombre de commandes gérées en même temps
plt.figure(3)
plt.plot(rush_soiree_Opti, c='b', label='plan basique')
plt.title("Nombre de commandes en attentes")
plt.xlabel("temps")
plt.ylabel("nombre de commandes")
plt.legend()
plt.show()