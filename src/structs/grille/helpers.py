from structs.grille.interface import *
from headers.constants import *

def est_dans_grille(grille, x, y):
    return 0 <= x < N and 0 <= y < N

def afficher_grille(grille, tour):
    """
    Affiche la grille. Prend en entrée une grille.
    Ne renvoie rien

    Peut éventuellement faire planter (intentionellement) le programme si la grille n'est pas valide
    """

    delimitation = lambda start, mid, sep, end: start + (mid + sep) * (N - 1) + mid + end # Fonction auxiliaire qui permet d'obtenir le séparateur
    
    print(" " * 5, end="");
    for i in range(N):
        print(f" {str(i + 1): <2} ", end="")
    print("")

    print(" " * 4 + delimitation("╔", 3 * "═", "╦", "╗"))
    for x in range(N):
        print(f"  {chr(x + 65)} ", end="")
        for y in range(N):
            case = case_grille(grille, x, y)
            if case == None:
                raise(AssertionError())
 
            print("║ ", end="")
            if case == 0:
                print("  ", end="")
            elif case == 1:
                print("● ", end="")
            else:
                print("○ ", end="");
        print("║", end="")

        if x == 0 and tour == 2:
            print("  <--", end="")
        if x == N - 1 and tour == 1:
            print("  <--", end="")

        print("")
        
        if x != N - 1:
            print(" " * 4 + delimitation("╠", 3 * "═", "╬", "╣"));

    print(" " * 4 + delimitation("╚", 3 * "═", "╩", "╝"))
