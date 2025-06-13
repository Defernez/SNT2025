import pyxel

class LogicGateSimulator:
    def __init__(self):
        self.input_a = 0
        self.input_b = 0
        self.selected_gate = 0  # index dans la liste des portes

        self.gates = [
            ("ET", lambda a, b: a & b),
            ("OU", lambda a, b: a | b),
            ("NON A", lambda a, b: 1 - a),
            ("NON B", lambda a, b: 1 - b),
            ("NAND", lambda a, b: 1 - (a & b)),
            ("NOR", lambda a, b: 1 - (a | b)),
            ("XOR", lambda a, b: a ^ b),
        ]

        pyxel.init(200, 150, title="Portes Logiques - Clavier + Affichage")
        pyxel.mouse(False)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_A):
            self.input_a ^= 1

        if pyxel.btnp(pyxel.KEY_B):
            self.input_b ^= 1

        if pyxel.btnp(pyxel.KEY_SPACE):
            self.selected_gate = (self.selected_gate + 1) % len(self.gates)

    def draw_gate_icon(self, name, x, y):
        # Dessin ASCII simplifié de porte logique
        pyxel.rect(x, y, 60, 30, 1)
        pyxel.text(x + 3, y + 3, name, 7)
        pyxel.line(x - 10, y + 8, x, y + 8, 7)   # Entrée gauche 1
        pyxel.line(x - 10, y + 22, x, y + 22, 7) # Entrée gauche 2
        pyxel.line(x + 60, y + 15, x + 70, y + 15, 8) # Sortie droite

    def draw(self):
        pyxel.cls(0)
        pyxel.text(5, 2, "A: toggle A | B: toggle B | ESPACE: changer porte", 6)

        # Affiche entrées A et B
        pyxel.text(10, 20, f"A = {self.input_a}", 7)
        pyxel.text(10, 30, f"B = {self.input_b}", 7)

        # Affiche porte sélectionnée
        name, func = self.gates[self.selected_gate]
        result = func(self.input_a, self.input_b)
        pyxel.text(10, 50, f"Porte: {name}", 10)
        pyxel.text(10, 60, f"Resultat: {result}", 11)

        # Dessin de la porte logique
        self.draw_gate_icon(name, 100, 40)

# Lancement du simulateur
LogicGateSimulator()