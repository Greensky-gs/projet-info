import logging
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

def ligne_str(ligne, coup):
    """Représente un ligne de coups sous forme de texte"""
    return ligne + "{}{}{}{}".format(coup[0], coup[1], coup[2], coup[3])

def analyse_libre(grille, joueur):
    """
    Analyse la grille librement (sans devoir jouer un pion en particulier)
    Entrée: grille, joueur
        grille : la grille
        joueur : la couleur qui représente l'ordinateur

    Sortie: tuple[bool, int, int, int, int] - Si c'est une capture, et le coup choisit par l'ordinateur
    """ 
    T_MAX = 8192
    scores = abr_creer(T_MAX)

    # On trouve tous les coups autorisés, puis on les "joue", et on assigne un score à chacune des grilles, en gardant seulement la meilleure
    captures = detection_captures_joueur(grille, joueur)
    if len(captures) > 0:
        for capture in captures:
            captures_pion = detection_captures_pions(grille, capture)
            for capture_pion in captures_pion:
                clone = [row[:] for row in grille]

                deplacement_capture(clone, capture[0], capture[1], capture_pion[0], capture_pion[1], joueur)
                appliquer_mort_subite(clone, joueur)

                score = score_position(clone, joueur)
                abr_inserer(scores, [score, ligne_str("", (capture[0], capture[1], capture_pion[0], capture_pion[1]))], T_MAX)
    else:
        moves = detection_deplacements_joueur(grille, joueur)
        for move in moves:
            moves_pion = detection_deplacements_pions(grille, move)
            for move_pion in moves_pion:
                clone = [row[:] for row in grille]

                deplacement_mouvement(clone, move[0], move[1], move_pion[0], move_pion[1], joueur)
                appliquer_mort_subite(clone, joueur)

                score = score_position(clone, joueur)
                abr_inserer(scores, [score, ligne_str("", (move[0], move[1], move_pion[0], move_pion[1]))], T_MAX)

    meilleur_coup = abr_sommet(scores)
    if meilleur_coup is None:
        return None

    return (
            len(captures) > 0,
            int(meilleur_coup[1][0]),
            int(meilleur_coup[1][1]),
            int(meilleur_coup[1][2]),
            int(meilleur_coup[1][3])
    )

def analyse_ciblee(grille, joueur, pion):
    """
    Analyse tous les coups possibles pour un pion donnée, récursivement
    Entrée: grille, joueur, pion, profondeur
        grille         : le plateau
        joueur         : la couleur qui représente l'ordinateur
        pion           : tuple[int, int] - Le pion à analyser

    Sortie: tuple[bool, tuple[int, str]] | None - Si le coup est une capture, et ensuite le coup que l'ordinateur a choisit sous forme de texte à parser en int, précédé de son score. Peut valoir None
    """
    T_MAX = 8192
    scores = abr_creer(T_MAX)

    captures = detection_captures_pions(grille, pion)
    if len(captures) > 0:
        for capture in captures:
            clone = [r[:] for r in grille]

            deplacement_capture(clone, pion[0], pion[1], capture[0], capture[1], joueur)
            appliquer_mort_subite(clone, joueur)
                
            score = score_position(clone, joueur)

            abr_inserer(scores, [score, ligne_str("", (pion[0], pion[1], capture[0], capture[1]))], T_MAX)
    else:
        moves = detection_deplacements_pions(grille, pion)
        for move in moves:
            clone = [ r[:] for r in grille ]

            deplacement_mouvement(clone, pion[0], pion[1], move[0], move[1], joueur)
            appliquer_mort_subite(clone, joueur)

            score = score_position(clone, joueur)

            abr_inserer(scores, [score, ligne_str("", (pion[0], pion[1], move[0], move[1]))], T_MAX)
    meilleur = abr_sommet(scores);
    if meilleur is None:
        return None
    return (
            len(captures) > 0,
            int(meilleur[1][0]),
            int(meilleur[1][1]),
            int(meilleur[1][2]),
            int(meilleur[1][3])
    )

