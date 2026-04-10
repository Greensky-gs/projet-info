from _headers.constants import *
from structs.grille.helpers import *
from structs.grille.interface import *

# FONCTIONS DE DÉTECTION
def detection_pion_deplaceable(grille, position):
    """
    Détecte si un pion donné peut se déplacer (seulement déplacer, pas capturer)

    Entrée : grille, position
        grille   : le plateau
        position : un tuple (int, int) représentant la position (x;y) du pion dans le plateau
    Sortie : booléen - True si le pion a au moins une case valide, False si il n'en a aucune
    """
    alentours = [(position[0] + 1, position[1] + 1), (position[0] + 1, position[1] - 1), (position[0] - 1, position[1] + 1), (position[0] - 1, position[1] + 1)] # Toutes les cases autour de la position donnée

    for case in alentours:
        if est_dans_grille(grille, case[0], case[1]) and case_grille(grille, case[0], case[1]) == 0: # La case existe et est vide
            return True
    return False
    

def detection_deplacements(grille, joueur):
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
    alentours = [(position[0] + 1, position[1] + 1), (position[0] + 1, position[1] - 1), (position[0] - 1, position[1] + 1), (position[0] - 1, position[1] + 1)] # Toutes les cases autour de la position donnée
    
    alentours_valides = [ case for case in alentours if est_dans_grille(grille, case[0], case[1]) ] # Cases valides autours du pion

    alentours_libres = [ case for case in alentours_valides if case_grille(grille, case[0], case[1]) == 0 ] # Cases vides valides autours du pion
    return alentours_libres
