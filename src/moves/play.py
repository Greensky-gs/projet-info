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
    Sortie : 'capture' | 'deplacement'
    """
    peut_capturer = len(detection_captures_joueur(grille, tour)) > 0
    peut_deplacer = len(detection_deplacements_joueur(grille, tour)) > 0

    saisie = None
    while not (saisie == 'capture' or saisie == 'deplacement'):
        print(f"Veuillez choisir votre type de coup : [{"capture" if peut_capturer else "déplacement" }]")
        res = input("> ")

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

def capture_case(grille, tour, options):
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

            if saisie_target is None:
                raise NotImplementedError() # N'arrive jamais, c'est pour que le linter ne détecte pas d'erreur sur la ligne suivante

            if not deplacement_capture(grille, saisie[0], saisie[1], saisie_target[0], saisie_target[1], case_grille(grille, saisie[0], saisie[1])):
                print("\x1b[31mLa capture n'a pas eu lieu, réessayez\x1b[0m")
                continue
            print("Le pion a été capturé !")

            targetx = (saisie_target[0] - saisie[0]) * 2 + saisie[0]
            targety = (saisie_target[1] - saisie[1]) * 2 + saisie[1]

            if appliquer_mort_subite(grille, tour):
                return;

            afficher_grille(grille, tour)
            targets = detection_captures_pions(grille, (targetx, targety))
            saisie = (targetx, targety)
            target_msg = f"Choisissez un pion à capturer parmi {", ".join(list(map(afficher_cords, targets)))} : "
        return

def deplacement_case(grille, tour, options):
    pass

def tour_de_jeu(grille, tour):
    """Effectue un tour de jeu complet (saisie, et application)
    
    Entrée : grille, tour
        grille : La grille
        tour   : Le joueur qui doit jouer ( 1 = Blanc, 2 = Noir )
    Sortie : Rien
    """
    type_deplacement = select_deplacement(grille, tour)

    options = detection_captures_joueur(grille, tour) if type_deplacement == 'capture' else detection_deplacements_joueur(grille, tour)
    
    if type_deplacement == 'capture':
        capture_case(grille, tour, options)
    
