from _headers.constants import *
from structs.grille.helpers import *
from aux.tools import *
from structs.grille.interface import *
from structs.tour.helpers import *

# Fonctions relatives à la mort subite
def plus_proche_pion(grille, de):
    """
    Trouve le pion le plus proche du pion "de"

    Entrée :
        grille : La grille
        de     : La position (x;y) du pion à trouver
    Sortie : Tuple[int, int] - La position (x;y) du pion adverse le plus proche si il existe, None sinon
    """
    if not case_grille(grille, de[0], de[1]) in [1, 2]:
        return None

    adverse = joueur_adverse(case_grille(grille, de[0], de[1]))

    distance = -1
    pos = None
    for x in range(N):
        for y in range(N):
            if case_grille(grille, x, y) == adverse:
                dist = (de[0] - x) ** 2 + (de[1] - y) ** 2 # Il faudrait prendre la racine, mais ça ne change rien au calcul, donc on peut l'éviter
                if distance == -1:
                    distance = dist
                    pos = (x, y)
                elif distance >= dist:
                    distance = dist
                    pos = (x, y)
    return pos

def appliquer_mort_subite(grille, tour):
    """
    Applique la mort subite

    Entrée :
        grille : la grille
        tour   : Le tour du joueur à qui on doit vérifier
    Sortie : booléen - Si la mort subite a été appliquée
    """

    row = 0 if tour == 1 else N - 1
    for i in range(N):
        if case_grille(grille, row, i) == tour:
            closest = plus_proche_pion(grille, (row, i))
            if closest is not None:
                set_case(grille, closest[0], closest[1], 0)

            set_case(grille, row, i, 0)
            for x in range(0, N) if tour == 2 else range(N - 1, -1, -1):
                for y in range(N):
                    if case_grille(grille, x, y) == 0 and valeur_case_depart(x, y) != 0:
                        set_case(grille, x, y, tour)
                        return True
    return False



# Fin des fonctions relatives à la mort subite
