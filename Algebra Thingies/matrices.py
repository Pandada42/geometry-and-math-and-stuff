from math import ceil, log


class matrix :
	def __init__(self, values: list[list[float]]) :
		self.Rows = len(values)
		self.Columns = len(values[0])
		self.Values = values
		self.isSquare = self.Rows == self.Columns

	def __getitem__(self, item1, item2 = None) :
		if item2 is None :
			return [self.Values[k][item1] for k in range(self.Rows)]
		return self.Values[item1][item2]

	def __str__(self) :
		return str(self.Values)

	def transpose(self) :
		nvals = [[self[i][j] for j in range(self.Columns)] for i in range(self.Rows)]
		return matrix(nvals)

	def trace(self) :
		if self.isSquare :
			return sum([self[i][i] for i in range(self.Rows)])


valls = [[2, 1], [1, 1]]
mat = matrix(valls)


def add(A, B) :
	if A.Rows != B.Rows or A.Columns != B.Columns :
		return "Incompatible Dimensions"
	nvals = [[A[i][j] for j in range(A.Columns)] for i in range(A.Rows)]
	for i in range(A.Rows) :
		for j in range(A.Columns) :
			nvals[i][j] += B[i][j]
	return matrix(nvals)


def sub(A, B) :
	if A.Rows != B.Rows or A.Columns != B.Columns :
		return "Incompatible Dimensions"
	C = [[0 for _ in range(A.Columns)] for _ in range(A.Rows)]
	for i in range(0, A.Rows) :
		for j in range(0, A.Columns) :
			C[i][j] -= B[i][j]
	return matrix(C)


def naive_product(A, B) :
	if not A.Columns == B.Rows :
		return "Dimension Error : Incompatible Product"
	nvals = [[0 for _ in range(B.Columns)] for _ in range(A.Rows)]

	for i in range(A.Rows) :
		for j in range(B.Columns) :
			for k in range(A.Columns) :
				nvals[i][j] += A[i][k] * B[k][j]

	return matrix(nvals)


