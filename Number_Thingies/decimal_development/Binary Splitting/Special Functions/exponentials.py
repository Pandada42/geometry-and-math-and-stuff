import numpy as np
from Number_Thingies.number_thingies_main import *


def exp_matrix_mul_iter(x, n):

	def M(x, k) :
		"""
		:param x: Argument in the exponential, any element from an algebra (see below)
		:type x:
		:param k: Element used in the recursive formula
		:type k: int
		:return: Matrix used to compute the next element of the recursion
		:rtype: numpy matrix
		"""
		res = np.matrix([[x / (k + 1), 0], [1, 1]])
		return res

	cur = np.matrix([1, 0]).transpose()
	for k in range(n):
		cur = np.matmul(M(x, k), cur)

	return cur[1, 0]


def exp_matrix_mul_bs(x, n) :

	def M(x, k) :
		"""
		:param x: Argument in the exponential, any element from an algebra (see below)
		:type x:
		:param k: Element used in the recursive formula
		:type k: int
		:return: Matrix used to compute the next element of the recursion
		:rtype: numpy matrix
		"""
		res = np.matrix([[x / (k + 1), 0], [1, 1]])
		return res

	cur = np.matrix([1, 0]).transpose()
	for k in range(n) :
		cur = np.matmul(M(x, k), cur)

	return cur[1, 0]

# Need to run the calculations to find a linear recurrence relation and apply binary splitting


def exp_bs_rational(x, n):
	"""

	:param x: rational value at which to compute the exponential
	:type x: tuple[int, int]
	:param n: Number of bits of precision i.e. precision is O(2^-n)
	:type n: int
	:return: exp(x) at 2^-n precision
	:rtype: float
	"""
	u, v = simplify(x)

	def bs_computing(a, b):
		if b - a == 1 :
			if a == 0 :
				Pab = Qab = 1
			else :
				Pab = u
				Qab = a * v
			Tab = Pab

		else :
			m = (a + b) // 2
			Pam, Qam, Tam = bs_computing(a, m)
			Pmb, Qmb, Tmb = bs_computing(m, b)
			Pab = Pam * Pmb
			Qab = Qam * Qmb
			Tab = Pam * Tmb + Tam * Qmb
		return Pab, Qab, Tab


	# Need to compute the number of terms that are to be added
	# Here n_max = O(N/(log(N) - log(|x|)) :

	n_max = n/(log_bs_int(n) - log_bs_rational(*x))
	P, Q, T = bs_computing(0, n_max)
	return T/Q
