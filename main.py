# -*- coding: utf-8 -*-

"""
Type de données :
    CONSTANTES :
        N : int : le nombre de lignes (= la taille d'un côté) du plateau - C'est une constante.

    VARIABLES GLOBALES :
        grille : list[int] : une liste de taille N*N remplie d'entiers : 0 si la case est vide, 1 si elle est occupée par le premier joueur et 2 par le deuxième
            fonctions d'interface :
                case_grille(grille: list[int], x: int, y: int) -> int : Renvoie la valeur de la case de coordonnées (x;y). Si cette case n'existe pas, None est renvoyé
                set_case(grille: list[int], x: int, y: int, val: int) -> bool : Modifie la case de coordonnées (x;y) de la grille. Si l'opération réussi, True est renvoyé, False sinon (ie. si la case n'existe pas ou que la valeur est impossible)

            Fonctions de manipulation :
                afficher_grille(grille: list[int]) -> None : Affiche la grille à l'écran. Ne renvoie rien
                est_dans_grille(grille: list[int], x: int, y: int) -> bool : Renvoie True si la case de coordonnées (x;y) peut être écrite dans la grille, False sinon

        tour : int : Une variable globale, qui contient 1 ou 2, dépendamment du joueur qui doit jouer. Vaut 1 si c'est au premier joueur, 2 si c'est au deuxième
            Fonction d'interface :
                inverser_tour(tour: int[]) -> None : Change la tour pour l'autre joueur

Remarques :
    Les constantes sont manipulées comme des valeurs fixées en début, il n'y a donc pas de fonctions d'interface pour ces valeurs.
"""

# Constantes

N = 10 # Taille de la grille

# Variables globales

grille = [ [ 0 for y in range(N) ] for x in range(N) ]
tour = 1

# Fonction de manipulation

## GRILLE

def est_dans_grille(grille, x, y):
    return 0 <= x < N and 0 <= y < N

## EOf GRILLE

# EOf fonction de manipulation
# Fonctions d'interface

## Fonctions d'interface du tour

def inverser_tour(tour):
    return (tour % 2) + 1

## EOf Fonctions d'interface du tour
## Fonctions d'interface de la grille

## EOf fonctions d'interface de la grille
# EOf fonction d'interfaces


# Fonctions utilitaires

"""
Pour des raisons de performances, on n'exécutera pas de tests sur les fonctions utilitaires
"""

# EOf fonctions utilitaires

# FONCTION DE VÉRIFICATION

def tester_fonction_avec_jeu(fonction, jeu, interruption_quand_echec = True):
    """
    fonction facultative permettant d'automatiser le test d'une fonction (avec des couleurs parce que c'est la vie)
    Cette fonction ne permet que de vérifier qu'une autre fonction renvoie les résultats attendus sur certaines valeurs de paramètres

    fonction est une fonction
    jeu est une liste de la forme : list[(T, list[...])], avec T le type de retour de la fonction, et list[...] la liste des paramètres, où la premiere valeur est le résultat attendu de la fonction

    Cette fonction renvoie True si la fonction a passé tout ses tests, False sinon
    Quand interruption_quand_echec est mis à True, une erreur est levée avec raise(AssertionError)
    """

    print(f"Test de la fonction \x1b[32m{fonction.__name__}\x1b[0m...")

    n = len(jeu)


    tests = 0
    passes = 0
    for test in jeu:
        attendu = test[0]
        params = test[1]

        result = fonction(*params)
        valid = result == attendu

        tests += 1;
        if valid:
            passes +=1

        print(f"\x1b[35m[{tests}/{n}]\x1b[0m \x1b[32m{fonction.__name__}(\x1b[36m{str(params)}\x1b[32m) = \x1b[33m{result}\x1b[34m, attendu : \x1b[33m{attendu} | ", end = " ")

        if valid:
            print("\x1b[32mvalide\x1b[0m")
        else:
            print("\x1b[31minvalide\x1b[0m")
            if interruption_quand_echec:
                raise(AssertionError("Tests"))

    print(f"La fonction \x1b[33m{fonction.__name__}\x1b[0m a passé \x1b[{31 + (n == passes)}m{passes}\x1b[0m tests sur \x1b[33m{n}\x1b[0m")

    return passes == n

## Vérification inversion tour

def test_inverser_tour():
    global tour # Indiquer à python qu'il faut utiliser cette variable

    tour = inverser_tour(tour);
    assert tour == 2, "Inverser tour 1"

    tour = inverser_tour(tour);
    assert tour == 1, "Inverser tour 2"

    tour = inverser_tour(tour)
    assert tour == 2, "Inverser tour 3"

    tour = inverser_tour(tour)
    assert tour == 1, "Inverser tour 4"

## EOf vérification tour
## Vérification est_dans_grille

def test_est_dans_grille():
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
## EOf vérification est_dans_grille
## Appels vérifications

test_inverser_tour()
test_est_dans_grille()

# EOf Fonctions de vérification
