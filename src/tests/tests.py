from _headers.constants import *
from aux.test_function import *
from moves.detection import positions_alentours
from structs.tour.interface import *
from structs.grille.helpers import *
from structs.grille.interface import *
from moves.capture import deplacement_capture
from moves.move import deplacement_mouvement
from aux.tools import *
from aux.utils import *
from suddendeath.detection import plus_proche_pion
from structs.heap import *

# Fonctions de tests
def generer_grille_test():
    return [ [ valeur_case_depart(x, y) for y in range(N) ] for x in range(N) ]
def generer_grille_vide():
    return [ [ 0 for _ in range(N) ] for _ in range(N) ]

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

def test_deplacement():
    grille = generer_grille_test()
    grille[3][6] = 1
    jeu = [
        (False, [grille, 7, 0, 6, 1, 1]), # La case est déjà occupée
        (False, [grille, 5, 0, N * 2, 9, 1]), # La case d'arrivée n'existe pas
        (False, [grille, N + 1, 10, 0, 1, 1]), # La case de départ n'existe pas
        (False, [grille, 5, 2, 3, 4, 1]), # La case d'arrivée n'est pas une case imméditament à côté de celle de départ
        (True, [grille, 3, 6, 4, 5, 1]), # Toutes les conditions sont validées
    ]

    assert tester_fonction_avec_jeu(deplacement_mouvement, jeu, False), "Vérification deplacement_mouvement"

def test_capture():
    grille = generer_grille_test()
    grille[3][6] = 1
    grille[0][3] = 1

    tour = 2 # Au tour de Noir

    jeu = [
        (False, [grille, 5, 0, N * 2, 9, tour]), # La case à prendre n'existe pas
        (False, [grille, N + 1, 10, 0, 1, tour]), # La case de départ n'existe pas
        (False, [grille, 5, 2, 3, 4, tour]), # La case de capture n'est pas une case imméditament à côté de celle de départ
        (False, [grille, 1, 4, 0, 3, tour]), # La case d'arrivée n'existe pas
        (False, [grille, 1, 4, 2, 3, tour]), # Le pion à capturer est un pion allié
        (True, [grille, 2, 7, 3, 6, tour]), # Toutes les conditions sont validées
    ]

    assert tester_fonction_avec_jeu(deplacement_capture, jeu, False), "Vérification deplacement_capture"

def test_positions_alentours():
    grille = generer_grille_test()

    mid = N // 2

    jeu = [
        ([(1, 1)], [grille, (0, 0)]), # Angle supérieur gauche
        ([(N - 2, N - 2)], [grille, (N - 1, N - 1)]), # Angle inférieur droit
        ([(mid + 1, mid + 1), (mid + 1, mid - 1), (mid - 1, mid + 1), (mid - 1, mid - 1)], [grille, (mid, mid)]), # Milieu
        ([(2, 1), (0, 1)], [grille, (1, 0)]), # Sur le bord gauche
        ([], [grille, (2 * N + 2, 2 * N + 2)]), # Position inexistante
    ]

    assert tester_fonction_avec_jeu(positions_alentours, jeu, False), "Vérififcation positions_alentours"

def test_plus_proche_pion():
    grille = generer_grille_vide()
    grille_1_pion = generer_grille_vide()
    grille_2_pion = generer_grille_vide()
    grille_3_pion = generer_grille_vide()

    grille_1_pion[0][0] = 1
    grille_2_pion[0][0] = 1
    grille_2_pion[1][1] = 2

    grille_3_pion[0][0] = 1
    grille_3_pion[0][2] = 2
    grille_3_pion[0][4] = 1

    jeu = [
        (None, [grille, (0, 0)]),
        (None, [grille, (N - 1, N - 1)]),
        (None, [grille, (2 * N + 2, 2 * N + 2)]),
        (None, [grille_1_pion, (0, 0)]),
        (None, [grille_1_pion, (1, 1)]),
        (None, [grille_2_pion, (3, 3)]), 
        ((0, 0), [grille_2_pion, (1, 1)]), 
        ((1, 1), [grille_2_pion, (0, 0)]), 
        ((0, 4), [grille_3_pion, (0, 2)]),
        ((0, 2), [grille_3_pion, (0, 0)]),
        ((0, 2), [grille_3_pion, (0, 4)]),
    ]

    assert tester_fonction_avec_jeu(plus_proche_pion, jeu, False), "Vérification plus_proche_pion"

def est_abr_trie(abr, taille):
    i = 0
    while abr[i] is not None:
        index_gauche = 2 * i + 1
        index_droite = 2 * i + 2
        
        if index_gauche < taille:
            fils_gauche = abr[index_gauche]
            if fils_gauche is not None and fils_gauche[0] > abr[i][0]:
                return False
        if index_droite < taille:
            fils_droit = abr[index_droite]
            if fils_droit is not None and fils_droit[0] > abr[i][0]:
                return False
        i += 1
    return True

def test_abr():
    a = abr_creer(4)
    b = abr_creer(4)
    c = abr_creer(4)

    abr_inserer(a, [0, 'abc'])
    abr_inserer(b, [0, 'abc'])
    abr_inserer(b, [1, 'abcd'])
    abr_inserer(b, [-1, 'abcde'])
    abr_inserer(c, [0, 'abc'])
    abr_inserer(c, [-1, 'abcde'])
    abr_inserer(c, [3, 'trois'])

    jeu = [
        ([0, 'abc'], [a]),
        ([1, 'abcd'], [b]),
        ([3, 'trois'], [c])
    ]

    assert tester_fonction_avec_jeu(abr_sommet, jeu, False), "Vérification ABR"

    jeu_tri = [
        (True, [a, 4]),
        (True, [b, 4]),
        (True, [c, 4])
    ]

    assert tester_fonction_avec_jeu(est_abr_trie, jeu_tri, False), "Vérification tri ABR"

    jeu_pop = [
        ([0, 'abc'], [a, 4]),
        ([1, 'abcd'], [b, 4]),
        ([3, 'trois'], [c, 4])
    ]

    assert tester_fonction_avec_jeu(abr_pop, jeu_pop, False), "Vérification suppression ABR"

    jeu_nouveau_sommet = [
        (None, [a]),
        ([0, 'abc'], [b]),
        ([0, 'abc'], [c])
    ]

    assert tester_fonction_avec_jeu(abr_sommet, jeu_nouveau_sommet, False), "Vérification nouveau sommet ABR"

    assert tester_fonction_avec_jeu(est_abr_trie, jeu_tri, False), "Vérification tri ABR après opérations"

def executer_tests():
    test_inverser_tour()
    test_est_dans_grille()
    test_case_grille()
    test_set_case()
    test_est_au_bon_format()
    test_extraire_coordonnees()
    test_deplacement()
    test_capture()
    test_positions_alentours()
    test_plus_proche_pion()
    test_abr()

# Fin des fonctions de tests
