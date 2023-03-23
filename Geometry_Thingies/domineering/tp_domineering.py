import numpy as np
import random


# Dans tout le TP, on remplacera le joueur 0 par le joueur -1, parce que c'est vachement plus joli.


def grille_vide(p, q) :
    return np.zeros((p, q))


def coups_possibles(v, joueur) :
    result = []
    p, q = len(v), len(v[0])
    if joueur == -1 :
        for i in range(p - 1) :
            for j in range(q) :
                if v[i, j] == 0 and v[i + 1, j] == 0 :
                    result.append((i, j))
    else :
        for i in range(p) :
            for j in range(q - 1) :
                if v[i, j] == 0 and v[i, j + 1] == 0 :
                    result.append((i, j))

    return result


def strategie_aleatoire(v, joueur) :
    return random.choice(coups_possibles(v, joueur))


def placer(v, i, j, joueur) :
    if joueur == -1 :
        v[i, j] = -1
        v[i + 1, j] = -1
    else :
        v[i, j] = 1
        v[i, j + 1] = 1


def retirer(v, i, j, joueur) :
    if joueur == -1 :
        v[i, j] = 0
        v[i + 1, j] = 0
    else :
        v[i, j] = 0
        v[i, j + 1] = 0


def jeu(strategie0, strategie1, p, q) :
    state_list = []
    v = grille_vide(p, q)
    over = False
    joueur = -1
    while not over :
        i, j = p, q
        if joueur < 0 :
            try :
                (i, j) = strategie0(v, joueur)
                state_list.append((-1, i, j))
            except IndexError :
                over = True
                pass
        else :
            try :
                (i, j) = strategie1(v, joueur)
                state_list.append((1, i, j))
            except IndexError :
                over = True
                pass
        if i < p and j < q :
            placer(v, i, j, joueur)
        joueur *= -1
    return state_list, joueur


def statistiques(strategie0, strategie1, p, q, nb_parties) :
    r = np.array([0, 0])
    for _ in range(nb_parties) :
        g = jeu(strategie0, strategie1, p, q)
        if g < 0 :
            r[0] += 1
        else :
            r[1] += 1
    return list(r)


def h1(v) :
    unique, counts = np.unique(v, return_counts = True)
    tiles = dict(zip(unique, counts))
    a, b = len(coups_possibles(v, -1)), len(coups_possibles(v, 1))

    if tiles.get(-1, 0) <= tiles.get(1, 0) :
        if a == 0 :
            return float("-inf")
        return a - b
    else :
        if b == 0 :
            return float("inf")
        return a - b


def minmax(v, joueur, profondeur, h):
    coups = coups_possibles(v, joueur)
    if profondeur == 0 or not coups :
        return h(v), None
    else :
        if joueur == -1 :
            best, pos = float("-inf"), (-1, -1)
            for coup in coups :
                placer(v, coup[0], coup[1], joueur)
                val, suite = minmax(v, -joueur, profondeur - 1, h)
                if val > best :
                    best, pos = val, coup
                retirer(v, coup[0], coup[1], joueur)
            return best, pos
        else :
            best, pos = float("inf"), (-1, -1)
            for coup in coups:
                placer(v, coup[0], coup[1], joueur)
                val, suite = minmax(v, -joueur, profondeur - 1, h)
                if val < best :
                    best, pos = val, coup
                retirer(v, coup[0], coup[1], joueur)
            return best, pos


def strategie_minmax(v, joueur):
    return minmax(v, joueur, 2, h1)[1]
