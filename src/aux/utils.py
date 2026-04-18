# Fonctions utilitaires

def est_au_bon_format(message):
    """
    Entrée : string : une chaine de caractères contenant une case, en théorie.
    Sortie : bool : si oui ou non le message contient une case valide. La sortie vaut True si le code peut lire une entrée AU BON FORMAT, pas avec les BONNE VALEURS. Autrement dit, si la saisie dépasse la grille, la fonction renverra quand même True
    """

    if len(message) < 2:
        return False

    lettre = message[0]
    suite = message[1:]

    if not ((ord("a") <= ord(lettre) <= ord("z") or (ord("A") <= ord(lettre) <= ord("Z")))):
        return False
    
    # Il faut parcourir la suite du message, car il se peut que le nombre fasse plus de 2 chiffres
    i = 0
    while (i < len(suite)):
        # Le premier chiffre ne peut pas être 0 (ce sera un chiffre invalide)
        if i == 0 and not (ord("1") <= ord(suite[i]) <= ord("9")):
            return False

        if not (ord("0") <= ord(suite[i]) <= ord("9")):
            return False
        i+=1
    return True

def extraire_coordonnees(message):
    """
    Entrée : string : une chaine de caractères contenant une case au bon format (Une exception sera levée si ce n'est pas le cas)
    Sortie : (int, int) : les coordonnées (x;y), avec X correspondant à la ligne (correspondant à la lattre saisie), en format PROGRAMME (commençant à 9) et y correspondant à la colone lue (correspondant au chiffre), au format PROGRAMME
    """
    assert est_au_bon_format(message)

    x = ord(message[0])
    if ord("a") <= x <= ord("z"):
        x = x - ord("a") # 0 si x = "a", 1 si x = "b", ...
    else:
        x = x - ord("A") # 0 si x = "A", 1 si x = "B" ...

    # Construction de y par la saisie
    y = 0
    i = 1
    while i < len(message):
        y = y * 10 + (ord(message[i]) - ord("0"))
        i += 1
    return (x, y - 1)

def afficher_cords(data):
    x, y = data
    X = chr(ord("A") + x)
    Y = chr(ord("0") + y + 1)

    return f"{X}{Y}"

# Fin des fonctions utilitaires
