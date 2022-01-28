import random
import sys
from Affichage import Affichage

class Controleur:
    def __init__(self):
        self.vue = Affichage()
        self.modele = Jeu(self.vue, self)

    def verifier_compte_daleks(self):
        compte_daleks = len(self.modele.partie_courante.dalek)
        if compte_daleks == 0:
            self.modele.partie_courante.niveau += 1
            for k in self.modele.partie_courante.dalek:
                self.modele.partie_courante.dalek.remove(k)
            for f in self.modele.partie_courante.ferrailles:
                self.modele.partie_courante.ferrailles.remove(f)
            self.vue.map_visuelle = []
            compte_zappeur_actuel_docteur = self.modele.partie_courante.docteur.compte_zappeur
            compte_zappeur_actuel_docteur += 1
            self.modele.partie_courante.creer_aire_jeu(self.vue)
            self.modele.partie_courante.creer_docteur()
            self.modele.partie_courante.creer_dalek()
            self.vue.demarrer_partie(self.modele.partie_courante)
            return True
        return False

    def verifier_si_defaite(self):
        liste_daleks = self.modele.partie_courante.dalek
        docteur = self.modele.partie_courante.docteur
        for k in liste_daleks:
            if k.y == docteur.y:
                if k.x == docteur.x:
                    self.vue.afficher_aire_jeu()
                    print('''
-   -   -   -   =   =   -   -   -   -
G   A   M   E           O   V   E   R
-   -   -   -   =   =   -   -   -   -
''')
                    return True
        return False

class Jeu:
    def __init__(self, affichage, controleur):
        self.partie_courante = Partie(affichage, controleur)

class Partie:
    def __init__(self, affichage, controleur):
        self.niveau = 1
        self.score = 0
        self.mode = None
        self.x = 16
        self.y = 16
        self.docteur = None
        self.dalek = []
        self.ferrailles = []

    def afficher_menu_debut(self, affichage):
        reponse_valide = {
            '1': "facile",
            '2': "ordinaire",
            '3': "difficile"
        }
        reponse = affichage.afficher_menu_debut()
        if reponse in reponse_valide.keys():
            self.mode = reponse_valide[reponse]
            self.creer_aire_jeu(affichage)
            self.creer_docteur()
            self.creer_dalek()
            affichage.demarrer_partie(self)
            return True
        else:
            print('''
--- Votre réponse est invalide ---
''')
            affichage.afficher_aire_jeu()
            self.afficher_menu_debut()

    def creer_aire_jeu(self, affichage):
        map_visuelle = []
        for ligne in range(self.y):
            ligne = []
            for case in range(self.x):
                case = '-'
                ligne.append(case)
            map_visuelle.append(ligne)
        affichage.map_visuelle = map_visuelle
        return map_visuelle

    def creer_docteur(self):
        self.docteur = Docteur(self)

    def creer_dalek(self):
        if self.niveau == 1:
            for i in range(5):
                self.dalek.append(Dalek(i+1))
        elif self.niveau == 2:
            for i in range(10):
                self.dalek.append(Dalek(i+1))
        elif self.niveau == 3:
            for i in range(15):
                self.dalek.append(Dalek(i+1))
        elif self.niveau == 4:
            for i in range(20):
                self.dalek.append(Dalek(i+1))
        elif self.niveau == 5:
            for i in range(25):
                self.dalek.append(Dalek(i+1))
        else:
            print("Vous avez surmonté tous les niveaux et gagné le jeu, 🏆")

    def afficher_menu_jeu(self, affichage, controleur):
        reponse = affichage.afficher_menu_jeu()

        if reponse in "wdsae":
            if self.tas_ferraille_est_devant_docteur(affichage, reponse):
                self.docteur.deplacer_docteur(reponse, self)
                affichage.effacer_position_precedente_docteur()
                affichage.positionner_docteur(self)
                for k in self.dalek:
                    k.deplacer_dalek(self.docteur)
                affichage.effacer_position_precedente_dalek()
                self.positionner_dalek(affichage)
            else:
                print("Le docteur ne peut pas se déplacer sur une intersection occupée par un tas de ferraille")
                affichage.afficher_aire_jeu()
                self.afficher_menu_jeu(affichage, controleur)
                return
        elif reponse == "t":
            self.docteur.teleporter(self, affichage)
            affichage.effacer_position_precedente_docteur()
            affichage.positionner_docteur(self)
            for k in self.dalek:
                k.deplacer_dalek(self.docteur)
            affichage.effacer_position_precedente_dalek()
            self.positionner_dalek(affichage)
        elif reponse == "z":
            self.docteur.zapper(self, affichage, self.dalek)
            for k in self.dalek:
                k.deplacer_dalek(self)
            affichage.effacer_position_precedente_dalek()
            self.positionner_dalek(affichage)
        elif reponse == "q":
            reponse = self.afficher_menu_stats(affichage)
            if reponse == 'back':
                affichage.afficher_aire_jeu()
                self.afficher_menu_jeu(affichage, controleur)
                return
        elif reponse == "r":
            affichage.afficher_reinit_jeu()
            affichage.map_visuelle = []
            controleur.modele = None
            del controleur.modele
            bon_traitement = self.afficher_menu_debut()
            if bon_traitement == True:
                self.afficher_menu_jeu(affichage, controleur)
            return
            
        else:
            print("--- Votre réponse est invalide ---")
            affichage.afficher_aire_jeu()
            self.afficher_menu_jeu(affichage, controleur)
            return

        monter_de_niveau = controleur.verifier_compte_daleks()
        partie_termine = controleur.verifier_si_defaite()
        if not monter_de_niveau and not partie_termine:
            affichage.afficher_aire_jeu()
        if not partie_termine:
            self.afficher_menu_jeu(affichage, controleur)

