import math
import time

import gmpy2
from gmpy2 import mpz
import dill

import matplotlib.pyplot as plt


def newton_raphson_sqrt(n, one) :
    floating_point_precision = 10 ** 16
    n_float = float((n * floating_point_precision) // one) / floating_point_precision
    x = (int(floating_point_precision * math.sqrt(n_float)) * one) // floating_point_precision
    n_one = n * one
    while 1 :
        x_old = x
        x = (x + n_one // x) // 2
        if x == x_old :
            break
    return x


def chudnovsky_bs_pi_decimal_development(digits, base10log = False, save = True) :
    """
    :param base10log: contains true if digits is base 10 log of the number of wanted digits. Default is False
    :type base10log: bool
    :param digits: number of digits wanted
    :type digits: int
    :return: string containing the k first digits of Pi using the
    Chudnovsky Algorithm. This is not the fastest way to converge to Pi but the most efficient to compute,
    see below.
    :rtype: str
    """
    C = 640320
    C3over24 = C ** 3 // 24
    start = time.time()

    def bs_computing(a, b) :
        """
        :param a: lower bound considered
        :type a: int
        :param b: upper bound considered
        :type b: int
        :return: computes the terms for binary splitting the Chudnovsky Infinite Series. (see wikipedia for the series)
        Formulas for Binary Splitting are as follows :
        a(a) = +/- (13591409 + 545140134*a)
        p(a) = (6*a-5)*(2*a-1)*(6*a-1)
        b(a) = 1
        q(a) = a*a*a*C3over24

        Notations and computation taken from https://www.ginac.de/CLN/binsplit.pdf
        :rtype: int
        """
        if b - a == 1 :
            if a == 0 :
                Pab = Qab = 1
            else :
                Pab = (6 * a - 5) * (2 * a - 1) * (6 * a - 1)
                Qab = a * a * a * C3over24
            Tab = Pab * (13591409 + 545140134 * a)

            if a & 1 :
                Tab = - Tab
        else :
            m = (a + b) // 2
            Pam, Qam, Tam = bs_computing(a, m)
            Pmb, Qmb, Tmb = bs_computing(m, b)
            Pab = Pam * Pmb
            Qab = Qam * Qmb
            Tab = Pam * Tmb + Tam * Qmb
        return Pab, Qab, Tab

    # We need to know in advance how many terms to compute for bs_computing to work as we need to be able to compute
    digits_term_ratio = math.log10(C3over24 / 6 / 2 / 6)
    if base10log :
        digits = 10 ** digits
    n = int(digits / digits_term_ratio + 1)
    P, Q, T = bs_computing(0, n)
    one = 10 ** digits
    sqrtC = newton_raphson_sqrt(10005 * one, one)
    pi = (Q * 426880 * sqrtC) // T

    end = time.time()
    duration = end - start

    if save :
        try :
            with open("pi_digits.txt", "r") as f :
                text = f.readlines()

        except :
            text = ["a b 0 2"]

        first_line = text[0].split(" ")
        if int(first_line[2]) <= digits :
            with open("pi_digits.txt", "w") as f :
                str_pi = str(pi)
                pi_string = "3."
                pi_string += str_pi[1 :]
                f.write(f"Pi's first {digits} digits are : \n" + pi_string)
                f.write("\n \n")
                f.write(f"Computed in {duration}s")

    return pi, duration


"""k = int(input("How Many Digits of Pi ? (enter the number or base 10 log of the number)"))
t = str(input("Was the precedent number base 10 log of the wanted number of digits ?")) == "y"

print(chudnovsky_bs_pi_decimal_development(k, t))"""


def chudnovsky_bs_pi_decimal_development_with_gmpy2(digits, base10log = False, save = True) :
    """
    :param base10log: contains true if digits is base 10 log of the number of wanted digits. Default is False
    :type base10log: bool
    :param digits: number of digits wanted
    :type digits: int
    :return: string containing the k first digits of Pi using the
    Chudnovsky Algorithm. This is not the fastest way to converge to Pi but the most efficient to compute,
    see below.
    :rtype: str
    """
    C = 640320
    C3over24 = C ** 3 // 24
    start = time.time()

    def bs_computing(a, b) :
        """
        :param a: lower bound considered
        :type a: int
        :param b: upper bound considered
        :type b: int
        :return: computes the terms for binary splitting the Chudnovsky Infinite Series. (see wikipedia for the series)
        Formulas for Binary Splitting are as follows :
        a(a) = +/- (13591409 + 545140134*a)
        p(a) = (6*a-5)*(2*a-1)*(6*a-1)
        b(a) = 1
        q(a) = a*a*a*C3over24

        Notations and computation taken from https://www.ginac.de/CLN/binsplit.pdf
        :rtype: int
        """
        if b - a == 1 :
            if a == 0 :
                Pab = Qab = mpz(1)
            else :
                Pab = mpz((6 * a - 5) * (2 * a - 1) * (6 * a - 1))
                Qab = mpz(a * a * a * C3over24)
            Tab = Pab * (13591409 + 545140134 * a)

            if a & 1 :
                Tab = - Tab
        else :
            m = (a + b) // 2
            Pam, Qam, Tam = bs_computing(a, m)
            Pmb, Qmb, Tmb = bs_computing(m, b)
            Pab = Pam * Pmb
            Qab = Qam * Qmb
            Tab = Pam * Tmb + Tam * Qmb
        return Pab, Qab, Tab

    # We need to know in advance how many terms to compute for bs_computing to work as we need to be able to compute
    digits_term_ratio = math.log10(C3over24 / 6 / 2 / 6)
    if base10log :
        digits = 10 ** digits
    n = int(digits / digits_term_ratio + 1)
    P, Q, T = bs_computing(0, n)
    one_sqr = mpz(10) ** (2 * digits)
    sqrtC = gmpy2.isqrt(10005 * one_sqr)
    pi = (Q * 426880 * sqrtC) // T
    pi = pi.__int__()

    end = time.time()
    duration = end - start

    with open("pi_digits_gmpy.txt", "wb") as f :
        dill.dump(pi, f)

    return pi, duration


def counter(n : int) -> tuple[dict[int, float], float]:
    freq_dict ={}
    pi, duration = chudnovsky_bs_pi_decimal_development_with_gmpy2(n, False, False)
    for digit in str(pi):
        freq_dict[int(digit)] = freq_dict.get(int(digit), 0) + 1/n
    return freq_dict, duration


def graph():
    durations = []
    durations_gmpy = []
    number = 10**6
    N = []
    for i in range(0, number + 1, 10000):
        print(i)
        N.append(i)
        durations.append(chudnovsky_bs_pi_decimal_development(i, False, False)[1])
        durations_gmpy.append(chudnovsky_bs_pi_decimal_development_with_gmpy2(i, False, False)[1])

    plt.clf()
    plt.plot(N, durations, 'r', label = 'Newton-Raphson Sqrt Method')
    plt.plot(N, durations_gmpy, 'b', label = 'Fast GMPY2 C Sqrt')
    plt.legend()
    plt.xlabel('Number of decimals calculated')
    plt.ylabel('Calculation Time')
    plt.savefig('pi_decimal_development_calctime_comparison.png')

    number = 9
    durations = []
    N = []
    for i in range(number):
        print(i)
        N.append(i)
        durations.append(chudnovsky_bs_pi_decimal_development_with_gmpy2(i, True, False)[1])

    plt.clf()
    plt.plot(N, durations, 'r', label = 'Binary Splitting with GMPY2 Library')
    plt.legend()
    plt.xlabel('Number of decimals calculated')
    plt.ylabel('Calculation Time')
    plt.savefig('pi_decimal_development_calctime_gmpy2.png')



