from manim import *
import tp_domineering


def state_list(strategie0, strategie1, p, q) :
    return tp_domineering.jeu(strategie0, strategie1, p, q)


p, q = 3, 4
config_list, gagnant = state_list(tp_domineering.strategie_aleatoire, tp_domineering.strategie_minmax, p, q)


class Domineering(Scene) :
    def construct(self) :
        start_row = -p / 2 - 1/2
        start_column = q / 2
        size = 2
        square = Square(size).set_color(WHITE).move_to([start_row, start_column, 0.], aligned_edge = [1, 0, 0])
        self.add(square)
        for i in range(1, q) :
            square = Square(size).set_color(WHITE).next_to(square, RIGHT, buff = 0)
            self.add(square)

        for row in range(1, p) :
            square = Square(size).set_color(WHITE).next_to(square, DOWN, buff = 0)
            self.add(square)
            for i in range(1, q) :
                if row % 2 != 1 :
                    square = Square(size).set_color(WHITE).next_to(square, RIGHT, buff = 0)
                    self.add(square)
                else :
                    square = Square(size).set_color(WHITE).next_to(square, LEFT, buff = 0)
                    self.add(square)

        for coup in config_list :
            joueur, i, j = coup
            # print(joueur, i, j)
            if joueur < 0 :
                rect = RoundedRectangle(corner_radius = 0.2, height = 1.95 * size, width = 0.95 * size).set_fill(PURPLE,
                    opacity = 0.7).set_color(PURPLE)
                rect.next_to([start_row - size / 2, start_column - 0.025 * size + size / 2, 0],
                             aligned_edge = [1, 1, 0], buff = 0.01)
            else :
                rect = RoundedRectangle(corner_radius = 0.2, height = 0.95 * size, width = 1.95 * size).set_fill(GREEN_D,
                    opacity = 0.7).set_color(GREEN_D)
                rect.next_to([start_row , start_column - 0.025 * size + size / 2, 0],
                             aligned_edge = [1, 1, 0], buff = 0.01)
            """
            self.add(rect)
            break"""

            self.play(FadeIn(rect))
            self.wait(0.2)
            if j != 0 :
                self.play(rect.animate.shift(RIGHT * size * j))
                self.wait(0.2)
            if i != 0 :
                self.play(rect.animate.shift(DOWN * size * i))
                self.wait(0.2)

        if gagnant < 0 :
            couleur_gagnante = "Violet"
            couleur = PURPLE
        else :
            couleur_gagnante = "Vert"
            couleur = GREEN_D
        resultat = Text(f"Le Joueur {couleur_gagnante} a gagné", stroke_color = BLACK, stroke_width = 0.5, stroke_opacity = 0.9, color = couleur, opacity = 1)
        rect = Rectangle(width = 4 * size, height = size).set_fill(LIGHT_GRAY, opacity = 1)
        self.play(Create(rect))
        self.play(Write(resultat))
        self.wait(2)
        self.clear()


