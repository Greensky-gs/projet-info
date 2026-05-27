from aux.tools import *

# La fonction suivante contient une décalaration de type
#    Il est optionnel, mais ça m'aide pour développer, d'avoir une structure et de savoir à quoi elle ressemble.
#    Ici il s'agit d'une liste de tuple contenant deux élélements de type texte, et d'un entier:
#        - Le titre
#        - La description
#        - un identifiant
def menu(nom: str, options: list[tuple[str, str, int]]):
    response = None
    n = len(options)
    msg = ""
    while response is None:
        effacer_console()
        print(f"    {nom}    ")

        length = len(nom) + 4 * 2
        print("=" * length)

        for i in range(n):
            element = options[i]
            print(f"{i + 1}) [{element[0]}] - {element[1]}")

        if len(msg) > 0:
            print(msg)
        print("> ", end="")
        resp = input()
        if not resp.isdigit():
            msg = "\x1b[91mVotre entrée n'est pas un chiffre valide, réessayez\x1b[0m"
        else:
            resp = int(resp) - 1
            if not (0 <= resp < n):
                msg = "\x1b[91mVotre entrée n'est pas une option valide, réessayez\x1b[0m"
            else:
                response = options[resp][2]
    return response
