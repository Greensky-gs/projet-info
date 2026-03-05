# projet-info

CS project for my college

## Tools

Projet écrit en C (natif), se joue dans un terminal car la consigne le demande

## Projet

Faire un jeu de dame avec les règles suivantes (non-exhaustives) :
* Plateau de taille 8x8
* Captures en diagonale classique + captures en arrière (toujours en diagonale)
* Promotion en dame provoque la mort subite :
  * Capture le pion adverse le plus proche
  * Renvoie le pion sur sa rangée de départ
* Captures obligatoires
* Faire ça en python

## Utilisation

Vous pouvez utiliser le projet de deux manières

### En C

Suivez ces étapes (il faut au moins **gcc**, et **make** peut aider)

1. Cloner le projet ( `git clone https://github.com/Greensky-gs/projet-info` )
2. Compiler : avec make : `make all`, sans make : compiler tous les fichiers C en un exécutable
3. Exécuter : `./bin/main.uwu` (par défaut)

### En python

Il vous faudra **gcc** (et **make**, si besoin)

1. Cloner le projet ( `git clone https://github.com/Greensky-gs/projet-info` )
2. Compiler en une librarie partagée : `make shared`. La sortie sera dans `build/shared.so`
3. L'inclure dans un fichier python, de la manière suivante :

```py
from ctypes import CDLL

game = CDLL("./checkers.so")
_ = game.main()
``` 
(ou voir exemple : [`python.example.py`](./python.example.py))

Pour ça, il faut avoir le fichier python situé au même endroit que le fichier **.so**
