import sys
from _headers.constants import *
from moves.detection import *
from moves.capture import *
from moves.move import deplacement_mouvement
from structs.tour.interface import *
from suddendeath.detection import appliquer_mort_subite
from structs.heap import *
# Fonction de sélection de coup pour l'ordinateur

def score_position(grille, joueur):
    """
    Donne un score à une position donnée
    Entrée: grille, joueur
        grille : La position
        joueur : Le joueur qui représente l'ordinateur

    Sortie: int - entier représentant le score de la position. Une valeur négative est une position désavantageuse pour l'ordinateur
    """
    # Coefficients, on les mets dans un dictionnaire, mais on pourrait très bien les mettre dans des variables classique, je préfère cette notation car plus lisible
    coeffs = {
        "materiel": 0.6,
        "ouvertures": -1.2,
        "captures": 1 # On privilégie la défense plutôt que l'attaque
    }

    # Analyse simplement matérielle
    pions_ordinateur = 0
    pions_adversaire = 0
    ouvertures = 0
    attaques = 0
    couleur_adversaire = joueur_adverse(joueur)

    for x in range(N):
        for y in range(N):
            # Pour des questions d'optimisation, on évite les caluls inutiles (ex: vérification de coordonnées)
            if grille[x][y] == couleur_adversaire:
                pions_adversaire += 1

                ouvertures += len(detection_captures_pions(grille, (x, y)))
            elif grille[x][y] == joueur:
                pions_ordinateur += 1

                attaques += len(detection_captures_pions(grille, (x, y)))

    return (pions_ordinateur - pions_adversaire) * coeffs["materiel"] + attaques * coeffs["captures"] + ouvertures * coeffs["ouvertures"]

