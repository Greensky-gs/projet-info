from _headers.constants import *
from structs.tour.helpers import *
from structs.grille.helpers import *
from structs.grille.interface import *

# FONCTIONS DE DÉTECTION
def positions_alentours(grille, position):
    """
    Renvoie les cases aux alentours d'une position donnée

    Entrée : grille, position
        grille   : la grille
        position : un tuple (int, int) représentant la positio (x;y) de la case
    """

    alentours = [(position[0] + 1, position[1] + 1), (position[0] + 1, position[1] - 1), (position[0] - 1, position[1] + 1), (position[0] - 1, position[1] - 1)] # Toutes les cases autour de la position donnée

    return [ x for x in alentours if est_dans_grille(grille, x[0], x[1]) ]

def detection_pion_deplaceable(grille, position):
    """
    Détecte si un pion donné peut se déplacer (seulement déplacer, pas capturer)

    Entrée : grille, position
        grille   : le plateau
        position : un tuple (int, int) représentant la position (x;y) du pion dans le plateau
    Sortie : booléen - True si le pion a au moins une case valide, False si il n'en a aucune
    """
    alentours = positions_alentours(grille, position)

    for case in alentours:
        if case_grille(grille, case[0], case[1]) == 0: # La case existe et est vide
            return True
    return False

def detection_deplacements_joueur(grille, joueur):
    """
    Détecte tous les déplacements possibles pour un joueur donné
    
    Entrée : grille, joueur
        grille : le plateau
        joueur : le joueur en question (1 = Blanc, 2 = Noir)
    Sortie : List[(int, int)] - la liste de tous les pions pouvant se déplacer
    """
    pions_depleaceables = []

    # Parcours de l'entièreté de la grille
    for x in range(N):
        for y in range(N):
            if case_grille(grille, x, y) == joueur and detection_pion_deplaceable(grille, (x, y)):
                pions_depleaceables.append((x, y))
    return pions_depleaceables

def detection_deplacements_pions(grille, position):
    """
    Détecte toutes les positions possibles de déplacement pour un pion

    Entrée : grille, position
        grille   : le plateau
        position : Tuple(int, int) - la position (x;y) du pion
    Sortie : List[(int, int)] - la liste de toutes les cases possibles dans le plateau pour ce pion
    """
    alentours = positions_alentours(grille, position)

    alentours_libres = [ case for case in alentours if case_grille(grille, case[0], case[1]) == 0 ] # Cases vides valides autours du pion
    return alentours_libres

def detection_captures_pions(grille, position):
    """
    Détecte toutes les captures possibles de captures pour un pion donné

    Entée : grille, position
        grille   : le plateau
        position : Tuple(int, int) - la position (x;y) du pion
    Sortie : List[(int, int)] - La liste de toutes les CASES sur lesquelles le pion peut aller capturer. Le pion donné se déplacera sur le pion suivant en diagonale, et la position donnée dans la liste est le pion adverse
    """
    joueur = case_grille(grille, position[0], position[1])
    adversaire = joueur_adverse(joueur)

    alentours = positions_alentours(grille, position)

    resultat = []
    for casex, casey in alentours:
        coefx = (casex - position[0]) * 2
        coefy = (casey - position[1]) * 2

        targetx = position[0] + coefx;
        targety = position[1] + coefy;

        if case_grille(grille, casex, casey) == adversaire and est_dans_grille(grille, targetx, targety) and case_grille(grille, targetx, targety) == 0: # La aux alentours est un adversaire, la case d'arrivée existe et est libre
            resultat.append((casex, casey))
    return resultat

def detection_pion_captureur(grille, position):
    """
    Détecte si un pion donné peut capturer

    Entée : grille, position
        grille   : le plateau
        position : Tuple(int, int) - la position (x;y) du pion
    Sortie : booléen - True si le pion à la position *position* peut capturer au moins un pion adverse
    """
    joueur = case_grille(grille, position[0], position[1])
    adversaire = joueur_adverse(joueur)

    alentours = positions_alentours(grille, position)

    for casex, casey in alentours:
        coefx = (casex - position[0]) * 2
        coefy = (casey - position[1]) * 2

        targetx = position[0] + coefx;
        targety = position[1] + coefy;

        if case_grille(grille, casex, casey) == adversaire and est_dans_grille(grille, targetx, targety) and case_grille(grille, targetx, targety) == 0: # La aux alentours est un adversaire, la case d'arrivée existe et est libre
            return True
    return False

def detection_captures_joueur(grille, joueur):
    """
    Détecte l'intégralité pions pouvant effectuer au moins une capture pour un joueur donné

    Entrée : grille, joueur
        grille : la grille
        joueur : joueur pour qui les pions doivent être cherchés (1 = Blanc, 2 = Noir)
    Sortie : List[(int, int)] - La liste des positions (x;y) des pions de *joueur* pouvant effectuer au moins une capture
    """

    resultat = []
    for x in range(N):
        for y in range(N):
            if case_grille(grille, x, y) == joueur and detection_pion_captureur(grille, (x, y)):
                resultat.append((x, y))
    return resultat

#FIN FONCTIONS DE DÉTECTION