def strassen_product(A, B) :
	if not (A.isSquare and B.isSquare) :
		return "Only works for square matrices"


	nextPowerOfTwo = lambda number : 2 ** int(ceil(log(number, 2)))

	n = A.Rows
	m = nextPowerOfTwo(n)
	APrep = matrix([[0 for _ in range(m)] for _ in range(m)])
	BPrep = matrix([[0 for _ in range(m)] for _ in range(m)])
	for i in range(n) :
		for j in range(n) :
			APrep[i][j] = A[i][j]
			BPrep[i][j] = B[i][j]

	def strassenR(A, B) :
		"""
		Implementation of the strassen algorithm, similar to
		http://en.wikipedia.org/w/index.php?title=Strassen_algorithm&oldid=498910018#Source_code_of_the_Strassen_algorithm_in_C_language
		"""
		if not (A.isSquare and B.isSquare) :
			return "Only Works for Square Matrices, Grow up to 2^n"
		if not (A.Rows == B.Rows) :
			return "Dimension Error"
		n = A.Columns

		if n <= 25 :
			return naive_product(A, B)
		else :
			# initializing the new sub-matrices
			new_size = n // 2
			a11 = matrix([[0 for _ in range(new_size)] for _ in range(new_size)])
			a12 = matrix([[0 for _ in range(new_size)] for _ in range(new_size)])
			a21 = matrix([[0 for _ in range(new_size)] for _ in range(new_size)])
			a22 = matrix([[0 for _ in range(new_size)] for _ in range(new_size)])

			b11 = matrix([[0 for _ in range(0, new_size)] for _ in range(new_size)])
			b12 = matrix([[0 for _ in range(0, new_size)] for _ in range(new_size)])
			b21 = matrix([[0 for _ in range(0, new_size)] for _ in range(new_size)])
			b22 = matrix([[0 for _ in range(0, new_size)] for _ in range(new_size)])

			# dividing the matrices in 4 sub-matrices:
			for i in range(new_size) :
				for j in range(new_size) :
					a11[i][j] = A[i][j]  # top left
					a12[i][j] = A[i][j + new_size]  # top right
					a21[i][j] = A[i + new_size][j]  # bottom left
					a22[i][j] = A[i + new_size][j + new_size]  # bottom right

					b11[i][j] = B[i][j]  # top left
					b12[i][j] = B[i][j + new_size]  # top right
					b21[i][j] = B[i + new_size][j]  # bottom left
					b22[i][j] = B[i + new_size][j + new_size]  # bottom right

			# Calculating p1 to p7:
			aResult = add(a11, a22)
			bResult = add(b11, b22)
			p1 = strassenR(aResult, bResult)  # p1 = (a11+a22) * (b11+b22)

			aResult = add(a21, a22)  # a21 + a22
			p2 = strassenR(aResult, b11)  # p2 = (a21+a22) * (b11)

			bResult = sub(b12, b22)  # b12 - b22
			p3 = strassenR(a11, bResult)  # p3 = (a11) * (b12 - b22)

			bResult = sub(b21, b11)  # b21 - b11
			p4 = strassenR(a22, bResult)  # p4 = (a22) * (b21 - b11)

			aResult = add(a11, a12)  # a11 + a12
			p5 = strassenR(aResult, b22)  # p5 = (a11+a12) * (b22)

			aResult = sub(a21, a11)  # a21 - a11
			bResult = add(b11, b12)  # b11 + b12
			p6 = strassenR(aResult, bResult)  # p6 = (a21-a11) * (b11+b12)

			aResult = sub(a12, a22)  # a12 - a22
			bResult = add(b21, b22)  # b21 + b22
			p7 = strassenR(aResult, bResult)  # p7 = (a12-a22) * (b21+b22)

			# calculating c21, c21, c11 e c22:
			c12 = add(p3, p5)  # c12 = p3 + p5
			c21 = add(p2, p4)  # c21 = p2 + p4

			aResult = add(p1, p4)  # p1 + p4
			bResult = add(aResult, p7)  # p1 + p4 + p7
			c11 = sub(bResult, p5)  # c11 = p1 + p4 - p5 + p7

			aResult = add(p1, p3)  # p1 + p3
			bResult = add(aResult, p6)  # p1 + p3 + p6
			c22 = sub(bResult, p2)  # c22 = p1 + p3 - p2 + p6

			# Grouping the results obtained in a single matrix:
			C = [[0 for _ in range(n)] for _ in range(n)]
			for i in range(new_size) :
				for j in range(new_size) :
					C[i][j] = c11[i][j]
					C[i][j + new_size] = c12[i][j]
					C[i + new_size][j] = c21[i][j]
					C[i + new_size][j + new_size] = c22[i][j]
			return C

	CPrep = strassenR(APrep, BPrep)
	C = [[0 for _ in range(n)] for _ in range(n)]
	for i in range(n) :
		for j in range(n) :
			C[i][j] = CPrep[i][j]
	return matrix(C)


def permutation(n, swaps):
	vals = [[0 for _ in range(n)] for _ in range(n)]
	for i in range(n):
		if i in swaps :
			vals[i][swaps[i]] = 1
		else :
			vals[i][i] = 1
	return matrix(vals)


def LUP(A):
	if not A.isSquare :
		return "No LU decomposition for a rectangular matrix"
	n = A.Rows
	if A[0][0] == 0 :
		i = min([j for j in range(n) if A[j][0] != 0])
		if i is None :
			return "c'est la merde"
		P = permutation(n, {i : 0, 0 : i})
	return None


def determinant(A):
	"""
	:param A: Integer Matrix
	:type A: matrix
	:return: det(A) using Bareiss algorithm
	:rtype:
	"""
	if not A.isSquare : return "No determinant for a rectangular matrix"
	n = A.Rows
	if A[0][0] == 0 :
		i = min([j for j in range(n) if A[j][0] != 0])
		if i is None :
			return 0
		P = permutation(n, {i : 0, 0 : i})
		return determinant(strassen_product(P, A))

	M = matrix([[A[i][j] for j in range(n)] for i in range(n)])
	pivot = 1
	for k in range(n-1):
		for i in range(k+1, n):
			for j in range(k+1, n):
				M[i][j] = M[k][k] * M[i][j] - M[i][k] * M[k][j]
				M[i][j] = M[i][j] / pivot
		pivot = M[k][k]

	return M[-1][-1]


print(determinant(mat))























