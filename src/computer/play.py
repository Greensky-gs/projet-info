# Fonctions de jeu de l'ordinateur
from computer.select_move import *
from moves.capture import deplacement_capture
from moves.move import deplacement_mouvement
from suddendeath.detection import appliquer_mort_subite

def jeu_ordinateur(grille, joueur):
    """
    Fait choisir un coup à l'ordinateur, en respectant les règles
    Entrée : grille, joueur, pion_impose
        grille      : la grille de jeu
        joueur      : la couleur que l'ordinateur joue

    Sortie : bool - Si la mort subite a été appliquée
    """

    done = False
    mort_subite = False
    impose = None
    while not done:
        coup = choisir_coup_ordinateur(grille, joueur, impose)
        if coup is None:
            done = True
            continue
        if coup[0] == 0:
            # Un déplacement simple
            deplacement_mouvement(grille, coup[1][0], coup[1][1], coup[2][0], coup[2][1], joueur)
            done = True
            mort_subite = appliquer_mort_subite(grille, joueur)
        elif coup[0] == 1:
            deplacement_capture(grille, coup[1][0], coup[1][1], coup[2][0], coup[2][1], joueur)

            mort_subite = appliquer_mort_subite(grille, joueur)
            if mort_subite:
                done = True
            else:
                impose = (coup[2][0], coup[2][1])
                if len(detection_captures_pions(grille, impose)) == 0:
                    done = True
        else:
            raise NotImplementedError("Ce coup n'existe pas. Si vous voyez ça, le code n'est pas bon")
    return mort_subite

