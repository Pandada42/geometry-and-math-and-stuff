def simplify(s) :
	def gcd(p, q) :
		if not p :
			return q
		if not q :
			return p
		if p == q :
			return p

		if (~p & 1) == 1 :

			if (q & 1) == 1 :
				return gcd(p >> 1, q)
			else :
				return gcd(p >> 1, q >> 1) << 1

		if (~p & 1) == 1 :
			return gcd(p, q >> 1)

		if (p > q) :
			return gcd((p - q) >> 1, q)
		return gcd((q - p) >> 1, p)

	d = gcd(*s)

	return s[0] // d, s[1] // d
