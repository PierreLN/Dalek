import random

class Affichage:
    def __init__(self):
        self.map_visuelle = []

    def afficher_menu_debut(self):
        reponse = input('''Choisir mode de difficulté; entrer:
1 - mode facile
2 - mode ordinaire
3 - mode difficile
>>> Votre réponse: ''')
        return reponse

    def demarrer_partie(self, partie):
        self.positionner_docteur(partie)
        self.positionner_dalek_initiale(partie)
        self.afficher_aire_jeu()

    def positionner_docteur(self, partie):
        self.map_visuelle[partie.docteur.y][partie.docteur.x] = 'D'

    def positionner_dalek_initiale(self, partie):
        id_dalek = 1
        while id_dalek <= len(partie.dalek):
            position_x_dalek = random.randrange(0, partie.x)
            position_y_dalek = random.randrange(0, partie.y)
            if self.map_visuelle[position_y_dalek][position_x_dalek] == '-':
                partie.dalek[id_dalek -1].x = position_x_dalek
                partie.dalek[id_dalek -1].y = position_y_dalek
                self.map_visuelle[position_y_dalek][position_x_dalek] = 'k'
                id_dalek += 1

    def positionner_dalek(self, dalek):
        self.map_visuelle[dalek.y][dalek.x] = 'k'

    def positionner_tas_ferraille(self, tas_ferraille):
        self.map_visuelle[tas_ferraille.y][tas_ferraille.x] = 'f'

    def afficher_aire_jeu(self):
        for case in self.map_visuelle:
            print(case)

    def afficher_menu_jeu(self):
        reponse = input('''
w -> déplacer Docteur vers haut
d -> déplacer Docteur vers droite
s -> déplacer Docteur vers bas
a -> déplacer Docteur vers gauche
e -> ne pas déplacer Docteur (passer son tour)
t -> téléporter Docteur
z -> zapper Daleks
q -> afficher statistiques
r -> réinitialiser partie
>>> Votre réponse: ''')
        return reponse

    def effacer_position_precedente_docteur(self):
        compte_ligne = len(self.map_visuelle)
        for num_ligne in range(compte_ligne):
            compte_case = len(self.map_visuelle[num_ligne])
            for num_case in range(compte_case):
                if self.map_visuelle[num_ligne][num_case] == 'D':
                    self.map_visuelle[num_ligne][num_case] = '-'
                    return

    def effacer_position_precedente_dalek(self):
        compte_ligne = len(self.map_visuelle)
        for num_ligne in range(compte_ligne):
            compte_case = len(self.map_visuelle[num_ligne])
            for num_case in range(compte_case):
                if self.map_visuelle[num_ligne][num_case] == 'k':
                    self.map_visuelle[num_ligne][num_case] = '-'

    def afficher_menu_stats(self, partie):
        reponse = input(f'''
Niveau courant: {partie.niveau}
Score: {partie.score}
Zappeur disponible: {partie.docteur.compte_zappeur}
>>> écrire "back" puis ENTER pour revenir en arrière: ''')
        return reponse

    def afficher_reinit_jeu(self):
        print('''
-   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
R   É   I   N   I   T   I   A   L   I   S   A   T   I   O   N
-   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
''')