# Fonctions d'interface du tour
def inverser_tour(tour):
    """
    Inteverse le tour donné en paramètre
    
    Entrée : tour
        tour : le tour
    Sortie : le tour inversé
    """
    return (tour % 2) + 1
def couleur_tour(tour):
    return "blanc" if tour == 1 else "noir"
# Fin des fonctions d'interface du tour
