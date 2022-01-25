import random

class Affichage:
    def __init__(self):
        self.map_visuelle = [] # représentation graphique aire de jeu

    def afficher_menu_debut(self):
        reponse = input('''Choisir mode de difficulté; entrer:
1 - mode facile
2 - mode ordinaire
3 - mode difficile
>>> Votre réponse: ''')
        return reponse

    def demarrer_partie(self, partie, compte_zappeur):
        self.creer_aire_jeu(partie)
        self.creer_docteur(partie, compte_zappeur)
        self.creer_dalek(partie)
        self.positionner_docteur(partie)
        self.positionner_initial_dalek(partie)
        self.afficher_aire_jeu()

    def creer_aire_jeu(self, partie):
        for ligne in range(partie.y):
            ligne = []
            for case in range(partie.x):
                ligne.append('-')
            self.map_visuelle.append(ligne)
        return self.map_visuelle

    def creer_docteur(self, partie, compte_zappeur):
        from main import Docteur
        partie.docteur = Docteur(compte_zappeur)
        # assigner coordonnées (position) initiale/s
        partie.docteur.x = (round(partie.x / 2)) -1 # correspond à colonne
        partie.docteur.y = (round(partie.y / 2)) -1 # correspond à ligne

    def creer_dalek(self, partie):
        from main import Dalek
        if partie.niveau == 1:
            for i in range(5):
                partie.dalek.append(Dalek(i+1))
        elif partie.niveau == 2:
            for i in range(10):
                partie.dalek.append(Dalek(i+1))
        elif partie.niveau == 3:
            for i in range(15):
                partie.dalek.append(Dalek(i+1))
        elif partie.niveau == 4:
            for i in range(20):
                partie.dalek.append(Dalek(i+1))
        # rajout de niveaux éventuels
        # elif ...
        else:
            print("Vous avez surmonté tous les niveaux et gagné le jeu, 🏆")

    def positionner_docteur(self, partie):
        self.map_visuelle[partie.docteur.y][partie.docteur.x] = 'D'

    def positionner_initial_dalek(self, partie):
        id_dalek = 1
        while id_dalek <= len(partie.dalek):
            position_x_dalek = random.randrange(0, partie.x)
            position_y_dalek = random.randrange(0, partie.y)
            if self.map_visuelle[position_y_dalek][position_x_dalek] == '-':
                partie.dalek[id_dalek -1].x = position_x_dalek
                partie.dalek[id_dalek -1].y = position_y_dalek
                self.map_visuelle[position_y_dalek][position_x_dalek] = 'k'
                id_dalek += 1

    def positionner_dalek(self, partie):
        for k in partie.dalek:
            if self.map_visuelle[k.y][k.x] == '-':
                self.map_visuelle[k.y][k.x] = 'k'
            elif self.map_visuelle[k.y][k.x] == 'k':
                # cas de collision entre deux Daleks
                # deux Daleks doivent mourrir ET +10 au score
                position_x_collision = k.x
                position_y_collision = k.y
                print(k.y, k.x)   # supposer être position collision
                print("collision entre " + str(k.id))
                #  pour chaque Dalek de liste partie.dalek, trouver autre Dalek à supprimer selon position collisions
                for k2 in partie.dalek:
                    if k2.y == position_y_collision and k2.x == position_x_collision:
                        print(" et " + str(k2.id))
                    
                        # supprimer le troisième Dalek entrant en collision (possiblement)
                        for k3 in partie.dalek:
                            if k3.y == position_y_collision and k3.x == position_x_collision:
                                print(" et " + str(k3.id))
                                partie.dalek.remove(k3)
                        
                        partie.dalek.remove(k2)

                partie.dalek.remove(k) # del partie.dalek[k.id - 1]  # supprimer objet Dalek qui rentre en collision

                # créer tas de ferraille à cette même coordonnée
                from main import Ferraille
                nouvelle_ferraille = Ferraille(len(partie.ferrailles) + 1)
                partie.ferrailles.append(nouvelle_ferraille)  # nouvel objet Ferraille
                print(partie.ferrailles[len(partie.ferrailles) -1])
                partie.ferrailles[len(partie.ferrailles) -1].x = position_x_collision
                partie.ferrailles[len(partie.ferrailles) -1].y = position_y_collision
                print("Position de la feraille")
                print(partie.ferrailles[len(partie.ferrailles) - 1].x)
                print(partie.ferrailles[len(partie.ferrailles) - 1].y) 
                self.map_visuelle[position_y_collision][position_x_collision] = 'f'  # case occupée par tas ferraille
                
                # augmenter score de 10
                partie.score += 10
            elif self.map_visuelle[k.y][k.x] == 'f':  # si Dalek rentre collision avec tas ferraille, Dalek meurt
                print(k.id)
                print("Frappe tas de ferraille")
                
                partie.dalek.remove(k) # del partie.dalek[k.id - 1]  # supprimer objet Dalek qui rentre en collision
                partie.score += 5

    def afficher_aire_jeu(self):
        for case in self.map_visuelle:
            print(case)

    def afficher_menu_jeu(self):
        reponse = input('''w -> déplacer Docteur vers haut
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

    # False: déplacement invalide du docteur car tas de ferraille à l'arrivée
    # True: déplacement valide du docteur car aucun tas de ferraille à l'arrivée
    def verifier_si_tas_ferraille(self, direction, partie):
        if direction == 'w':
            if self.map_visuelle[partie.docteur.y - 1][partie.docteur.x] == 'f':  # une ligne de moins
                return False
        elif direction == 'd':
            if self.map_visuelle[partie.docteur.y][partie.docteur.x + 1] == 'f':  # une colonne de +
                return False
        elif direction == 's':
            if self.map_visuelle[partie.docteur.y + 1][partie.docteur.x] == 'f':  # une ligne de +
                return False
        elif direction == 'a':
            if self.map_visuelle[partie.docteur.y][partie.docteur.x - 1] == 'f':  # une colonne de -
                return False
        else:  # demeure à même intersection
            pass
        return True

