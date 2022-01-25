import random
import sys
from Affichage import Affichage  # importation classe Affichage depuis Affichage.py

class Controleur:
    def __init__(self):
        self.vue = Affichage()
        self.modele = None  # sera Jeu() après réponse valide pour mode difficulté

    def afficher_menu_debut(self):
        reponse_valide = {  # modes de difficulté
            '1': "facile",
            '2': "ordinaire",
            '3': "difficile"
        }
        reponse = self.vue.afficher_menu_debut()
        if reponse in "123":
            self.modele = Jeu()
            self.modele.partie_courante = Partie()
            self.modele.partie_courante.mode = reponse_valide[reponse]
            self.vue.demarrer_partie(self.modele.partie_courante, 1)  # démarrer partie
            return True
        else:
            print("--- Votre réponse est invalide ---")
            self.afficher_menu_debut()
        return False

    def afficher_menu_jeu(self):
        reponse = self.vue.afficher_menu_jeu()

        if reponse in "wdsae":  # déplacer Docteur
            deplacement_valide = self.vue.verifier_si_tas_ferraille(reponse, self.modele.partie_courante)
            if deplacement_valide:
                # déplacer Docteur
                self.modele.partie_courante.docteur.deplacer_docteur(reponse, self.modele.partie_courante)
                self.vue.effacer_position_precedente_docteur()
                self.vue.positionner_docteur(self.modele.partie_courante)

                # déplacer Daleks
                for k in self.modele.partie_courante.dalek:
                    k.deplacer_dalek(self.modele.partie_courante.docteur)
                self.vue.effacer_position_precedente_dalek()
                self.vue.positionner_dalek(self.modele.partie_courante)
            else:
                print("Le docteur ne peut pas se déplacer sur une intersection occupée par un tas de ferraille")
                self.vue.afficher_aire_jeu()
                self.afficher_menu_jeu()
                return

        elif reponse == "t":
            # téléporter Docteur
            self.modele.partie_courante.docteur.teleporter(self.modele.partie_courante, self.vue)
            self.vue.effacer_position_precedente_docteur()
            self.vue.positionner_docteur(self.modele.partie_courante)

            # déplacer Daleks
            for k in self.modele.partie_courante.dalek:
                k.deplacer_dalek(self.modele.partie_courante.docteur)
            self.vue.effacer_position_precedente_dalek()
            self.vue.positionner_dalek(self.modele.partie_courante)

        elif reponse == "z":
            partie_courante = self.modele.partie_courante
            affichage = self.vue
            daleks = self.modele.partie_courante.dalek  # liste de Daleks existant
            self.modele.partie_courante.docteur.zapper(partie_courante, affichage, daleks)

            # déplacer Daleks
            for k in self.modele.partie_courante.dalek:
                k.deplacer_dalek(self.modele.partie_courante.docteur)
            self.vue.effacer_position_precedente_dalek()
            self.vue.positionner_dalek(self.modele.partie_courante)



        elif reponse == "q":
            reponse = self.afficher_menu_stats()
            if reponse == 'back':
                self.vue.afficher_aire_jeu()
                self.afficher_menu_jeu()
                return

        elif reponse == "r":
            print('''
                    -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
                    R   É   I   N   I   T   I   A   L   I   S   A   T   I   O   N
                    -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
                    ''')
            self.vue.map_visuelle = []  # vider la matrice
            self.modele = None  # pointer nulle part (modele)
            del self.modele # supprimer l'objet Jeu qui contient l'objet Partie... Docteur, Dalek et Ferraille (supprimé aussi)
            bon_traitement = c.afficher_menu_debut()  # CRÉER UN NOUVEAU MODELE SI LE TRAITEMENT EST BON
            if bon_traitement == True:
                c.afficher_menu_jeu()
            return
            
        else:
            print("--- Votre réponse est invalide ---")
            self.afficher_menu_jeu()
            return

        monter_de_niveau = self.verifier_compte_daleks()  # TESTESTESTEST; return TRUE
        partie_termine = self.verifier_si_defaite()
        if not monter_de_niveau and not partie_termine:
            self.vue.afficher_aire_jeu()
        if not partie_termine:
            self.afficher_menu_jeu()

    def afficher_menu_stats(self):
        reponse = input(f'''Niveau courant: {self.modele.partie_courante.niveau}
Score: {self.modele.partie_courante.score}
Zappeur disponible: {self.modele.partie_courante.docteur.compte_zappeur}
>>> écrire "back" pour revenir en arrière: ''')
        return reponse

    def verifier_compte_daleks(self):
        compte_daleks = len(self.modele.partie_courante.dalek)
        if compte_daleks == 0:
            self.modele.partie_courante.niveau += 1
            # supprimer tous les daleks
            for k in self.modele.partie_courante.dalek:
                self.modele.partie_courante.dalek.remove(k)
            # supprimer tous les ferrailles
            for f in self.modele.partie_courante.ferrailles:
                self.modele.partie_courante.ferrailles.remove(f)
            
            print(f'''Docteur: {self.modele.partie_courante.docteur}
Daleks: {self.modele.partie_courante.dalek}
Ferrailles: {self.modele.partie_courante.ferrailles}''')
            print("fin de niveau: il ne reste plus de feraille...right??")
            print(self.modele.partie_courante.ferrailles)
            
            self.vue.map_visuelle = [] # vider la map visuelle en premier, avant d'en recréer une autre
            compte_zappeur_actuel_docteur = self.modele.partie_courante.docteur.compte_zappeur
            compte_zappeur_actuel_docteur += 1 # à chaque niveau accompli, un zappeur de + disponible pour Docteur
            self.vue.demarrer_partie(self.modele.partie_courante, compte_zappeur_actuel_docteur)  # Redémarrer partie
            print(self.modele.partie_courante.niveau)
            return True
        return False

    def verifier_si_defaite(self):
        liste_daleks = self.modele.partie_courante.dalek
        docteur = self.modele.partie_courante.docteur
        for k in liste_daleks:
            if k.y == docteur.y:
                if k.x == docteur.x:
                    print('''
                    -   -   -   -   =   =   -   -   -   -
                    G   A   M   E           O   V   E   R!
                    -   -   -   -   =   =   -   -   -   -
                    ''')
                    return True
        return False

