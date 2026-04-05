def case_grille(grille, x, y):
    """
    Obtient la valeur de la case (x;y) de la grille grille

    Entrée : grille, x, y
        grille : La grille
        x      : la position x de la case à obtenir
        y      : la position y de la case à obtenir
    Sortie : entier - None si la case n'existe pas, 0 si elle est vide, 1 ou 2 dépendamment du joueur qui y est
    """
    from structs.grille.helpers import est_dans_grille # Avoid circular imports

    if not est_dans_grille(grille, x, y):
        return None
    return grille[x][y]

def set_case(grille, x, y, val):
    """
    Change la valeur de la case (x;y) de la grille grille pour val

    Entrée : grille, x, y, val
        grille : La grille
        x      : la position x de la case à modifier
        y      : la position y de la case à modifier
    Sortie : booléen - Si la case a été modifiée
    """
    from structs.grille.helpers import est_dans_grille # Avoid circular imports

    if not est_dans_grille(grille, x, y):
        return False
    if not val in [0, 1, 2]:
        return False

    grille[x][y] = val
    return True

