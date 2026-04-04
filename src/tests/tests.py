from headers.constants import *
from aux.test_function import *
from structs.tour.interface import *
from structs.grille.helpers import *
from structs.grille.interface import *
from aux.tools import *
from aux.utils import *

def test_inverser_tour():
    tour = 1

    tour = inverser_tour(tour);
    assert tour == 2, "Inverser tour 1"

    tour = inverser_tour(tour);
    assert tour == 1, "Inverser tour 2"

    tour = inverser_tour(tour)
    assert tour == 2, "Inverser tour 3"

    tour = inverser_tour(tour)
    assert tour == 1, "Inverser tour 4"

def test_est_dans_grille():
    grille = [ [ 0 for y in range(N) ] for x in range(N) ]
    jeu = [
        (True, [grille, 0, 0]),
        (True, [grille, 0, N - 1]),
        (True, [grille, N - 1, 0]),
        (True, [grille, N - 1, N - 1]),
        (True, [grille, N // 2, N // 3]),
        (False, [grille, N, N + 2]),
        (False, [grille, N * 2, N + 5])
    ]

    assert tester_fonction_avec_jeu(est_dans_grille, jeu, False), "Vérification est_dans_grille"

def test_case_grille():
    grillebis = [
        [ 0 for y in range(N) ] for x in range(N)
    ]

    grillebis[N - 2][N - 1] = 2
    grillebis[0][0] = 1
    grillebis[N // 2][N // 2] = 0

    jeu = [
        (None, [grillebis, N + 1, 0]),
        (None, [grillebis, 2 * N, N]),
        (0, [grillebis, N // 2, N // 2]),
        (2, [grillebis, N - 2, N - 1]),
        (1, [grillebis, 0, 0])
    ]

    assert tester_fonction_avec_jeu(case_grille, jeu, False), "Vérificaiton case_grille"

def test_set_case():
    grillebis = [
        [ 0 for y in range(N) ] for x in range(N)
    ]

    jeu = [
        (True, [grillebis, 0, 0, 0]),
        (True, [grillebis, N - 1, N - 2, 1]),
        (True, [grillebis, N - 2, N - 1, 2]),
        (False, [grillebis, 0, 0, 5]),
        (False, [grillebis, 0, 0, -2]),
        (False, [grillebis, N, N + 2, 0]),
        (False, [grillebis, N, N, -2])
    ]

    assert tester_fonction_avec_jeu(set_case, jeu, False), "Vérification set_case"
    assert grillebis[0][0] == 0
    assert grillebis[N - 1][N - 2] == 1
    assert grillebis[N - 2][N - 1] == 2

def test_est_au_bon_format():
    """
    Rappel : la fonction est_au_bon format vérifie uniquement si la saisie est composée d'une lettre (majuscule ou minuscule) puis d'une suite de chiffres
    """
    jeu = [
        (True, ["A1"]),
        (True, ["a2"]),
        (True, ["a901"]),
        (True, ["B2"]),
        (False, ["O"]),
        (True, ["O22"]),
        (False, ["aA"]),
        (False, ["8"]),
        (False, ["63"]),
        (False, ["4b"]),
        (False, ["1H"]),
        (False, ["3141592653589"]),
        (True, ["a314159265358979323846264338327950"])
    ]

    assert tester_fonction_avec_jeu(est_au_bon_format, jeu, False), "Vérification est_au_bon_format"
def test_extraire_coordonnees():
    jeu = [
        ((0, 0), ["A1"]),
        ((1, 1), ["B2"]),
        ((2, 9), ["C10"]),
        ((25, 1024), ["Z1025"]),
        ((10, 0), ["K1"]),
        ((0, 0), ["a1"]),
        ((1, 1), ["b2"]),
        ((2, 9), ["c10"]),
        ((25, 1024), ["z1025"]),
        ((10, 0), ["k1"]),
   ]

    assert tester_fonction_avec_jeu(extraire_coordonnees, jeu, False), "Vérification extraire_coordonnées"

def run_tests():
    test_inverser_tour()
    test_est_dans_grille()
    test_case_grille()
    test_set_case()
    test_est_au_bon_format()
    test_extraire_coordonnees()