class Jeu:
    def __init__(self):
        self.partie_courante = None
class Partie:
    def __init__(self):
        self.niveau = 1
        self.score = 0
        self.mode = None
        self.x = 8
        self.y = 8
        self.docteur = None
        self.dalek = []  # liste contenant plusieurs daleks
        self.ferrailles = []  # liste contenant plusieurs tas de ferraille

class Docteur:
    def __init__(self, compte_zappeur = 1):
        self.vivant = True
        self.nom = "Who"
        self.x = None
        self.y = None
        self.compte_zappeur = compte_zappeur  # 1 zappeur disponible lors d'un démarrage de partie

    def deplacer_docteur(self, direction, partie):
        if direction == 'w':  # haut
            if self.y > 0:
                self.y -= 1  # se déplace sur une même colonne, différente ligne
            else:
                print("Mur haut atteint; vous perdez votre tour")
        elif direction == 'd':  # droite
            if self.x < partie.x:
                self.x += 1  # se déplace sur une même ligne, différente colonne
            else:
                print("Mur droite atteint; vous perdez votre tour")
        elif direction == 's':  # bas
            if self.y < partie.y:
                self.y += 1  # se déplace sur une même colonne, différente ligne
            else:
                print("Mur bas atteint: vous perdez votre tour")
        elif direction == 'a':  # gauche
            if self.x > 0:
                self.x -= 1  # se déplace sur une même ligne, différente colonne
            else:
                print("Mur gauche atteint; vous perdez votre tour")
        else:  # demeure à même intersection
            pass

    def teleporter(self, partie, affichage):
        nouveau_x = random.randrange(0, partie.x)
        nouveau_y = random.randrange(0, partie.y)
        if partie.mode == "difficile":
            if affichage.map_visuelle[nouveau_y][nouveau_x] == '-':
                self.x = nouveau_x
                self.y = nouveau_y
                return True
        elif partie.mode == "ordinaire":
            if affichage.map_visuelle[nouveau_y][nouveau_x] == '-':
                self.x = nouveau_x
                self.y = nouveau_y
                # print(f"Position de teleporation : {nouveau_x}, {nouveau_y}")
                # print(f"Position docteur: {self.x}, {self.y}")
                return True
            else:
                print("position de dalek, teleportation a refaire")
        else:  # partie.mode == "facile"
            print(f" Position initial docteur: {self.x}, {self.y}")
            if affichage.map_visuelle[nouveau_y][nouveau_x] == '-':
                # vérifier qu'il n'y a pas de Daleks à proximité de 2 cases minimum
                for i in range(2):
                    proximite = i + 1

                    # VÉRIFICATION VERTICAL (POUR SAVOIR SI DALEKS À PROXIMITÉ) - axe des y

                    if nouveau_y == 0:  # docteur sur première ligne
                        # vérifier 2 lignes vers le bas; aucune vérification vers le haut
                        if affichage.map_visuelle[nouveau_y + proximite][nouveau_x] == 'k':
                            print("Dalek à proximité!")
                            return self.teleporter(partie, affichage)
                            
                    elif nouveau_y == 1:  # docteur sur deuxième ligne
                        # vérifier 1 ligne vers le haut
                        if proximite == 1:
                            if affichage.map_visuelle[nouveau_y - proximite][nouveau_x] == 'k':
                                print("Dalek à proximité!")
                                return self.teleporter(partie, affichage)
                        # vérifier 2 lignes vers le bas
                        if affichage.map_visuelle[nouveau_y + proximite][nouveau_x] == 'k':
                            print("Dalek à proximité!")
                            return self.teleporter(partie, affichage)
                            
                    elif nouveau_y == partie.y - 1:  # docteur sur dernière ligne
                        # vérifier 2 lignes vers le haut
                        if affichage.map_visuelle[nouveau_y - proximite][nouveau_x] == 'k':
                            print("Dalek à proximité!")
                            return self.teleporter(partie, affichage)

                    elif nouveau_y == partie.y - 2: # docteur sur avant-dernière ligne
                        # vérifier 1 ligne vers le bas
                        if proximite == 1:
                            if affichage.map_visuelle[nouveau_y + proximite][nouveau_x] == 'k':
                                print("Dalek à proximité!")
                                return self.teleporter(partie, affichage)
                        # vérifier 2 lignes vers le haut
                        if affichage.map_visuelle[nouveau_y - proximite][nouveau_x] == 'k':
                            print("Dalek à proximité!")
                            return self.teleporter(partie, affichage)
                            
                    else:
                        print(f" Position Y nouvelle de téléportation du docteur:{nouveau_y}")

                        # peut vérifier jusqu'à 2 proximités (2 lignes) vers le haut ET vers le bas
                        if affichage.map_visuelle[nouveau_y - proximite][nouveau_x] == 'k':
                            print("Dalek à proximité!")
                            return self.teleporter(partie, affichage)
                        if affichage.map_visuelle[nouveau_y + proximite][nouveau_x] == 'k':
                            print("Dalek à proximité!")
                            return self.teleporter(partie, affichage)

                    # VÉRIFICATION HORIZONTAL (POUR SAVOIR SI DALEKS À PROXIMITÉ) - axe des x

                    if nouveau_x == 0:  # docteur sur première colonne
                        # vérifier 2 colonne vers la droite; aucune vérification vers la gauche
                        if affichage.map_visuelle[nouveau_y][nouveau_x + proximite] == 'k':
                            print("Dalek à proximité!")
                            return self.teleporter(partie, affichage)
            
                    elif nouveau_x == 1:  # docteur sur deuxième colonne
                        # vérifier 1 colonne à gauche
                        if proximite == 1:
                            if affichage.map_visuelle[nouveau_y][nouveau_x - proximite] == 'k':
                                print("Dalek à proximité!")
                                return self.teleporter(partie, affichage)
                        # vérifier 2 colonnes vers la droite
                        if affichage.map_visuelle[nouveau_y][nouveau_x + proximite] == 'k':
                            print("Dalek à proximité!")
                            return self.teleporter(partie, affichage)
                            
                    elif nouveau_x == partie.x - 1:  # docteur sur dernière colonne
                        # vérifier 2 colonnes vers a gauche
                        if affichage.map_visuelle[nouveau_y][nouveau_x - proximite] == 'k':
                            print("Dalek à proximité!")
                            return self.teleporter(partie, affichage)

                    elif nouveau_x == partie.x - 2: # docteur sur avant-dernière colonnes
                        # vérifier 1 colonnes vers la droite
                        if proximite == 1:
                            if affichage.map_visuelle[nouveau_y][nouveau_x + proximite] == 'k':
                                print("Dalek à proximité!")
                                return self.teleporter(partie, affichage)
                        # vérifier 2 colonnes vers le gauche
                        if affichage.map_visuelle[nouveau_y][nouveau_x - proximite] == 'k':
                            print("Dalek à proximité!")
                            return self.teleporter(partie, affichage)
                                 
                    else:
                        print(f" Position X nouvelle de téléportation du docteur: {nouveau_x}")

                        # peut vérifier jusqu'à 2 proximités (2 colonnes) vers la gauche ET vers la droite
                        if affichage.map_visuelle[nouveau_y][nouveau_x - proximite] == 'k':
                            print("Dalek à proximité!")
                            return self.teleporter(partie, affichage)
                        if affichage.map_visuelle[nouveau_y][nouveau_x + proximite] == 'k':
                            print("Dalek à proximité!")
                            return self.teleporter(partie, affichage)       
            else:
                print("Ne peut pas se téléporter sur un Dalek OU sur un tas de ferraille")
                return self.teleporter(partie, affichage)

        if partie.mode == "ordinaire" or partie.mode == "difficile":
            return self.teleporter(partie, affichage)
        elif partie.mode == "facile":
            self.x = nouveau_x
            self.y = nouveau_y
            print(f" Position final docteur: {self.x}, {self.y}")
            return True               
                
                
    def zapper(self, partie, affichage, daleks):
        # zapper à 8 directions
        # VÉRIFIER SI TOUTES LES DIRECTIONS SONT OCCUPÉES PAR UN DALEK
        # SI CHACUNE DES DIRECTIONS LISTÉES EST OCCUPÉE PAR UN DALEK; TUER DALEK
        # TUER L'OBJET REPRÉSENTANT LE DALEK ET EFFACER LE DALEK PAR SON ID DANS L'AFFICHAGE

        if self.compte_zappeur > 0:
            # ... vérifier les directions à portée immédiate (sur une case)
            # en haut et à gauche (diagonale haut/gauche)
            if affichage.map_visuelle[self.y - 1][self.x - 1] == "k":
                for dalek in daleks:
                    if dalek.y == self.y - 1:
                        if dalek.x == self.x - 1:
                            #del daleks[dalek.id - 1] # supprimer le dalek ici (l'objet)
                            daleks.remove(dalek)
                            partie.score += 5
                            affichage.map_visuelle[self.y - 1][self.x - 1] = "-"
            # en haut
            if affichage.map_visuelle[self.y - 1][self.x] == "k":
                for dalek in daleks:
                    if dalek.y == self.y - 1:
                        if dalek.x == self.x:
                            #del daleks[dalek.id - 1] # supprimer le dalek ici (l'objet)
                            daleks.remove(dalek)
                            partie.score += 5
                            affichage.map_visuelle[self.y - 1][self.x] = "-"
            # en haut et à gauche (diagonale haut/droite)
            if affichage.map_visuelle[self.y - 1][self.x + 1] == "k":
                for dalek in daleks:
                    if dalek.y == self.y - 1:
                        if dalek.x == self.x + 1:
                            #del daleks[dalek.id - 1] # supprimer le dalek ici (l'objet)
                            daleks.remove(dalek)
                            partie.score += 5
                            affichage.map_visuelle[self.y - 1][self.x + 1] = "-"
            # à droite
            if affichage.map_visuelle[self.y][self.x + 1] == "k":
                for dalek in daleks:
                    if dalek.y == self.y:
                        if dalek.x == self.x + 1:
                            # del daleks[dalek.id - 1] # supprimer le dalek ici (l'objet)
                            daleks.remove(dalek)
                            partie.score += 5
                            affichage.map_visuelle[self.y][self.x + 1] = "-"
            # en bas à droite (diagonale bas/droite)
            if affichage.map_visuelle[self.y + 1][self.x + 1] == "k":
                for dalek in daleks:
                    if dalek.y == self.y + 1:
                        if dalek.x == self.x + 1:
                            # del daleks[dalek.id - 1] # supprimer le dalek ici (l'objet)
                            daleks.remove(dalek)
                            partie.score += 5
                            affichage.map_visuelle[self.y + 1][self.x + 1] = "-"
            # en bas
            if affichage.map_visuelle[self.y + 1][self.x] == "k":
                for dalek in daleks:
                    if dalek.y == self.y + 1:
                        if dalek.x == self.x:
                            # del daleks[dalek.id - 1] # supprimer le dalek ici (l'objet)
                            daleks.remove(dalek)
                            partie.score += 5
                            affichage.map_visuelle[self.y + 1][self.x] = "-"
            # en bas à gauche (diagonale bas/gauche)
            if affichage.map_visuelle[self.y + 1][self.x - 1] == "k":
                for dalek in daleks:
                    if dalek.y == self.y + 1:
                        if dalek.x == self.x - 1:
                            #del daleks[dalek.id - 1] # supprimer le dalek ici (l'objet)
                            daleks.remove(dalek)
                            partie.score += 5
                            affichage.map_visuelle[self.y + 1][self.x - 1] = "-"
            # à gauche
            if affichage.map_visuelle[self.y][self.x - 1] == "k":
                for dalek in daleks:
                    if dalek.y == self.y:
                        if dalek.x == self.x - 1:
                            #del daleks[dalek.id - 1] # supprimer le dalek ici (l'objet)
                            daleks.remove(dalek)
                            partie.score += 5
                            affichage.map_visuelle[self.y][self.x - 1] = "-"
        else:
            print("Pas de zappeur disponible!")


        if self.compte_zappeur > 0:
            self.compte_zappeur -= 1
        else:
            self.compte_zappeur == 0
            print("Compte zappeur est déjà à zéro; choisissez une autre option!")
        print(self.compte_zappeur)
        
class Dalek:
    def __init__(self, id):
        self.id = id
        self.vivant = True
        self.x = None
        self.y = None

    # 50% des Daleks se déplaceront sur l'axe vertical, le reste sur l'axe horizontal (selon position Docteur)
    def deplacer_dalek(self, docteur):

        if self.id % 2 == 0:
            if docteur.x > self.x:
                self.x += 1
            elif docteur.x < self.x:
                self.x -= 1
            else:
                if docteur.y > self.y:
                    self.y += 1
                elif docteur.y < self.y:
                    self.y -= 1
        else:
            if docteur.y > self.y:
                self.y += 1
            elif docteur.y < self.y:
                self.y -= 1
            else:
                if docteur.x > self.x:
                    self.x += 1
                elif docteur.x < self.x:
                    self.x -= 1
        print("DALEK initial")
        print(f"{self.id} : {self.x}, {self.y}")


class Ferraille:
    def __init__(self, id):
        self.id = id
        self.x = None
        self.y = None


if __name__ == '__main__':
    c = Controleur()
    bon_traitement = c.afficher_menu_debut()
    if bon_traitement == True:
        c.afficher_menu_jeu()
