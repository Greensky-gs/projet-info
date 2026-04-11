# Fonction de test
def tester_fonction_avec_jeu(fonction, jeu, interruption_quand_echec = True):
    """
    fonction facultative permettant d'automatiser le test d'une fonction (avec des couleurs parce que c'est la vie)
    Cette fonction ne permet que de vérifier qu'une autre fonction renvoie les résultats attendus sur certaines valeurs de paramètres

    fonction est une fonction
    jeu est une liste de la forme : list[(T, list[...])], avec T le type de retour de la fonction, et list[...] la liste des paramètres, où la premiere valeur est le résultat attendu de la fonction

    Cette fonction renvoie True si la fonction a passé tout ses tests, False sinon
    Quand interruption_quand_echec est mis à True, une erreur est levée avec raise(AssertionError)
    """

    print(f"Test de la fonction \x1b[33m{fonction.__name__}\x1b[0m...")

    n = len(jeu)

    display = lambda v: str(v)[:5] + "..." + str(v)[-5:] if len(str(v)) > 10 else str(v)
    displaylist = lambda l: ", ".join(list(map(display, l)))

    tests = 0
    passes = 0
    for test in jeu:
        attendu = test[0]
        params = test[1]

        result = fonction(*params)
        valid = result == attendu

        tests += 1;
        if valid:
            passes +=1

        print(f"\x1b[35m[{tests}/{n}]\x1b[0m \x1b[33m{fonction.__name__}(\x1b[36m{displaylist(params)}\x1b[33m) = \x1b[36m{result}\x1b[34m, attendu : \x1b[36m{attendu}\x1b[35m | ", end = " ")

        if valid:
            print("\x1b[32mvalide\x1b[0m")
        else:
            print("\x1b[31minvalide\x1b[0m")
            if interruption_quand_echec:
                raise(AssertionError("Tests"))

    print(f"La fonction \x1b[33m{fonction.__name__}\x1b[0m a passé \x1b[{31 + (n == passes)}m{passes}\x1b[0m tests sur \x1b[33m{n}\x1b[0m")

    return passes == n

# Fin de fonction de test
