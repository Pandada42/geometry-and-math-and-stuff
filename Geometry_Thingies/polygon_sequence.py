from manim import *
import numpy as np
import random as rd


def is_regular(angle_list):
    difference_list = np.array([angle_list[i] - angle_list[i-1] for i in range(len(angle_list))])
    return difference_list.std() <= 0.5


def points(angle_list, r):
    p = np.array([[0., 0., 0.] for _ in angle_list])
    for i in range(len(angle_list)):
        angle = angle_list[i]
        p[i] = [r * np.cos(angle), r * np.sin(angle), 0.]
    return p


def update(angle_list, param):
    next_list = np.zeros_like(angle_list)
    for i in range(len(angle_list) - 1):
        next_list[i] = angle_list[i] + param * (angle_list[i + 1] - angle_list[i])
    next_list[-1] = angle_list[-1] + param * (angle_list[0] - angle_list[-1] + 2 * np.pi)
    next_list = np.mod(next_list, (2 * np.pi))
    return next_list


n = 3
alpha = 1/2
thetas = np.zeros(n)
radius = 2
max_k = 500
regular = True
while regular :
    thetas[-1] = 0
    for o in range(n):
        thetas[o] = rd.uniform(thetas[o-1], 2*np.pi)
    regular = is_regular(thetas)


cur_thetas = thetas
k = 0
print(cur_thetas)
while not is_regular(cur_thetas) and k <= max_k :
    next_thetas = update(cur_thetas, alpha)
    print(next_thetas)
    k += 1
    cur_thetas = next_thetas


class PolygonSequence(Scene):
    def construct(self):
        self.add(Circle(radius))
        vertices = points(thetas, radius)
        cur_poly = Polygon(*vertices)
        self.play(Create(cur_poly))
        k = 0
        counter_text = Text("Current Step Number : ").move_to([-3.9, 3, 0.])
        self.play(FadeIn(counter_text))
        alpha_prompt = Text(f"Alpha Value : {round(alpha, 3)}").move_to([-4.5, 2.35, 0.])
        self.play(FadeIn(alpha_prompt))
        cur_counter = Text("0").move_to([0., 3, 0.])
        self.play(FadeIn(cur_counter))
        cur_thetas = thetas
        while not is_regular(cur_thetas) and k <= max_k:
            next_thetas = update(cur_thetas, alpha)
            next_poly = Polygon(*points(sorted(next_thetas), radius))
            k += 1
            next_counter = Text(f"{k}").move_to([0., 3, 0.])
            self.wait(0.05)
            self.play(Transform(cur_counter, next_counter, run_time = 0.01))
            self.play(Transform(cur_poly, next_poly, run_time = 0.1))
            cur_thetas = next_thetas













