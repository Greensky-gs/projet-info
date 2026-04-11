from _headers.constants import *
from structs.grille.helpers import *

# Fonction de déplacement
def deplacement_mouvement(grille, originx, originy, targetx, targety, valeur):
    """
    Entrée : grille, originx, originy, targetx, targety, valeur
        grille  : le plateau à modifier
        originx : la position X de la case d'origine
        originy : la position Y de la case d'origine
        targetx : la position X de la case d'origine
        targety : la position Y de la case d'origine
        valeur  : la couleur du joueur à déplacer (non vérifiée pour la case d'origine)

    Sortie : booléen - si le déplacement a pu être effectué
    """
    if not est_dans_grille(grille, originx, originy) or not est_dans_grille(grille, targetx, targety): # Les cases de départs et d'arrivée de ne sont pas dans la grille
        return False
    
    autour_origin = [(originx + 1, originy + 1), (originx + 1, originy - 1), (originx - 1, originy + 1), (originx - 1, originy - 1)]
    if not (targetx, targety) in autour_origin: # La case sélectionnée n'est pas autour de la case de départ
        return False

    if case_grille(grille, targetx, targety) != 0: # On devrait avoir une case vide 
        return False
    
    set_case(grille, originx, originy, 0)
    set_case(grille, targetx, targety, valeur)
    return True

# Fin des fonctions de déplacement
