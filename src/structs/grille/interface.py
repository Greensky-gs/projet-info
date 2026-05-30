# Fonctions d'interface de la grille


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

def list_coups_grille(grille, joueur, pion_impose = None) -> list[tuple[bool, tuple[int, int], tuple[int, int]]]:
    """
    Renvoie la liste de  tous les coups possibles pour un joueur donné
    Entrée : grille, joueur
        grille       : list[list[int]] - La grille de jeu
        joueur       : PlayerType (int) - Le joueur dont les coups doivent être calculés
        pion_imposoe : tuple[int, int] | None - Le pion que le joueur doit bouger (par exemple pour une chaine de captures)

    Sortie : list[tuple[bool, tuple[int, int], tuple[int, int]]] - La liste de tous les coups possibles. La première valeur correspond à si le coup est une capture ou non, la deuxième est le premier paramètre de déplacement, et le troisième est le deuxième paramètre de déplacement
    """
    from moves.detection import detection_captures_joueur, detection_captures_pions, detection_deplacements_joueur, detection_deplacements_pions

    captures = detection_captures_joueur(grille, joueur) if pion_impose is None else (pion_impose,)
    if len(captures) > 0:
        result = []
        for capture in captures:
            captures_pion = detection_captures_pions(grille, capture)
            for capture_pion in captures_pion:
                result.append((True, capture, capture_pion))
        return result
    else:
        moves = detection_deplacements_joueur(grille, joueur)
        result = []
        for move in moves:
            moves_pion = detection_deplacements_pions(grille, move)
            for move_pion in moves_pion:
                result.append((False, move, move_pion))
        return result


# Fin des fonctions d'interface de la grille
