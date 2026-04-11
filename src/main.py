from _headers._header import *
from _headers.constants import *
from structs.grille.helpers import *
from structs.user.interface import *
from aux.utils import *
from tests.tests import *

if __name__ == "__main__": # Condition permettant d'être excuté seulement en ligne de commande et pas en importation depuis un autre fichier
    executer_tests()

    grille_depart = [ [ valeur_case_depart(x, y) for y in range(N) ] for x in range(N) ]
    grille_fin = [ [ 0 for _ in range(N) ] for _ in range(N) ]
    grille_fin[0][1] = 1

    grille_milieu = [ [ 0 for _ in range(N) ] for _ in range(N) ]
    for a, b in [ (0, 5), (0, 7), (1, 6), (1, 4), (2, 1), (2, 7), (3, 6) ]:
        set_case(grille_milieu, a, b, 2)
    for a, b in [ (4, 7), (5, 0), (5, 2), (5, 4), (6, 1), (6, 3), (6, 7), (7, 0) ]:
        set_case(grille_milieu, a, b, 1)
    

    tour = 1

    afficher_grille(grille_depart, tour)
    afficher_grille(grille_milieu, tour)
    afficher_grille(grille_fin, tour)

    modif = saisir_coordonnees(grille_milieu, tour)

    if modif is not None:
        set_case(grille_depart, modif[0], modif[1], 2) # Pour voir les modifications

    afficher_grille(grille_milieu, tour)
