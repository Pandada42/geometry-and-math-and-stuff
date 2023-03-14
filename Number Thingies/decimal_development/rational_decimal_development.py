import numpy as np
import matplotlib.pyplot as plt
from colour import Color


def binary_gcd(u, v) :
    if u == 0 :
        return v
    elif v == 0 :
        return u
    elif u % 2 == v % 2 == 0 :
        return 2 * binary_gcd(u // 2, v // 2)
    elif u % 2 == 0 :
        return binary_gcd(u // 2, v)
    elif v % 2 == 0 :
        return binary_gcd(u, v // 2)
    else :
        return binary_gcd(abs(u - v), min(u, v))


def decimal_development(n: int) :
    if n == 0 :
        return ZeroDivisionError
    if n == 1 :
        return [], 0
    development = []
    foo = 1
    while not development or (foo != 1 and foo != 0) :
        foo *= 10
        development.append(foo//n)
        foo = foo % n
    period = len(development) if foo != 0 else 0
    return development, period


print(decimal_development(7))


def rational_decimal_development(p, q) :
    integer_part = [p // q]
    a, period = decimal_development(q)
    fractionary_part = (p % q) * a
    return integer_part + fractionary_part, period


class Rational :
    def __init__(self, p, q) :
        if q == 0 :
            pass
        else :
            m = binary_gcd(p, q)
            p, q = p // m, q // m
            self.numerator = p
            self.denominator = q

        self.decimal_development, self.periods = rational_decimal_development(p, q)

    def __str__(self):
        foo = f"{self.numerator}/{self.denominator} || {self.decimal_development[0]}."
        for i in self.decimal_development[1:]:
            foo += f"{i}"
        foo += f", Period = {self.periods}"
        return foo


def isPrime(p):
    n = int(np.sqrt(p)) + 1
    for i in range(2, n):
        if p % i == 0 : return False
    return True


number = 1000000
rational_dict = {}
prime_dict = {}
for i in range(1, number):
    if i % 100 == 0 :
        print(i)
    # rational_dict[i] = Rational(1, i)
    if isPrime(i) :
        prime_dict[i] = decimal_development(i)[1]
"""
N = [i for i in range(number)]
rationals_periods = [rational_dict[i].periods for i in rational_dict]

plt.clf()
plt.bar(N, rationals_periods, label = f"Periode du développement décimal des inverses des entiers jusqu'à {number}")
plt.xlabel("Nombres Entiers")
plt.ylabel("Période du développement décimal de 1/n")
plt.legend()
plt.savefig("periode_developpement_decimal_inverses_entiers.png")
"""

P = [p for p in prime_dict]
N = [_ for _ in range(len(P))]
prime_periods = [prime_dict[P[n]] for n in N]
plt.clf()
plt.bar(P, prime_periods)
red = Color("red")
colors = list(red.range_to(Color("purple"), 5))
for k in range(1, 6):
    T_k = [(p-1)/k for p in P]
    plt.plot(P, T_k, colors[k - 1].hex)
plt.xlabel("Nombres Entiers")
plt.ylabel("Période du développement \n décimal de 1/n si p est premier")
plt.title(f"Periode du développement décimal \n des inverses des entiers premiers jusqu'à {number}")
plt.savefig("periode_developpement_decimal_inverses_premiers.png")

plt.clf()
plt.bar(N, prime_periods)
for k in range(1, 6) :
    T_k = [(P[n] - 1) / k for n in N]
    plt.plot(N, T_k, colors[k - 1].hex)
plt.xlabel("k-ème Nombre Premier")
plt.ylabel("Période du développement \n décimal de 1/P_n")
plt.title(f"Periode du développement décimal \n des inverses des entiers premiers jusqu'à {number}")
plt.savefig("periode_developpement_decimal_inverses_premiers_par_indice.png")