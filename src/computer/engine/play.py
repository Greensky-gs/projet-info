# Fonctions de jeu de l'ordinateur
from moves.detection import *
from moves.capture import deplacement_capture
from moves.move import deplacement_mouvement
from suddendeath.detection import appliquer_mort_subite
from time import sleep
from computer.engine.select_move import choisir_coup_ordinateur_ameliore
from _headers.constants import *

def jeu_ordinateur_ameliore(grille, joueur, nom):
    """
    Fait choisir un coup à l'ordinateur amélioré, en respectant les règles
    Entrée : grille, joueur, pion_impose
        grille       : la grille de jeu
        joueur       : la couleur que l'ordinateur joue
        nom          : Nom de l'ordinateur
        tour         : Le tour actuel (pour l'affichage des coups intermédiaires)
        noms_joueurs : Le tuple des noms des joueurs (premier = nom de Blanc, deuxième = nom de Noir)

    Sortie : bool - Si la mort subite a été appliquée
    """

    done = False
    mort_subite = False
    impose = None
    while not done:
        for x in range(1, 4):
            print(f"\x1b[1m{nom}\x1b[0m réfléchit" + "." * x, end="\r")
            sleep(T / 3);

        coup = choisir_coup_ordinateur_ameliore(grille, joueur, impose)
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
                coefx = coup[2][0] - coup[1][0]
                coefy = coup[2][1] - coup[1][1]

                endx = coup[1][0] + 2 * coefx
                endy = coup[1][1] + 2 * coefy

                impose = (endx, endy)
                if len(detection_captures_pions(grille, impose)) == 0:
                    done = True
        else:
            raise NotImplementedError("Ce coup n'existe pas. Si vous voyez ça, le code n'est pas bon")
    return mort_subite

