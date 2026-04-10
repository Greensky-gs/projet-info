from _headers.constants import *

def detection_deplacements(grille, joueur):
    """
    Détecte tous les déplacements possibles pour un joueur donné
    
    Entrée : grille, joueur
        grille : le plateau
        joueur : le joueur en question (1 = Blanc, 2 = Noir)
    Sortie : List[(int, int)] - la liste de tous les pions pouvant se déplacer
    """
    pass

def detection_deplacements_pions(grille, position):
    """
    Détecte toutes les positions possibles de déplacement pour un pion

    Entrée : grille, position
        grille   : le plateau
        position : Tuple(int, int) - la position (x;y) du pion
    Sortie : List[(int, int)] - la liste de toutes les cases possibles dans le plateau pour ce pion
    """
    alentours = [(position[0] + 1, position[1] + 1), (position[0] + 1, position[1] - 1), (position[0] - 1, position[1] + 1), (position[0] - 1, position[1] + 1)] # Toutes les cases autour de la position donnée


