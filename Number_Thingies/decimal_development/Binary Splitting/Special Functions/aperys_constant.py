import math
import sys
import time

sys.setrecursionlimit(10000)


def apery_constant(digits: int, base10log = True, save = True) :
    start = time.time()

    def bs_computing(a, b) :
        """
        :param a: lower bound considered
        :type a: int
        :param b: upper bound considered
        :type b: int
        :return: computes the terms for binary splitting the Chudnovsky Infinite Series. (see wikipedia for the series)
        Formulas for Binary Splitting are as follows :
        a(a) = 205a^2 + 250a + 77
        p(0) = 1
        p(a) = a**5
        b(a) = 1
        q(a) = 32 * (2a+1)^5

        Notations and computation taken from https://www.ginac.de/CLN/binsplit.pdf
        :rtype: int
        """
        if b - a == 1 :
            if a == 0 :
                Pab = Qab = 1
            else :
                Pab = a ** 5 if a > 0 else 1
                Qab = 32 * (2 * a + 1) ** 5
            Tab = ((-1) ** a) * Pab * (205 * (a ** 2) + 250 * a + 77)

        else :
            m = (a + b) // 2
            Pam, Qam, Tam = bs_computing(a, m)
            Pmb, Qmb, Tmb = bs_computing(m, b)
            Pab = Pam * Pmb
            Qab = Qam * Qmb
            Tab = Pam * Tmb + Tam * Qmb
        return Pab, Qab, Tab

    digits_term_ratio = math.log10(2**-10)
    if base10log :
        digits = 10 ** digits
    n = int(digits / digits_term_ratio + 1)
    P, Q, T = bs_computing(0, n)
    aperys = (T + 77 * Q)/(128 * Q)

    end = time.time()
    duration = end - start

    if save :
        try :
            with open("aperys_digits.txt", "r") as f :
                text = f.readlines()
        except :
            text = ["a b 0 2"]

        first_line = text[0].split(" ")
        if int(first_line[2]) <= digits :
            with open("aperys_digits.txt", "w") as f :
                str_aperys = str(aperys)
                aperys_string = str_aperys
                f.write(f"Apery's Constant's first {digits} digits are : \n" + aperys_string)
                f.write("\n \n")
                f.write(f"Computed in {duration}s")

    return aperys, duration


apery_constant(100, False, True)
