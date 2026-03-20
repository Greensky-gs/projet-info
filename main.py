# -*- coding: utf-8 -*-

"""
Type de données :
    CONSTANTES :
        N : int : le nombre de lignes (= la taille d'un côté) du plateau - C'est une constante.

    VARIABLES :
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
    Ce ne sont pas des variables globales, car elles ne varient pas.
"""

# Constantes

N = 8 # Taille de la grille

# Variables globales

# Fonction de manipulation

## GRILLE

def est_dans_grille(grille, x, y):
    return 0 <= x < N and 0 <= y < N

def afficher_grille(grille, tour):
    """
    Affiche la grille. Prend en entrée une grille.
    Ne renvoie rien

    Peut éventuellement faire planter (intentionellement) le programme si la grille n'est pas valide
    """

    delimitation = lambda start, mid, sep, end: start + (mid + sep) * (N - 1) + mid + end # Fonction auxiliaire qui permet d'obtenir le séparateur
    
    print(" " * 5, end="");
    for i in range(N):
        print(f" {str(i + 1): <2} ", end="")
    print("")

    print(" " * 4 + delimitation("╔", 3 * "═", "╦", "╗"))
    for x in range(N):
        print(f"  {chr(x + 65)} ", end="")
        for y in range(N):
            case = case_grille(grille, x, y)
            if case == None:
                raise(AssertionError())
 
            print("║ ", end="")
            if case == 0:
                print("  ", end="")
            elif case == 1:
                print("● ", end="")
            else:
                print("○ ", end="");
        print("║", end="")

        if x == 0 and tour == 2:
            print("  <--", end="")
        if x == N - 1 and tour == 1:
            print("  <--", end="")

        print("")
        
        if x != N - 1:
            print(" " * 4 + delimitation("╠", 3 * "═", "╬", "╣"));

    print(" " * 4 + delimitation("╚", 3 * "═", "╩", "╝"))

## EOf GRILLE

# EOf fonction de manipulation
# Fonctions d'interface

## Fonctions d'interface du tour

def inverser_tour(tour):
    return (tour % 2) + 1

## EOf Fonctions d'interface du tour
## Fonctions d'interface de la grille

def case_grille(grille, x, y):
    if not est_dans_grille(grille, x, y):
        return None
    return grille[x][y]
def set_case(grille, x, y, val):
    if not est_dans_grille(grille, x, y):
        return False
    if not val in [0, 1, 2]:
        return False

    grille[x][y] = val
    return True


## EOf fonctions d'interface de la grille
## fonctions d'interface utilisateur

def saisir_coordonnees(grille, tour):
    """
    Entrée : tour (int) : Le tour actuel, permet de s'addresser directement au joueur (Blanc pour 1 et Noir pour 2)
    Sortie : (x, y) : un couple de coordonnées valides, dans la grille
    """

    entree_valide = False
    entree = None

    while not entree_valide:
        res = input(f"\x1b[33m{'Noir' if tour == 2 else 'Blanc'}\x1b[0m : veuillez entrer votre une coordonnée (ex: A1): ")

        if not est_au_bon_format(res):
            print("Votre entrée n'est pas au bon format, veuillez réessayer.")
            continue

        entree = extraire_coordonnees(res)
        entree_valide = est_dans_grille(grille, entree[0], entree[1])

        if not entree_valide:
            print(f"Vos coordonnées \x1b[90m({entree[0]};{entree[1]})\x1b[0m ne sont pas dans la grille")
            continue;

    return entree

## EOf fonctions d'interface utilisateur

# EOf fonction d'interfaces


# Fonctions utilitaires

def est_au_bon_format(message):
    """
    Entrée : string : une chaine de caractères contenant une case, en théorie.
    Sortie : bool : si oui ou non le message contient une case valide. La sortie vaut True si le code peut lire une entrée AU BON FORMAT, pas avec les BONNE VALEURS. Autrement dit, si la saisie dépasse la grille, la fonction renverra quand même True
    """

    if len(message) < 2:
        return False

    lettre = message[0]
    suite = message[1:]

    if not ((ord("a") <= ord(lettre) <= ord("z") or (ord("A") <= ord(lettre) <= ord("Z")))):
        return False
    
    # Il faut parcourir la suite du message, car il se peut que le nombre fasse plus de 2 chiffres
    i = 0
    while (i < len(suite)):
        # Le premier chiffre ne peut pas être 0 (ce sera un chiffre invalide)
        if i == 0 and not (ord("1") <= ord(suite[i]) <= ord("9")):
            return False

        if not (ord("0") <= ord(suite[i]) <= ord("9")):
            return False
        i+=1
    return True
