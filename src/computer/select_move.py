from moves.detection import *
from random import randint
# Fonction de sélection de coup pour l'ordinateur

def choisir_coup_ordinateur(grille, joueur, pion_impose = None) -> tuple[int, tuple[int, int], tuple[int, int]] | None:
    """
    Fait choisir un coup à l'ordinateur, en respectant les règles
    Entrée : grille, joueur, pion_impose
        grille      : la grille de jeu
        joueur      : la couleur que l'ordinateur joue
        pion_impose : Le pion que l'ordinateur est obligé de jouer dans le cas où il doit effectuer des prises successives. Vaut None quand l'ordinateur fait son premier coup du tour

    Sortie : tuple[int, tuple[int, int], tuple[int, int]] | None - Le type de déplacement (0 = déplacement, 1 = capture) Les coordonnées du pion d'origine et celles de la case d'arrivée/celle du pion à capturer, ou None si l'ordinateur ne trouve aucun coup
    """
    if pion_impose is None:
        captures = detection_captures_joueur(grille, joueur)
        if len(captures) > 0:
            ## Choix au hasard d'une capture possible
            # Choix au hasard du pion qui va capturer
            pion = captures[randint(0, len(captures) - 1)]

            # Choix au hasard d'une case à capturer pour ce pion
            cibles = detection_captures_pions(grille, pion)
            cible = cibles[randint(0, len(captures) - 1)]

            return (1, pion, cible)
        deplacements = detection_deplacements_joueur(grille, joueur)
        if len(deplacements) == 0:
            return None # L'ordinateur "admet" avoir perdu
        ## Choix au hasard du pion à déplacer
        # Choix au hasard d'un pion à déplacer
        pion = deplacements[randint(0, len(deplacements) - 1)]

        # Choix au hasard de la case d'arrivée
        cibles = detection_deplacements_pions(grille, pion)
        cible = cibles[randint(0, len(cibles) - 1)]

        return (0, pion, cible)
    else:
        # La fonction n'est appellée dans ce cas la que si le pion précisé peut capturer
        captures = detection_captures_pions(grille, pion_impose)

        # Choix au hasard d'une capture
        capture = captures[randint(0, len(captures) - 1)]
        return (1, pion_impose, capture)
