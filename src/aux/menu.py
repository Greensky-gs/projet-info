from typing import Literal # Pour le typage du dictionnaire, sinon c'est horrible

# La fonction suivante contient une décalaration de type
#    Il est optionnel, mais ça m'aide pour développer, d'avoir une structure et de savoir à quoi elle ressemble.
#    Ici il s'agit d'une liste de tuple contenant trois élélements de type texte
def menu(nom: str, options: list[tuple[str, str, str]]):
    print(f"    {nom}    ")

    length = len(nom) + 4 * 2
    print("=" * length)
