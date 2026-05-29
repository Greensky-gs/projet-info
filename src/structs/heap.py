import math
# Implémentation d'un arbre binaire de recherche avec des tableaux

"""
Note : Ces abres binaires de recherches sont conçus pour stocker des tuple, dont le premier élement est la valeur utilisé pour les comparaisons
"""
def abr_creer(taille_max = 256):
    return [None] * taille_max

def abr_sommet(abr):
    return abr[0]

def abr_inserer(abr, elt, taille, remplacement_si_pas_de_place = False):
    i = 0
    while abr[i] is not None and i < taille:
        i += 1
    if i >= taille and not remplacement_si_pas_de_place:
        return
    elif i >= taille and remplacement_si_pas_de_place: # On remplace le dernier noeud si pas de place. La raison à celà est que on va garder des scores, autant garder les meilleurs
        i -= 1

    abr[i] = elt
    parent_index = math.floor((i - 1) / 2)

    index = i
    while parent_index >= 0 and abr[parent_index][0] < abr[index][0]:
        # On échange ces deux valeurs, jusqu'à avoir que le parent est supérieur ou égal à tout ses fils
        abr[parent_index], abr[index] = abr[index], abr[parent_index]

        index = parent_index
        parent_index = math.floor((index - 1) / 2)

def abr_pop(abr, taille):
    last_element_index = 0
    while abr[last_element_index] is not None:
        last_element_index += 1
    if last_element_index == 0:
        return None
    if last_element_index == 1:
        copy = abr[0][:]
        abr[0] = None

        return copy

    last_element_index = last_element_index - 1

    copy = abr[0][:]
    abr[0] = abr[last_element_index]

    left_child_index = 1
    right_child_index = 2
    index = 0
    while (left_child_index < taille and abr[left_child_index] is not None and abr[index][0] < abr[left_child_index][0]) or (right_child_index < taille and abr[right_child_index] is not None and abr[index][0] < abr[right_child_index][0]):
        if left_child_index < taille and abr[left_child_index] is not None and abr[index][0] < abr[left_child_index][0]:
            abr[left_child_index], abr[index] = abr[index], abr[left_child_index]
            index = left_child_index
            left_child_index = 2 * index + 1
            right_child_index = 2 * index + 2

        if right_child_index < taille and abr[right_child_index] is not None and abr[index][0] < abr[right_child_index][0]:
            abr[right_child_index], abr[index] = abr[index], abr[right_child_index]
            index = right_child_index
            left_child_index = 2 * index + 1
            right_child_index = 2 * index + 2

    return copy
