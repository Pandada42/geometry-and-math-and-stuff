from Number_Thingies.number_thingies_main import *
import decimal
import numpy as np


# Goal here is to have a function that computes zeta functions
# We will use the exponential expression of the terms at rational points.
# We thus need to compute logarithms at prime Values.
# We use : log(q) = log(p) + 2 * atanh((q-p)/(q+p))


def atanh(x, N, base10 = False) :
	u, v = simplify(x)

	Nstar = N
	if base10 :
		Nstar = 3.32 * Nstar
		Nstar = int(Nstar) + 1

	def bs_computing(a, b) :
		if b - a == 1 :
			if a == 0 :
				Pab = u
				Qab = v
				Bab = 1
			else :
				Pab = u ** 2
				Qab = v ** 2
				Bab = 2 * a + 1
			Tab = Pab

		else :
			m = (a + b) // 2
			Pam, Bam, Qam, Tam = bs_computing(a, m)
			Pmb, Bmb, Qmb, Tmb = bs_computing(m, b)
			Pab = Pam * Pmb
			Bab = Bam * Bmb
			Qab = Qam * Qmb
			Tab = Bmb * Qmb * Tam + Bam * Pam * Tmb
		return Pab, Bab, Qab, Tab

	# Number of terms to be computed : remainder is smaller than (x^2nb)/(1-x) since x < 1
	x = u / v
	foo = x / (1 - x)
	nb = 1
	bit_val = (1 / 2) ** Nstar
	while foo > bit_val :
		foo *= (x ** 2)
		nb += 1

	P, B, Q, T = bs_computing(0, nb)
	if base10 :
		res = (10 ** Nstar * T) // (B * Q)

	else :
		res = (2 ** Nstar * T) // (B * Q)

	return "0." + str(res)[:N]


def is_equal_until(str1, str2) :
	print(len(str1), len(str2))
	n = min(len(str1), len(str2))
	i = 0
	while i < n :
		if str1[i] != str2[i] :
			break
		i += 1
	return i, str1[i], str2[i]


print(is_equal_until(
	"0.11157177565710487788314754515491725168730054277400360683564393624369587188413416670920361205017111785798167049028709571617648237890420754278413755709677690184536224792022018763643938947727908905751172748143594193345574236892408878145101221008617062444837769595767193453491719348853938107297977204544190527883619726814823812507606720912720855374094057020082573918613684328672628912492751309638177904743125102069410306454985240258720880420280552274398925387387339557323298609572876324428566702396233790868159491081104484233857777644622471086612256190931402425652028448825225776032103457391074945311883499153883731893213958147242012375491918115215863704926359308722057025314713188588341914859470081061697536414170359040875522627176679679912975848788779264516895228363578124125004256670810889496237957125409125271538904714336926858950111382708490830249047416215317544468144259527819021863296882635930288127916397443412090848714094559078009579475354913681008907467251162503745635410086701221640725826219679022644728764850880673683386047416918",
	atanh((1, 9), 1000, base10 = True)))
