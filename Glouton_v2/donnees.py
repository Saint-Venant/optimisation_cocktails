# Données

type_boisson=['mojito','bière','caïpirinha','sex on the beach','white russian','long island','caipiroska']

def F(n): #fonction de production (donne le temps de production de boissons en fonction du nb de boissons - et de son type- à préparer )
    assert(n>=0)
    a=0.15
    F_1=0.75
    if n==0:
        return 0
    if n==1:
        return F_1
    if n>1:
        return (a*n +F_1-a)

attente_max_acceptee=10