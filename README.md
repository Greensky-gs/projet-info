# projet-info

CS project for my college

## Projet

Faire un jeu de dame avec les règles suivantes (non-exhaustives) :
* Plateau de taille 8x8
* Captures en diagonale classique + captures en arrière (toujours en diagonale)
* Promotion en dame provoque la mort subite :
  * Capture le pion adverse le plus proche
  * Renvoie le pion sur sa rangée de départ
* Captures obligatoires
* Faire ça en python

## Étapes

Le projet est en cours de développement (j'ai pas encore la suite des consignes)

### Build.sh

Le fichier [`./build/sh`](./build.sh) est un fichier "d'assemblage" ; la consigne demandant un seul fichier python

Si `PyAssembler` n'est pas trouvé quand vous exécutez le script, c'est qu'il vous manque mon assembleur python, qui récupère des fichiers python et les copie-colle dans un unique fichier python (avec quelques étapes en plus). Vous pouvez l'installer depuis [https://github.com/Greensky-gs/pyassembler](https://github.com/Greensky-gs/pyassembler)

## Tests

Le projet a été testé sur différentes plateformes :

| OS | Version python |
|:--:|:--------------:|
| Archlinux | 3.14 |
| Windows | 3.10 |
| Windows | 3.11 |
| Windows | 3.14 |
| Ubuntu  | 3.12 |
| Fedora  | 3.14 |