def extraire_coordonnees(message):
    """
    Entrée : string : une chaine de caractères contenant une case au bon format (Une exception sera levée si ce n'est pas le cas)
    Sortie : (int, int) : les coordonnées (x;y), avec X correspondant à la ligne (correspondant à la lattre saisie), en format PROGRAMME (commençant à 9) et y correspondant à la colone lue (correspondant au chiffre), au format PROGRAMME
    """
    assert est_au_bon_format(message)

    x = ord(message[0])
    if ord("a") <= x <= ord("z"):
        x = x - ord("a") # 0 si x = "a", 1 si x = "b", ...
    else:
        x = x - ord("A") # 0 si x = "A", 1 si x = "B" ...

    # Construction de y par la saisie
    y = 0
    i = 1
    while i < len(message):
        y = y * 10 + (ord(message[i]) - ord("0"))
        i += 1
    return (x, y - 1)

# EOf fonctions utilitaires

# Fonction "outils"

"""
Les fonctions outils sont des petites fonctions, qui permettent de simplifier une expression (exemple: une grande condition, qui ne tiendrait pas sur une ligne de if, donc elle est factorisé en une petite fonction ici

Ces fonctions, généralement 4 lignes, ne seront pas testées
"""

def valeur_case_depart(x, y):
    if (x + y) % 2 != 1:
        return 0
    if x >= 3 and x < 5:
        return 0
    if x < 3:
        return 2
    return 1

# EOf fonction "outils"


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

    print(f"Test de la fonction \x1b[33m{fonction.__name__}\x1b[0m...")

    n = len(jeu)

    display = lambda v: str(v)[:5] + "..." + str(v)[-5:] if len(str(v)) > 10 else str(v)
    displaylist = lambda l: ", ".join(list(map(display, l)))

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

        print(f"\x1b[35m[{tests}/{n}]\x1b[0m \x1b[33m{fonction.__name__}(\x1b[36m{displaylist(params)}\x1b[33m) = \x1b[36m{result}\x1b[34m, attendu : \x1b[36m{attendu}\x1b[35m | ", end = " ")

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
    tour = 1

    tour = inverser_tour(tour);
    assert tour == 2, "Inverser tour 1"

    tour = inverser_tour(tour);
    assert tour == 1, "Inverser tour 2"

    tour = inverser_tour(tour)
    assert tour == 2, "Inverser tour 3"

    tour = inverser_tour(tour)
    assert tour == 1, "Inverser tour 4"

## EOf vérification tour
## Vérification  grille

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
    
## EOf vérification grille
## Vérification saisie

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

## EOf vérification saisie
## Appels vérifications

# Ces lignes peuvent être commentées
test_inverser_tour()
test_est_dans_grille()
test_case_grille()
test_set_case()
test_est_au_bon_format()
test_extraire_coordonnees()

# EOf Fonctions de vérification

# Code principal
if __name__ == "__main__":
    grille_depart = [ [ valeur_case_depart(x, y) for y in range(N) ] for x in range(N) ]; # Formule qui fait peur, 
    grille_fin = [ [ 0 for y in range(N) ] for x in range(N) ]
    grille_fin[0][1] = 1

    grille_milieu = [ [ 0 for y in range(N) ] for x in range(N) ]
    # Construction par algorithme :
    for a, b in [ (0, 5), (0, 7), (1, 6), (1, 4), (2, 1), (2, 5), (2, 7), (3, 6) ]:
        set_case(grille_milieu, a, b, 2)
    for a, b in [ (4, 7), (5, 0), (5, 2), (5, 4), (6, 1), (6, 3), (6, 7), (7, 0) ]:
        set_case(grille_milieu, a, b, 1)
    

    tour = 1

    afficher_grille(grille_depart, tour)
    afficher_grille(grille_milieu, tour)
    afficher_grille(grille_fin, tour)

    modif = saisir_coordonnees(grille_depart, tour)

    set_case(grille_depart, modif[0], modif[1], 2) # Pour voir les modifications

    afficher_grille(grille_depart, tour)