# il ne peux pas verifier en dehors de la matrice
# ferraille ne meur pas tous en cas de colision de plus de 2
# des Dalek invisibles
# des deplacements vers le bas et droite bugger apres le mur
    def tas_ferraille_est_devant_docteur(self, affichage, direction):
        if direction == 'w':
            if affichage.map_visuelle[self.docteur.y - 1][self.docteur.x] == 'f':
                return False
        elif direction == 'd':
            # if affichage.map_visuelle[self.docteur.y][self.docteur.x + 1] == 'f' and self.docteur.x != self.x - 1:
            #     return False
            # elif affichage.map_visuelle[self.docteur.y][self.docteur.x] == 'f' and self.docteur.x == self.x - 1:
            #     return False
            
            if affichage.map_visuelle[self.docteur.y][self.docteur.x + 1] == 'f':
                return False
        elif direction == 's':
            if affichage.map_visuelle[self.docteur.y + 1][self.docteur.x] == 'f':
                return False
        elif direction == 'a':
            if affichage.map_visuelle[self.docteur.y][self.docteur.x - 1] == 'f':
                return False
        else:
            pass
        return True

    def positionner_dalek(self, affichage):
        for k in self.dalek:
            if affichage.map_visuelle[k.y][k.x] == '-':
                affichage.positionner_dalek(k)
            elif affichage.map_visuelle[k.y][k.x] == 'k':
                collision_x = k.x
                collision_y = k.y
                self.dalek.remove(k)
                for k2 in self.dalek:
                    if k2.y == collision_y and k2.x == collision_x:
                        self.dalek.remove(k2)
                        # for k3 in self.dalek:
                        #     if k3.y == collision_y and k3.x == collision_x:
                        #         self.dalek.remove(k3)
                nouveau_tas_ferraille = Ferraille(len(self.ferrailles) + 1)
                nouveau_tas_ferraille.x = collision_x
                nouveau_tas_ferraille.y = collision_y
                self.ferrailles.append(nouveau_tas_ferraille)
                affichage.positionner_tas_ferraille(nouveau_tas_ferraille)
                self.score += 10
            elif affichage.map_visuelle[k.y][k.x] == 'f':
                self.dalek.remove(k)
                self.score += 5

    def afficher_menu_stats(self, affichage):
        return affichage.afficher_menu_stats(self)

