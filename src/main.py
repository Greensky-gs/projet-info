from random import randint
from time import sleep
from _headers._header import *
from _headers.constants import *
from computer.naive.play import jeu_ordinateur
from structs.grille.helpers import *
from structs.user.interface import *
from aux.utils import *
from tests.tests import *
from moves.play import *
from aux.menu import *

def jcj(grille: list[list[int]]):
    """
    Fonction principale pour le joueur contre joueur

    Prend en paramètre la grille sélectionnée
    """
    nomJ1 = input("\x1b[4mJoueur 1 entrez votre pseudo :\x1b[0m ")
    nomJ2 = input("\x1b[4mJoueur 2 entrez votre pseudo :\x1b[0m ")

    couleurJ1 = randint(1, 2)

    noms = (
        nomJ1 if couleurJ1 == 1 else nomJ2,
        nomJ2 if couleurJ1 == 1 else nomJ1
    )

    print(f"\x1b[1m{nomJ1}\x1b[0m, vous jouerez les \x1b[1m{couleur_tour(couleurJ1)}\x1b[0m")
    print(f"\x1b[1m{nomJ2}\x1b[0m, vous jouerez les \x1b[1m{couleur_tour(joueur_adverse(couleurJ1))}\x1b[0m")

    sleep(1)
    for x in range(3, -1, -1):
        print(f"Début de la partie dans \x1b[1;33m{x}\x1b[0m...", end="\r")
        sleep(1)

    effacer_console()
    
    tour = 1
    res = est_partie_finie(grille, tour)

    afficher_grille(grille, tour, noms)

    while not res[0]:
        mort_subite = tour_de_jeu(grille, tour, noms)
        tour = inverser_tour(tour)

        effacer_console()
        afficher_grille(grille, tour, noms)

        if mort_subite:
            msg = " MORT SUBITE !! "
            base = 4
            taille_plateau = 1 + 4 * N
            delta = (taille_plateau - len(msg)) // 2

            total = base + delta
            print(" " * total, end="")
            print(f"\x1b[47;91;1m{msg}\x1b[0m")
            mort_subite = False
        elif mort_subite == None:
            print(f"\x1b[1m{
                  noms[joueur_adverse(tour) - 1]
            }\x1b[0m a abandonné")
            res = (True, True) # (True, True) car : (Le joueur a abandoné, les tours ont été inversés, donc ce joueur a gagné)
            continue

        res = est_partie_finie(grille, tour)

    if res[1] is True:
        nom_gagnant = nomJ1 if tour == couleurJ1 else nomJ2
        print(f"\x1b[1m{nom_gagnant}\x1b[0m a gagné !")
    else:
        nom_gagnant = nomJ2 if tour == couleurJ1 else nomJ1
        print(f"\x1b[1m{nom_gagnant}\x1b[0m a gagné !")

def jco(grille):
    """
    Fonction principale pour le joueur contre ordinateur

    Prend en paramètre la grille sélectionnée
    """
    nomJ1 = input("\x1b[4mJoueur, entrez votre pseudo :\x1b[0m ")
    nomJ2 = "FryDames1"

    couleurJ1 = randint(1, 2)

    noms = (
        nomJ1 if couleurJ1 == 1 else nomJ2,
        nomJ2 if couleurJ1 == 1 else nomJ1
    )

    print(f"\x1b[1m{nomJ1}\x1b[0m, vous jouerez les \x1b[1m{couleur_tour(couleurJ1)}\x1b[0m")

    sleep(1)
    for x in range(3, -1, -1):
        print(f"Début de la partie dans \x1b[1;33m{x}\x1b[0m...", end="\r")
        sleep(1)

    effacer_console()
    
    tour = 1
    res = est_partie_finie(grille, tour)

    afficher_grille(grille, tour, noms)

    while not res[0]:
        if tour == couleurJ1:
            mort_subite = tour_de_jeu(grille, tour, noms)
        else:
            mort_subite = jeu_ordinateur(grille, tour, nomJ2, tour, noms)

        tour = inverser_tour(tour)

        effacer_console()
        afficher_grille(grille, tour, noms)

        if mort_subite is True:
            msg = " MORT SUBITE !! "
            base = 4
            taille_plateau = 1 + 4 * N
            delta = (taille_plateau - len(msg)) // 2

            total = base + delta
            print(" " * total, end="")
            print(f"\x1b[47;91;1m{msg}\x1b[0m")
            mort_subite = False
        elif mort_subite == None:
            print(f"\x1b[1m{
                  nomJ2 if couleurJ1 == 1 else nomJ1
            }\x1b[0m a abandonné")
            res = (True, True) # (True, True) car : (Le joueur a abandoné, les tours ont été inversés, donc ce joueur a gagné)
            continue;
        res = est_partie_finie(grille, tour)

    if res[1] is True:
        nom_gagnant = nomJ1 if tour == couleurJ1 else nomJ2
        print(f"\x1b[1m{nom_gagnant}\x1b[0m a gagné !")
    else:
        nom_gagnant = nomJ2 if tour == couleurJ1 else nomJ1
        print(f"\x1b[1m{nom_gagnant}\x1b[0m a gagné !")

if __name__ == "__main__": # Condition permettant d'être excuté seulement en ligne de commande et pas en importation depuis un autre fichier
    option_selectionnee = menu("Mode", [
        ("tests", "Lancer les tests", 0),
        ("JcJ", "Jouer contre un autre joueur", 1),
        ("JcO", "Jouer contre l'ordinateur", 2)
        ]);

    if option_selectionnee == 0:
        executer_tests()
    else:
        grille_selectionne = menu("Grille", [
            ("Début", "Grille initiale, avec tous les pions", 0),
            ("Milieu", "Une configuration de milieu de jeu pré-définie", 1),
            ("Fin", "Une configuration pour la fin de partie", 2)
        ])
        

        grille_depart = [ [ valeur_case_depart(x, y) for y in range(N) ] for x in range(N) ]
        grille_fin = [ [ 0 for _ in range(N) ] for _ in range(N) ]
        grille_fin[1][0] = 1
        grille_fin[4][3] = 2

        grille_milieu = [ [ 0 for _ in range(N) ] for _ in range(N) ]
        for a, b in [ (0, 5), (0, 7), (1, 6), (1, 4), (2, 1), (2, 7), (3, 6) ]:
            set_case(grille_milieu, a, b, 2)
        for a, b in [ (4, 7), (5, 0), (5, 2), (5, 4), (6, 1), (6, 3), (6, 7), (7, 0) ]:
            set_case(grille_milieu, a, b, 1)
    
        grille = [grille_depart, grille_milieu, grille_fin][grille_selectionne]

        if option_selectionnee == 1:
            jcj(grille);
        else:
            jco(grille)
