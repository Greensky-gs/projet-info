from _headers.constants import *
from structs.grille.helpers import *
from structs.tour.helpers import *

def deplacement_capture(grille, originx, originy, targetx, targety, valeur):
    """
    Entrée : grille, originx, originy, targetx, targety, valeur
        grille  : la grille
        originx : la position X d'origine
        originy : la position Y d'origine
        targetx : la position X du pion à capturer
        targety : la position Y du pion à capturer
        valeur  : la valeur du pion qui capture

    Sortie : booléen - si la capture a pu être effectuée
    """
    if not est_dans_grille(grille, originx, originy) or not est_dans_grille(grille, targetx, targety): # Une des positions n'est pas dans la grille
        return False
    
    autour_origin = [(originx + 1, originy + 1), (originx + 1, originy - 1), (originx - 1, originy + 1), (originx - 1, originy - 1)]
    if not (targetx, targety) in autour_origin: # La case sélectionnée n'est pas autour de la case de départ
        return False

    adversaire = joueur_adverse(valeur)
    if case_grille(grille, targetx, targety) != adversaire: # On devrait avoir un pion opposé
        return False

    # Calcul de la case d'arrivée en se basant sur la case de départ et la case du pion capturé
    coefx = targetx - originx
    coefy = targety - originy

    endx = originx + 2 * coefx
    endy = originy + 2 * coefy

    if not est_dans_grille(grille, endx, endy): # La case existe
        return False

    if case_grille(grille, endx, endy) != 0: # La case devrait être vide
        return False

    set_case(grille, endx, endy, valeur)
    set_case(grille, originx, originy, 0)
    set_case(grille, targetx, targety, 0)
    return True
