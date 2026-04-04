def case_grille(grille, x, y):
    from structs.grille.helpers import est_dans_grille # Avoid circular imports

    if not est_dans_grille(grille, x, y):
        return None
    return grille[x][y]

def set_case(grille, x, y, val):
    from structs.grille.helpers import est_dans_grille # Avoid circular imports

    if not est_dans_grille(grille, x, y):
        return False
    if not val in [0, 1, 2]:
        return False

    grille[x][y] = val
    return True

