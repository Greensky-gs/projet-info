from aux.utils import *
from structs.grille.helpers import *

# Fonctions d'interface du joueur
def saisir_coordonnees(grille, tour, msg = None):
    """
    Permet d'obtenir des coordonnées, demandées à l'utilisateur

    Entrée :
        grille     : la grille
        tour (int) : Le tour actuel, permet de s'addresser directement au joueur (Blanc pour 1 et Noir pour 2)
        msg        : [OPTIONNEL] Le message à afficher avant de prendre la coordonnée | Par défaut : f"\x1b[33m{'Noir' if tour == 2 else 'Blanc'}\x1b[0m : veuillez entrer une coordonnée (ex: A1): "
    Sortie : (x, y) : un couple de coordonnées valides, dans la grille
    """
    if msg is None:
        msg = f"\x1b[33m{'Noir' if tour == 2 else 'Blanc'}\x1b[0m : veuillez entrer une coordonnée (ex: A1): "

    entree_valide = False
    entree = None

    while not entree_valide:
        res = input(msg)

        if not est_au_bon_format(res):
            print("Votre entrée n'est pas au bon format, veuillez réessayer.")
            continue

        entree = extraire_coordonnees(res)
        entree_valide = est_dans_grille(grille, entree[0], entree[1])

        if not entree_valide:
            print(f"Vos coordonnées \x1b[90m({entree[0]};{entree[1]})\x1b[0m ne sont pas dans la grille")
            continue;

    return entree

# Fin des fonctions d'interface du joueur
