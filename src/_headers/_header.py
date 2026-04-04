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