class Docteur:
    def __init__(self, partie, compte_zappeur = 1):
        self.vivant = True
        self.nom = "Who"
        self.x = (round(partie.x / 2)) -1
        self.y = (round(partie.y / 2)) -1
        self.compte_zappeur = compte_zappeur 

    def deplacer_docteur(self, direction, partie):
        if direction == 'w':
            if self.y > 0:
                self.y -= 1
            else:
                print("Limite supérieur de la matrice atteint; tour perdu")
        elif direction == 'd':
            if self.x < partie.x - 1:
                self.x += 1
            else:
                print("Limite droite de la matrice atteinte; tour perdu")
        elif direction == 's':
            if self.y < partie.y - 1:
                self.y += 1
            else:
                print("Limite inférieure de la matrice atteinte; tour perdu")
        elif direction == 'a':
            if self.x > 0:
                self.x -= 1
            else:
                print("Limite gauche de la matrice atteinte; tour perdu")
        else:
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
                return True
            else:
                print("Le docteur ne peut pas se positionner sur un Dalek")
        else:
            if affichage.map_visuelle[nouveau_y][nouveau_x] == '-':
                for i in range(2):
                    proximite = i + 1
                    if nouveau_y == 0:
                        if affichage.map_visuelle[nouveau_y + proximite][nouveau_x] == 'k':
                            return self.teleporter(partie, affichage)
                    elif nouveau_y == 1:  
                        if proximite == 1:
                            if affichage.map_visuelle[nouveau_y - proximite][nouveau_x] == 'k':
                                return self.teleporter(partie, affichage)
                        if affichage.map_visuelle[nouveau_y + proximite][nouveau_x] == 'k':
                            return self.teleporter(partie, affichage)
                    elif nouveau_y == partie.y - 1:
                        if affichage.map_visuelle[nouveau_y - proximite][nouveau_x] == 'k':
                            return self.teleporter(partie, affichage)
                    elif nouveau_y == partie.y - 2:
                        if proximite == 1:
                            if affichage.map_visuelle[nouveau_y + proximite][nouveau_x] == 'k':
                                return self.teleporter(partie, affichage)
                        if affichage.map_visuelle[nouveau_y - proximite][nouveau_x] == 'k':
                            return self.teleporter(partie, affichage)
                    else:
                        if affichage.map_visuelle[nouveau_y - proximite][nouveau_x] == 'k':
                            return self.teleporter(partie, affichage)
                        if affichage.map_visuelle[nouveau_y + proximite][nouveau_x] == 'k':
                            return self.teleporter(partie, affichage)

                    if nouveau_x == 0:
                        if affichage.map_visuelle[nouveau_y][nouveau_x + proximite] == 'k':
                            return self.teleporter(partie, affichage)
                    elif nouveau_x == 1:
                        if proximite == 1:
                            if affichage.map_visuelle[nouveau_y][nouveau_x - proximite] == 'k':
                                return self.teleporter(partie, affichage)
                        if affichage.map_visuelle[nouveau_y][nouveau_x + proximite] == 'k':
                            return self.teleporter(partie, affichage)
                    elif nouveau_x == partie.x - 1:
                        if affichage.map_visuelle[nouveau_y][nouveau_x - proximite] == 'k':
                            return self.teleporter(partie, affichage)
                    elif nouveau_x == partie.x - 2:
                        if proximite == 1:
                            if affichage.map_visuelle[nouveau_y][nouveau_x + proximite] == 'k':
                                return self.teleporter(partie, affichage)
                        if affichage.map_visuelle[nouveau_y][nouveau_x - proximite] == 'k':
                            return self.teleporter(partie, affichage)
                    else:
                        if affichage.map_visuelle[nouveau_y][nouveau_x - proximite] == 'k':
                            return self.teleporter(partie, affichage)
                        if affichage.map_visuelle[nouveau_y][nouveau_x + proximite] == 'k':
                            return self.teleporter(partie, affichage)       
            else:
                return self.teleporter(partie, affichage)

        if partie.mode == "ordinaire" or partie.mode == "difficile":
            return self.teleporter(partie, affichage)
        elif partie.mode == "facile":
            self.x = nouveau_x
            self.y = nouveau_y
            return True               
                
    def zapper(self, partie, affichage, daleks):
        if self.compte_zappeur > 0:
            if affichage.map_visuelle[self.y - 1][self.x - 1] == "k":
                for dalek in daleks:
                    if dalek.y == self.y - 1:
                        if dalek.x == self.x - 1:
                            daleks.remove(dalek)
                            partie.score += 5
                            affichage.map_visuelle[self.y - 1][self.x - 1] = "-"
            if affichage.map_visuelle[self.y - 1][self.x] == "k":
                for dalek in daleks:
                    if dalek.y == self.y - 1:
                        if dalek.x == self.x:
                            daleks.remove(dalek)
                            partie.score += 5
                            affichage.map_visuelle[self.y - 1][self.x] = "-"
            if affichage.map_visuelle[self.y - 1][self.x + 1] == "k":
                for dalek in daleks:
                    if dalek.y == self.y - 1:
                        if dalek.x == self.x + 1:
                            daleks.remove(dalek)
                            partie.score += 5
                            affichage.map_visuelle[self.y - 1][self.x + 1] = "-"
            if affichage.map_visuelle[self.y][self.x + 1] == "k":
                for dalek in daleks:
                    if dalek.y == self.y:
                        if dalek.x == self.x + 1:
                            daleks.remove(dalek)
                            partie.score += 5
                            affichage.map_visuelle[self.y][self.x + 1] = "-"
            if affichage.map_visuelle[self.y + 1][self.x + 1] == "k":
                for dalek in daleks:
                    if dalek.y == self.y + 1:
                        if dalek.x == self.x + 1:
                            daleks.remove(dalek)
                            partie.score += 5
                            affichage.map_visuelle[self.y + 1][self.x + 1] = "-"
            if affichage.map_visuelle[self.y + 1][self.x] == "k":
                for dalek in daleks:
                    if dalek.y == self.y + 1:
                        if dalek.x == self.x:
                            daleks.remove(dalek)
                            partie.score += 5
                            affichage.map_visuelle[self.y + 1][self.x] = "-"
            if affichage.map_visuelle[self.y + 1][self.x - 1] == "k":
                for dalek in daleks:
                    if dalek.y == self.y + 1:
                        if dalek.x == self.x - 1:
                            daleks.remove(dalek)
                            partie.score += 5
                            affichage.map_visuelle[self.y + 1][self.x - 1] = "-"
            if affichage.map_visuelle[self.y][self.x - 1] == "k":
                for dalek in daleks:
                    if dalek.y == self.y:
                        if dalek.x == self.x - 1:
                            daleks.remove(dalek)
                            partie.score += 5
                            affichage.map_visuelle[self.y][self.x - 1] = "-"
        else:
            print("Pas de zappeur disponible pour le docteur Who!")


        if self.compte_zappeur > 0:
            self.compte_zappeur -= 1
        else:
            self.compte_zappeur == 0
            print("Compte zappeur est déjà à zéro; vous devez choisir une autre option!")
        
class Dalek:
    def __init__(self, id):
        self.id = id
        self.vivant = True
        self.x = None
        self.y = None

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

class Ferraille:
    def __init__(self, id):
        self.id = id
        self.x = None
        self.y = None


if __name__ == '__main__':
    c = Controleur()
    vue = c.vue
    bon_traitement = c.modele.partie_courante.afficher_menu_debut(vue)
    if bon_traitement == True:
        c.modele.partie_courante.afficher_menu_jeu(vue, c)