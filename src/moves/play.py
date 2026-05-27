from _headers.constants import *
from moves.capture import *
from moves.capture import *
from moves.detection import *
from moves.move import *
from structs.user.interface import saisir_coordonnees
from aux.utils import afficher_cords
from suddendeath.detection import *

# Tour de jeu d'un joueur
def select_deplacement(grille, tour):
    """
    Obtient le type de déplacement du joueur

    
    Entrée : grille, tour
        grille : La grille
        tour   : Le joueur qui doit jouer ( 1 = Blanc, 2 = Noir )
    Sortie : 'capture' | 'deplacement' | 'abandon'
    """
    peut_capturer = len(detection_captures_joueur(grille, tour)) > 0
    available = [ 'capture', 'deplacement', 'abandon' ]

    saisie = None
    while not (saisie in available):
        print(f"Veuillez choisir votre type de coup : [{"capture" if peut_capturer else "déplacement" }/abandon]")
        res = input("> ")
        if len(res) <= 0:
            print("Votre saisie est invalide")
            continue

        if res.lower() == 'abandon':
            saisie = 'abandon'
            continue

        if peut_capturer and res != 'capture':
            print("Votre saisie est invalide.")
            continue

        if peut_capturer:
            saisie = 'capture'
            continue
        if res != 'déplacement':
            print("Votre saisie n'est pas valide")
            continue
        saisie = 'deplacement'

    return saisie

def capture_case(grille, tour, options, noms_joueurs):
    """
    Effectue la capture complète d'un joueur
    Entée : grille, tour, options, noms_joueurs
        grille       : La grille
        tour         : Le tour actuel
        options      : Les pions disponibles pour la capture
        noms_joueurs : Les noms des joueurs
    Sortie : bool - True si la mort subite a été appliquée, False sinon
    """

    cases = options
    msg = f"Choisissez un pion pour capturer parmi : {", ".join(list(map(afficher_cords, cases)))} : "

    while len(cases) > 0:
        saisie = saisir_coordonnees(grille, tour, msg)
        if saisie is None:
            print("Votre saisie n'est pas valide");
            continue
        if not saisie in cases:
            print("  Votre saisie n'est pas dans la liste")
            continue

        targets = detection_captures_pions(grille, saisie)
        target_msg = f"Choisissez un pion à capturer parmi {", ".join(list(map(afficher_cords, targets)))} : "

        while len(targets) > 0:
            saisie_target = saisir_coordonnees(grille, tour, target_msg)
            if saisie_target is None:
                print("Votre saisie n'est pas valide");
                continue;
            if not saisie_target in targets:
                print("Votre saisie n'est pas dans la liste");
                continue

            if not deplacement_capture(grille, saisie[0], saisie[1], saisie_target[0], saisie_target[1], case_grille(grille, saisie[0], saisie[1])):
                print("\x1b[31mLa capture n'a pas eu lieu, réessayez\x1b[0m")
                continue
            print("Le pion a été capturé !")

            targetx = (saisie_target[0] - saisie[0]) * 2 + saisie[0]
            targety = (saisie_target[1] - saisie[1]) * 2 + saisie[1]

            if appliquer_mort_subite(grille, tour):
                return True

            effacer_console()
            afficher_grille(grille, tour, noms_joueurs)

            targets = detection_captures_pions(grille, (targetx, targety))
            saisie = (targetx, targety)
            target_msg = f"Choisissez un pion à capturer parmi {", ".join(list(map(afficher_cords, targets)))} : "
        return False

def deplacement_case(grille, tour, options):
    """
    Effectue le déplacement complet d'un joueur
    Entrée : grille, tour, options
        grille  : La grille
        tour    : Le tour actuel
        options : Les pions disponibles pour un joueur

    Sortie : True si la mort subite a été appliquée, False sinon
    """
    cases = options
    msg = f"Choisissez un pion à déplacer parmi : {", ".join(list(map(afficher_cords, cases)))} : "

    while len(cases) > 0:
        saisie = saisir_coordonnees(grille, tour, msg)

        if saisie is None:
            print("Votre saisie n'est pas valide");
            continue
        if not saisie in cases:
            print("    Votre saisie n'est pas dans la liste")
            continue

        targets = detection_deplacements_pions(grille, saisie)
        target_msg = f"Choisissez une case pour votre pion parmi {", ".join(list(map(afficher_cords, targets))) } : "

        while len(targets) > 0:
            saisie_target = saisir_coordonnees(grille, tour, target_msg);
            if saisie_target is None:
                print("Votre saisie n'est pas valide");
                continue;
            if not saisie_target in targets:
                print("Votre saisie n'est pas dans la liste des cases disponibles")
                continue

            if not deplacement_mouvement(grille, saisie[0], saisie[1], saisie_target[0], saisie_target[1], case_grille(grille, saisie[0], saisie[1])):
                print("\x1b[31mLe mouvement n'a pas eu lieu, réessayez\x1b[0m")
                continue;
            if appliquer_mort_subite(grille, tour):
                return True;
            return False;

def tour_de_jeu(grille, tour, noms_joueurs):
    """Effectue un tour de jeu complet (saisie, et application)
    
    Entrée : grille, tour
        grille       : La grille
        tour         : Le joueur qui doit jouer ( 1 = Blanc, 2 = Noir )
        noms_joueurs : Le nom des joueurs
    Sortie : bool | None - True si la mort subite a été appliquée, False sinon. Vaut None quand le joueur abandonne
    """
    type_deplacement = select_deplacement(grille, tour)
    if type_deplacement == "abandon":
        return None    

    options = detection_captures_joueur(grille, tour) if type_deplacement == 'capture' else detection_deplacements_joueur(grille, tour)
    
    if type_deplacement == 'capture':
        return capture_case(grille, tour, options, noms_joueurs)
    elif type_deplacement == 'deplacement':
        return deplacement_case(grille, tour, options)