def alpha_beta_pruning(
        grille: tuple[list[list[int]], None | tuple[bool, tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
        joueur,
        profondeur = 1,
        alpha = -sys.maxsize - 1,
        beta = sys.maxsize,
        est_bot = True,
        top = True
) -> tuple[int, list[list[int]], None | tuple[bool, tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]]:
    if profondeur == 0 or est_partie_finie(grille[0], joueur)[0]:
        return (
            score_position(grille[0], joueur),
            grille[0],
            grille[1],
            grille[2]
        )

    if beta <= alpha:
        return (beta, grille[0], grille[1], grille[2])

    if est_bot is True:
        meilleur: tuple[int, list[list[int]], None | tuple[bool, tuple[int, int], tuple[int, int]]] = (-sys.maxsize - 1, [ row[:] for row in grille[0] ], None)
        pion_impose = grille[2][1]

        coups = list_coups_grille(grille[0], joueur, pion_impose)
        for coup in coups:
            clone = [ row[:] for row in grille[0] ]

            if coup[0] is True:
                deplacement_capture(clone, coup[1][0], coup[1][1], coup[2][0], coup[2][1], joueur)
            else:
                deplacement_mouvement(clone, coup[1][0], coup[1][1], coup[2][0], coup[2][1], joueur)
                pion_impose = None
            nouvelle_pos = [-1, -1]
            mort_subite = appliquer_mort_subite(clone, joueur, nouvelle_pos)

            logging.info(f"({profondeur}) calling {profondeur - 1}")
            val = alpha_beta_pruning(
                (clone, coup),
                joueur,
                profondeur - 1,
                alpha,
                beta,
                False,
                False
            )
            logging.info(f"({profondeur}) received val = ({val[0], val[2]}) vs ({(meilleur[0], meilleur[2])})")
            
            if val[0] > meilleur[0]:
                meilleur = (
                    val[0],
                    [ row[:] for row in val[1] ],
                    grille[1] if not top else coup
                )
                alpha = max(alpha, val[0])
                if alpha >= beta:
                    break
    else:
        meilleur: tuple[int, list[list[int]], None | tuple[bool, tuple[int, int], tuple[int, int]]] = (sys.maxsize, [ row[:] for row in grille[0] ], None)
        coups = list_coups_grille(grille[0], joueur_adverse(joueur))
        for coup in coups:
            clone = [ row[:] for row in grille[0] ]

            if coup[0] is True:
                deplacement_capture(clone, coup[1][0], coup[1][1], coup[2][0], coup[2][1], joueur)
            else:
                deplacement_mouvement(clone, coup[1][0], coup[1][1], coup[2][0], coup[2][1], joueur)
            appliquer_mort_subite(clone, joueur)

            val = alpha_beta_pruning(
                (clone, coup),
                joueur,
                profondeur - 1,
                alpha,
                beta,
                True,
                False
            )
            
            if val[0] < meilleur[0]:
                meilleur = (
                    val[0],
                    [ row[:] for row in val[1] ],
                    grille[1] if not top else coup
                )
                beta = min(beta, val[0])
                if beta <= alpha:
                    break

    logging.info(f"({profondeur}) Returning meilleur = {(meilleur[0], meilleur[2])}")
    return (
        meilleur[0],
        [ row[:] for row in meilleur[1] ],
        meilleur[2]
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

    logging.basicConfig(filename="test/logs.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)03d %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)
    logging.info(f"Starting analyse with joueur = {joueur}")
    move = alpha_beta_pruning((grille, None, (None, None)), joueur, 8)
    logging.info(f"Ending analyse with joueur = {joueur}")
    if move is None:
        return None
    logging.info(f"move = {move}")
    logging.info(f"Move = {move[2]}")

    return move[2] 
