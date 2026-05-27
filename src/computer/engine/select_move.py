from _headers.constants import *
from moves.detection import *
from moves.capture import *
from moves.move import deplacement_mouvement
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
        est_bot        : bool - Si l'analyse est en train de se faire sur l'ordinateur.
        profondeur     : Le nombre de coups à anticiper. Valeur par défaut : 1
        ligne_actuelle : La ligne de coups, pour garder le fil de ce que l'ordinateur calcule. Valeur par défaut : ""

    Sortie: Tuple[int, str] | None - Le coup que l'ordinateur a choisit sous forme de texte à parser en int, précédé de son score. Peut valoir None
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
    if meilleur == None:
        return None
    return meilleur

def choisir_coup_ordinateur_ameliore(grille, joueur, pion_impose = None) -> tuple[int, tuple[int, int], tuple[int, int]] | None:
    """
    Fait choisir un coup à l'ordinateur, en respectant les règles
    Entrée : grille, joueur, pion_impose
        grille      : la grille de jeu
        joueur      : la couleur que l'ordinateur joue
        pion_impose : Le pion que l'ordinateur est obligé de jouer dans le cas où il doit effectuer des prises successives. Vaut None quand l'ordinateur fait son premier coup du tour

    Sortie : tuple[int, tuple[int, int], tuple[int, int]] | None - Le type de déplacement (0 = déplacement, 1 = capture) Les coordonnées du pion d'origine et celles de la case d'arrivée/celle du pion à capturer, ou None si l'ordinateur ne trouve aucun coup
    """
    if pion_impose is None:
        coup = analyse_libre(grille, joueur)
        if coup is None:
            return None
        return (1 if coup[0] else 0, (coup[1], coup[2]), (coup[3], coup[4]))
    else:
        # En principe on est ici parce qu'on suit un pion parce qu'il a fait une capture
        coup = analyse_ciblee(grille, joueur, pion_impose)
        if coup is None:
            return None
        return (1, (
            int(coup[1][0]),
            int(coup[1][1])
        ), (
            int(coup[1][2]),
            int(coup[1][3])
        ))
