import math
import time

import numpy as np


def exponential(digits, base10log = False, save = True):
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
                Qab = b
                Pab = 1

        else :
            m = (a + b) // 2
            Pam, Qam = bs_computing(a, m)
            Pmb, Qmb = bs_computing(m, b)
            Qab = Qam * Qmb
            Pab = Pam * Qmb + Pmb
        return Pab, Qab

    def number_of_terms(number):
        n = 1
        k = 0
        while k < number :
            n += 1
            k += np.log10(n)
        return n

    if base10log :
        digits = 10 ** digits
    n = number_of_terms(digits)
    P, Q = bs_computing(0, n)
    eulers = 1 + P/Q

    end = time.time()
    duration = end - start

    if save :
        try :
            with open("eulers_digits.txt", "r") as f :
                text = f.readlines()
        except :
            text = ["a b 0 2"]

        first_line = text[0].split(" ")
        if int(first_line[3]) <= digits :
            with open("eulers_digits.txt", "w") as f :
                str_aperys = str(eulers)
                aperys_string = str_aperys
                f.write(f"Euler's Constant's first {digits} digits are : \n" + aperys_string)
                f.write("\n \n")
                f.write(f"Computed in {duration}s")

    return eulers, duration


exponential(3, True, True)