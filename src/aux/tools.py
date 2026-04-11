# Fonctions outils
"""
Les fonctions outils sont des petites fonctions, qui permettent de simplifier une expression (exemple: une grande condition, qui ne tiendrait pas sur une ligne de if, donc elle est factorisé en une petite fonction ici

Ces fonctions, généralement 4 lignes, ne seront pas testées
"""

def valeur_case_depart(x, y):
    if (x + y) % 2 != 1:
        return 0
    if x >= 3 and x < 5:
        return 0
    if x < 3:
        return 2
    return 1

# Fin des fonctions outils
