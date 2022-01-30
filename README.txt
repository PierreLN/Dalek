PROJET DALEKS
============

Auteurs: Manil Boudjemai, Pierre Long Nguyen
Date de remise: 31 Janvier, 2022
Titre: Daleks
Language de programmation: Python

|~ Every day is a learning day ~|

INTRODUCTION
============

Dans le jeu DALEK, on prend le controle du Docteur WHO de la serie télévisée britannique de science-fiction créée par Sydney Newman et Donald Wilson.
Le joueur doit éviter d'entrer en colision avec les Daleks par différent moyens. À chaque action du joueur, les Dalek se rapporchent du dernier. 
Une seule collision met fin à la partie.   

PARTICULARITÉS ET DEROULEMENT DU JEU
=====================

Le jeu peut être joué selon 3 modes de difficultés:
- facile
- ordinaire
- difficile

Dès qu'un niveau débute, le docteur, soit le contrôle du joueur, est placé au centre de l'aire de jeu.
Les daleks sont positionnés aléatoirement sur l'aire de jeu.

Le jeu est composé de 5 niveaux. Lorsque le joueur débute la partie, il est confronté à 5 daleks (niveau 1).
Progressivement, d'un niveau à un autre, le joueur est confronté à 5 daleks additionnels dès le début du niveau.
Si le joueur complète les 5 niveaux, il gagne le jeu.

Le joueur doit éviter de rentrer en contact avec un dalek; si c'est le cas, le joueur perd la partie.

Les daleks sont éliminés si 2 ou 3 d'entre eux rentrent en collision l'un avec l'autre...
- un tas de ferraille à la case où la collision est survenue apparaît
    - le docteur ne peut pas se positionner sur une case occupée par un tas de ferraille
        - le tour n'est pas perdu, aucun déplacement de la part des daleks; le joueur en est averti
    - le docteur ne peut pas se téléporter sur une case occupée par un tas de ferraille
    - de plus, les daleks sont aussi éliminés si ils rentrent en collision avec un tas de ferraille

Pour chaque dalek éliminé, +5 points au score pour le docteur...
- il est possible de consulter son score en entrant 'q' lorsque demandé par le programme

Les tas de ferrailles disparaissent à chaque début de niveau.

Le joueur peut téléporter le docteur à volonté:
- permet de se repositionner pour tenter d'échapper à une mort soudaine
- selon le mode de difficulté choisi:
    - facile
        - déplacement sur une case vide à proximité d'au moins deux cases de distance d'un ou de plusieurs daleks
    - ordinaire
        - déplacement sur une case vide; un ou plusieurs daleks peuvent se retrouver à proximité d'une case du docteur
    - difficile
        - déplacement possible sur une case vide ou un dalek (un coup de chance)
            - aucune évaluation est faite concernant la proximité d'un ou de plusieurs daleks par rapport au docteur
                - si le docteur se téléporte sur un dalek; le joueur perd le niveau, et donc, la partie aussi

Le joueur peut éliminer des daleks avec un zappeur:
- élimine tous daleks à proximité d'une case dans les 8 directions possibles, depuis la position centrale du docteur
    - le zappeur est acquis à chaque début de niveau
        - 1x par niveau
    - le zappeur est cummulable d'un niveau à l'autre

Le joueur ne peut pas déplacer le docteur hors de la matrice; si c'est le cas, le joueur perd son tour.
Une notification est affiché pour avertir le joueur d'éviter de se déplacer hors de la matrice.

INSTRUCTIONS D'UTILISATIONS
===========================

Pour déplacer le docteur:
- 'w' vers le haut
- 'd' vers la droite
- 's' vers le bas
- 'a' vers la gauche
- 'e' pour passer son tour et rester à la même position

Outils disponibles:
- 't' pour teleporter aléatoirement sur le terrain
- 'z' pour zapper les Daleks à portée immédiate

Affichage et menu de jeu:
- 'r' pour reinitialiser le jeu
- 'q' pour afficher le score de la partie actuelle
    - ainsi que des informations sur le niveau courant et le compte de zappeur disponibles
    - entrer "back" pour revenir au menu du jeu

BUGS
====

La collision de deux Dalek ou plus avec le même tas de ferraille n'efface pas tous les Daleks tout le temps.
Quelques fois, un Dalek disparaît et réapparaît au tour suivant 
- très fréquent autour des collisions et des tas de ferrailles!

À certains moment, moins que la moitié du temps, le zap produit une erreur IndexError (list out of range)
- on suppose que c'est dû au conditions évaluant la portée du zappeur

CARACTÉRISTIQUES ET AMÉLIORATIONS SUGGÉRÉES
===========================================

- Permettre le déplacement en diagonale du docteur et des daleks.

- Ajout de vies supplémentaires si le docteur se déplace sur un case symbolisée par un 'v'

- Ajout de zappeur supplémentaires si le docteur se déplace sur une case symbolisée par un 'z'

Options:
- entrée "to end"
    - permet au joueur de rouler le programme jusqu'à la fin du niveau
        - le joueur gagne le niveau en question si tous les daleks rentrent en collision
        - le joueur perd le niveau, et donc la partie, si un dalek rentre en contact avec le docteur
- entrée "-1"
    - permet au joueur de rouler le programme jusqu'à la fin du niveau
        - si, avant la fin de la vague, un dalek se retrouve à proximité d'une case du docteur...
            - le déroulement automatique du programme est interrompu
                - permet au joueur d'effectuer une action pour éviter de perdre le niveau
        - si, tous les daleks rentrent en collision et que jamais un dalek se retrouve à proximité d'une case du docteur...
            - le joueur gagne le niveau et passe au prochain


REFERENCES
==========

https://en.wikipedia.org/wiki/Dalek_Attack
https://tardis.fandom.com/wiki/Doctor_Who


Lien github:

Manil: https://github.com/manilboudjemai
Pierre: https://github.com/PierreLN