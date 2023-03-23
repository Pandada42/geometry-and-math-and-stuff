import functools

import matplotlib.animation
import matplotlib.pyplot as plt
import numpy as np
import random as rd

n = 3
k = 1000


def point_generator(number):
    thetas = np.array([0. for _ in range(number)])
    for i in range(number):
        thetas[i] = (rd.uniform(thetas[i-1], 2 * np.pi))

    return thetas, rd.uniform(0, 1)


def update(thetas, a):

    def f(x, y):
        return a*x + (1-a) * y

    n_thetas = np.zeros_like(thetas)
    for i in range(len(thetas)):
        n_thetas[i-1] = f(thetas[i-1], thetas[i])

    return n_thetas


def polygon_arrays(number, iterations):
    diagonalley = np.array([np.array([0. for _ in range(number)]) for _ in range(iterations)])
    diagonalley[0], a = point_generator(number)
    for i in range(1, iterations):
        diagonalley[i] = update(diagonalley[i-1], a)
    return np.array([[(np.cos(u), np.sin(u)) for u in thetas] for thetas in diagonalley])


def polygon(coordinates):
    lines = []



def animator(number, iterations):
    fig = plt.figure()
    fig.xlim = (-1.01, 1.01)
    fig.ylim = (-1.01, 1.01)
    plt.Circle((0., 0.), 1, fc = 'None', edgecolor = 'black')
    polygons = polygon_arrays(number, iterations)
    previous = plt.plot(polygon([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]))
    for polygon in polygons:
        previous.remove()
        # x_values = [point[0] for point in polygon]
        # y_values = [point[1] for point in polygon]
        previous = plt.plot(polygon)


animator(3, 10)