def alpha_beta_pruning(
        grille: tuple[list[list[int]], None | tuple[bool, tuple[int, int], tuple[int, int]], tuple[None | tuple[int, int], None | tuple[int, int]]],
        couleur_bot,
        profondeur = 1,
        alpha = -sys.maxsize - 1,
        beta = sys.maxsize,
        est_bot = True,
        top = True
) -> tuple[int, list[list[int]], None | tuple[bool, tuple[int, int], tuple[int, int]], tuple[None | tuple[int, int], None | tuple[int, int]]]:
    """
    Fonction de recherche algorithmique du meilleur coup à partir d'une position donnée

    Utilise l'algorithme d'Élagage Alpha-Beta, qui consiste à éliminer les branches qui sont "déjà mauvaises" ou "déjà bonnes", pour ne pas avoir à calculer des positions redondantes, ou inutiles, et obtenir un temps de calcul raisonnable.
    PS: Lors du premier coup, cet algorithme est très lent (~27 secondes), mais tourne autour de 5 secondes par la suite, pour une raison inconnue

    Entrée : grille, couleur_bot, profondeur, alpha, beta, est_bot, top
        grille      : Un tuple contenant : 1. La grille de jeu à rechercher 2. un tuple contenant le dernier coup joué (si capture, origine, destination) ou None 3. Un tuple représentant les derniers coups joués par, respectivement le joueur et le robot, afin de reprendre le calcul en cas de chaine de captures
        couleur_bot : int - La couleur qui représente le robot
        profondeur  : int - Le nombre d'itérations de l'algorithme à effectuer. Par défaut : 1
        alpha       : int - Le score du meilleur coup trouvé jusqu'à présent. Par défaut : taille minimale des entiers signés en python
        beta        : int - Le score du pire coup trouvé jusqu'à présent. Par défaut : taille maximale des entiers signés en python
        est_bot     : bool - Si l'évaluation en cours évalue le robot ou le joueur
        top         : bool - Paramètre servant à déterminer si il faut renvoyer le coup actuel ou le coup passé en paramètre (pour renvoyer le coup correct en sortie)

    Sortie : Un tuple contenant : 1. Le score trouvé 2. La grille correspondante 3. Le coup (si capture, origine, destination) 4. Les Un tuple représentant les derniers coups joués par, respectivement le joueur et le robot
    """
    if profondeur == 0 or est_partie_finie(grille[0], couleur_bot)[0]:
        return (
            score_position(grille[0], couleur_bot),
            grille[0],
            grille[1],
            grille[2]
        )

    if beta <= alpha:
        return (beta, grille[0], grille[1], grille[2])

    if est_bot is True:
        meilleur: tuple[int, list[list[int]], None | tuple[bool, tuple[int, int], tuple[int, int]], tuple[None | tuple[int, int], None | tuple[int, int]]] = (-sys.maxsize - 1, [ row[:] for row in grille[0] ], None, (None, None)) 
        pion_impose = grille[2][1]

        coups = list_coups_grille(grille[0], couleur_bot, pion_impose)
        for coup in coups:
            clone = [ row[:] for row in grille[0] ]

            if coup[0] is True:
                deplacement_capture(clone, coup[1][0], coup[1][1], coup[2][0], coup[2][1], couleur_bot)
            else:
                deplacement_mouvement(clone, coup[1][0], coup[1][1], coup[2][0], coup[2][1], couleur_bot)
            mort_subite = appliquer_mort_subite(clone, couleur_bot)

            coefx = coup[2][0] - coup[1][0]
            coefy = coup[2][1] - coup[1][1]

            endx = coup[1][0] + 2 * coefx
            endy = coup[1][1] + 2 * coefy

            val = alpha_beta_pruning(
                (clone, coup, (
                    grille[2][1],
                    None if not coup[0] or mort_subite else (endx, endy)
                )),
                couleur_bot,
                profondeur - 1,
                alpha,
                beta,
                False,
                False
            )
            
            if val[0] >= meilleur[0]:
                meilleur = (
                    val[0],
                    [ row[:] for row in val[1] ],
                    grille[1] if not top else coup,
                    (
                        grille[2][1],
                        None if not coup[0] or mort_subite else (endx, endy)
                    )
                )
                alpha = max(alpha, val[0])
                if alpha >= beta:
                    break
    else:
        meilleur: tuple[int, list[list[int]], None | tuple[bool, tuple[int, int], tuple[int, int]], tuple[None | tuple[int, int], None | tuple[int, int]]] = (sys.maxsize, [ row[:] for row in grille[0] ], None, (None, None))
        pion_impose = grille[2][0]

        coups = list_coups_grille(grille[0], joueur_adverse(couleur_bot), pion_impose)
        for coup in coups:
            clone = [ row[:] for row in grille[0] ]

            if coup[0] is True:
                deplacement_capture(clone, coup[1][0], coup[1][1], coup[2][0], coup[2][1], couleur_bot)
            else:
                deplacement_mouvement(clone, coup[1][0], coup[1][1], coup[2][0], coup[2][1], couleur_bot)
            mort_subite = appliquer_mort_subite(clone, couleur_bot)

            coefx = coup[2][0] - coup[1][0]
            coefy = coup[2][1] - coup[1][1]

            endx = coup[1][0] + 2 * coefx
            endy = coup[1][1] + 2 * coefy

            val = alpha_beta_pruning(
                (clone, coup, (
                    None if not coup[0] or mort_subite else (endx, endy),
                    grille[2][1]
                )),
                couleur_bot,
                profondeur - 1,
                alpha,
                beta,
                True,
                False
            )
            
            if val[0] <= meilleur[0]:
                meilleur = (
                    val[0],
                    [ row[:] for row in val[1] ],
                    grille[1] if not top else coup,
                    (
                        grille[2][1],
                        None if not coup[0] or mort_subite else (endx, endy)
                    )
                )
                beta = min(beta, val[0])
                if beta <= alpha:
                    break

    return (
        meilleur[0],
        [ row[:] for row in meilleur[1] ],
        meilleur[2],
        meilleur[3]
    ) 

def choisir_coup_ordinateur_ameliore(grille, joueur, pion_impose = None) -> tuple[int, tuple[int, int], tuple[int, int]] | None:
    """
    Fait choisir un coup à l'ordinateur, en respectant les règles
    Entrée : grille, joueur, pion_impose
        grille      : la grille de jeu
        joueur      : la couleur que l'ordinateur joue
        pion_impose : Le pion que l'ordinateur est obligé de jouer dans le cas où il doit effectuer des prises successives. Vaut None quand l'ordinateur fait son premier coup du tour

    Sortie : tuple[int, tuple[int, int], tuple[int, int]] | None - Le type de déplacement (0 = déplacement, 1 = capture) Les coordonnées du pion d'origine et celles de la case d'arrivée/celle du pion à capturer, ou None si l'ordinateur ne trouve aucun coup
    """
    move = alpha_beta_pruning((grille, None, (None, pion_impose)), joueur, 8)
    if move is None:
        return None
    return move[2] 
