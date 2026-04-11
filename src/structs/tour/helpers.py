# Fonction utilitaires du tour
def joueur_adverse(tour):
    """
    Renvoie le joueur opposé. Même fonction que inverser_tour, mais celle-ci n'a pas pour but d'être utilisée pour changer réellement, il faut voir cette fonction comme un auxilaire et pas une fonction d'interface
    """
    return (tour % 2) + 1
# Fin des fonctions utilitaires du tour
