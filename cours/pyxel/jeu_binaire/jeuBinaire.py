import pyxel
import random
import time

class JeuBinaire:
    def __init__(self):
        pyxel.init(300, 200, title="Jeu Binaire + Shoot'em up")
        self.reset_jeu()
        pyxel.run(self.update, self.draw)

    def reset_jeu(self):
        self.etat = "binaire"  # binaire | shoot | fini
        self.score = 0
        self.essai = 0
        self.max_essais = 5
        self.reset_binaire()
        self.reset_shoot()

    def reset_binaire(self):
        self.valeur = random.randint(0, 255)
        self.binaire = format(self.valeur, '08b')
        self.poids = [2 ** i for i in range(8)]
        self.reponses = ['' for _ in range(8)]
        self.curseur = 0
        self.message = ""
        self.termine = False
        self.start_time = time.time()

    def reset_shoot(self):
        self.vaisseau_x = 140
        self.balles = []
        self.ennemis = []
        self.shoot_start = 0
        self.shoot_duration = 30  # secondes

    def update(self):
        if self.etat == "binaire":
            self.update_binaire()
        elif self.etat == "shoot":
            self.update_shoot()

    def update_binaire(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            if not self.termine:
                self.verifier()
            else:
                self.essai += 1
                if self.essai >= self.max_essais:
                    self.etat = "fini"
                else:
                    self.reset_shoot()
                    self.shoot_start = time.time()
                    self.etat = "shoot"

        elif pyxel.btnp(pyxel.KEY_BACKSPACE):
            if len(self.reponses[self.curseur]) > 0:
                self.reponses[self.curseur] = self.reponses[self.curseur][:-1]

        elif pyxel.btnp(pyxel.KEY_LEFT) and self.curseur > 0:
            self.curseur -= 1

        elif pyxel.btnp(pyxel.KEY_RIGHT) and self.curseur < 7:
            self.curseur += 1

        for key in range(pyxel.KEY_0, pyxel.KEY_9 + 1):
            if pyxel.btnp(key):
                chiffre = chr(key)
                self.reponses[self.curseur] += chiffre

    def verifier(self):
        try:
            total = sum(int(rep) if rep.strip() != '' else 0 for rep in self.reponses)
        except ValueError:
            self.message = "Erreur de saisie !"
            return

        if total == self.valeur:
            t = int(time.time() - self.start_time)
            points = max(20 - t, 1)
            self.message = f"✅ {self.valeur} Bravo ! +{points} pts"
            self.score += points
        else:
            self.message = f"❌ Mauvais ! Somme: {total}, attendu: {self.valeur}"
        self.termine = True

    def update_shoot(self):
        now = time.time()
        if now - self.shoot_start >= self.shoot_duration:
            self.reset_binaire()
            self.etat = "binaire"
            return

        # Déplacement vaisseau
        if pyxel.btn(pyxel.KEY_LEFT):
            self.vaisseau_x = max(0, self.vaisseau_x - 2)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.vaisseau_x = min(300 - 8, self.vaisseau_x + 2)

        # Tir
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.balles.append([self.vaisseau_x + 3, 180])

        # Déplacer balles
        self.balles = [[x, y - 4] for x, y in self.balles if y > 0]

        # Ajouter ennemis
        if random.random() < 0.05:
            self.ennemis.append([random.randint(0, 292), 0])

        # Déplacer ennemis
        self.ennemis = [[x, y + 2] for x, y in self.ennemis if y < 200]

        # Collision
        new_balles = []
        for bx, by in self.balles:
            touche = False
            for e in self.ennemis:
                if abs(bx - e[0]) < 8 and abs(by - e[1]) < 8:
                    self.ennemis.remove(e)
                    self.score += 1
                    touche = True
                    break
            if not touche:
                new_balles.append([bx, by])
        self.balles = new_balles

    def draw(self):
        pyxel.cls(0)
        if self.etat == "binaire":
            self.draw_binaire()
        elif self.etat == "shoot":
            self.draw_shoot()
        else:
            pyxel.text(100, 90, f"🏁 Fin du jeu ! Score : {self.score}", 10)
            pyxel.text(90, 110, "Appuie sur DEL pour rejouer", 7)
            if pyxel.btnp(pyxel.KEY_DELETE):
                self.reset_jeu()

    def draw_binaire(self):
        pyxel.text(10, 10, f"Essai {self.essai + 1}/{self.max_essais}  Score: {self.score}", 7)
        pyxel.text(10, 20, f"Nombre binaire : {self.binaire}", 7)
        pyxel.text(10, 30, "(bit faible à droite)", 5)

        for i in range(8):
            x = 10 + i * 35
            y = 60
            pyxel.rect(x - 2, y - 2, 30, 20, 1)
            pyxel.text(x, y, self.reponses[i], 7)
            if i == self.curseur:
                pyxel.rectb(x - 4, y - 4, 34, 24, 10)
            pyxel.text(x, y + 20, f"{self.poids[7 - i]}", 13)

        pyxel.text(10, 120, self.message, 11)

    def draw_shoot(self):
        pyxel.text(10, 10, "🚀 SHOOT 'EM UP ! SPACE = tir, ←/→ = bouger", 7)
        pyxel.text(10, 20, f"Score: {self.score}", 11)

        # Vaisseau
        pyxel.rect(self.vaisseau_x, 180, 8, 8, 9)

        # Balles
        for x, y in self.balles:
            pyxel.rect(x, y, 2, 4, 7)

        # Ennemis
        for x, y in self.ennemis:
            pyxel.rect(x, y, 8, 8, 8)

if __name__ == "__main__":
    JeuBinaire()