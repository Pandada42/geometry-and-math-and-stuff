import math
import time


def gamma_1_to_2(s, digits) :
    if not 1 <= s < 2 :
        return "s not in the right interval"
    start = time.time()
    x = WLambert(-10**(-digits))

    def bs_computing(a, b) :
        """
        :param a: lower bound considered
        :type a: int
        :param b: upper bound considered
        :type b: int
        :return: computes the terms for binary splitting a Gamma Function Series
        Formulas for Binary Splitting are as follows :
        a(a) = 205a^2 + 250a + 77
        p(0) = 1
        p(a) = x
        b(a) = 1
        q(a) = s + a
        """
        if b - a == 1 :
            if a == 0 :
                Pab = 1
                Qab = s
            else :
                Pab = x
                Qab = s + a
            Tab = Pab

        else :
            m = (a + b) // 2
            Pam, Qam, Tam = bs_computing(a, m)
            Pmb, Qmb, Tmb = bs_computing(m, b)
            Pab = Pam * Pmb
            Qab = Qam * Qmb
            Tab = Pam * Tmb + Tam * Qmb
        return Pab, Qab, Tab

    N = 100  # TODO : Insert Formula for calculating N
    P, Q, T = bs_computing(0, N)
    result = T/Q
    end = time.time()
    duration = end - start
    return result, duration






