class Inst:
	def __init__(self, X=[], Y=0, params=[], do=0, dc=0):
		self.X      = X
		self.Y      = Y
		self.params = params

		self.do = do
		self.dc = dc

		assert len(self.params) == len(self.params_str)

	def assert_coherance(self):
		raise Exception("Doit etre implémenté")

class i_Y(Inst):
	nom = "y"
	params = []
	params_str = []
	X = [0]
	Y =  0

	def assert_coherance(self):
		assert len(self.X) == 1
		assert self.X[0] == self.Y

		#	Params
		assert len(self.params) == 0

############################################

class i__Entree(Inst):
	nom = "_entrée"
	params = []
	params_str = []
	X = [0]
	Y =  0

	def assert_coherance(self):
		assert len(self.X) == 1
		assert self.X[0] == self.Y

		#	Params
		assert len(self.params) == 0

############################################

class i_Activation(Inst):
	nom = "activ(x)"
	params = [0]
	params_str = ['activ']
	X = [0]
	Y =  0

	def assert_coherance(self):
		assert len(self.X) == 1
		assert self.X[0] == self.Y

		#	Params
		assert len(self.params) == 1
		#       tanh, logistic, gauss, relu
		#activs = (0,     1,       2,     3)
		#assert self.params[0] in activs

class i_Activation_Poid(Inst):
	nom = "activ(x+p)"
	params = [0]
	params_str = ['activ']
	X = [0]
	Y =  0

	def assert_coherance(self):
		assert len(self.X) == 1
		assert self.X[0] == self.Y

		#	Params
		assert len(self.params) == 1
		#       tanh, logistic, gauss, relu
		#activs = (0,     1,       2,     3)
		#assert self.params[0] in activs

############################################

class i_Poid(Inst):
	nom = "Poid"
	params = []
	params_str = []
	X = []
	Y =  0

	def assert_coherance(self):
		assert len(self.X) == 0
		assert self.Y > 0

		#	Params
		assert len(self.params) == 0

############################################

class i_MatMul(Inst):
	nom = "A@B"
	params = [0,0,0,0]
	params_str = ['Ax', 'Ay', 'Bx', 'C0']
	X = [0,0]
	Y =  0

	def assert_coherance(self):
		assert len(self.X) == 2
		assert self.Y > 0

		#	Params
		assert len(self.params) == 4

		Ax, Ay, Bx, C0 = self.params

		assert self.Y    == C0 * Bx * Ay
		assert self.X[0] == C0 * Ax * Ay
		assert self.X[1] == C0 * Bx * Ax

class i_MatMul_Poid_AP(Inst):
	nom = "A@Poid"
	params = [0,0,0,0]
	params_str = ['Ax', 'Ay', 'Bx', 'C0']
	X = [0]
	Y =  0

	def assert_coherance(self):
		assert len(self.X) == 1
		assert self.Y > 0

		#	Params
		assert len(self.params) == 4

		Ax, Ay, Bx, C0 = self.params

		assert self.Y    == C0 * Bx * Ay
		assert self.X[0] == C0 * Ax * Ay

class i_MatMul_Poid_PA(Inst):
	nom = "Poid@A"
	params = [0,0,0,0]
	params_str = ['Ax', 'Ay', 'Bx', 'C0']
	X = [0]
	Y =  0

	def assert_coherance(self):
		assert len(self.X) == 1
		assert self.Y > 0

		#	Params
		assert len(self.params) == 4

		Ax, Ay, Bx, C0 = self.params

		assert self.X[0] == (Bx*Ax*C0)
		assert self.Y    == (Ay*Bx*C0)

############################################

class i_QKtDivClef(Inst):
	nom = "(Q @ K.t)/Clef**.5"
	params = [0,0,0,0]
	params_str = ['Ax', 'Ay', 'Bx', 'C0']
	X = [0,0]
	Y =  0

	def assert_coherance(self):
		assert len(self.X) == 2
		assert self.Y > 0

		#	Params
		assert len(self.params) == 4

		Ax, Ay, Bx, C0 = self.params

		assert self.Y    == C0 * Bx * Ay
		assert self.X[0] == C0 * Ax * Ay
		assert self.X[1] == C0 * Bx * Ax

############################################

class i_Somme(Inst):
	nom = "A+B"
	params = []
	params_str = []
	X = [0,0]
	Y =  0

	def assert_coherance(self):
		assert len(self.X) == 2
		assert self.Y == self.X[0] == self.X[1]

		#	Params
		assert len(self.params) == 0

class i_Sous(Inst):
	nom = "A-B"
	params = []
	params_str = []
	X = [0,0]
	Y =  0

	def assert_coherance(self):
		assert len(self.X) == 2
		assert self.Y == self.X[0] == self.X[1]

		#	Params
		assert len(self.params) == 0

class i_Mul(Inst):
	nom = "A*B"
	params = []
	params_str = []
	X = [0,0]
	Y =  0

	def assert_coherance(self):
		assert len(self.X) == 2
		assert self.Y == self.X[0] == self.X[1]

		#	Params
		assert len(self.params) == 0

class i_Div(Inst):
	nom = "A/B"
	params = []
	params_str = []
	X = [0,0]
	Y =  0

	def assert_coherance(self):
		assert len(self.X) == 2
		assert self.Y == self.X[0] == self.X[1]

		#	Params
		assert len(self.params) == 0

##########################################

class i_ISomme(Inst):
	nom = "sum(vect)"
	params = [1]
	params_str = ['C0']
	X = [0]
	Y =  0

	def assert_coherance(self):
		assert len(self.X) == 1

		assert self.Y == self.params[0]
		assert self.X[0] % self.params[0] == 0

		#	Params
		assert len(self.params) == 1
		assert self.params[0] > 0

class i_IMaxMin(Inst):
	nom = "maxmin(vect)"
	params = [1]
	params_str = ['C0']
	X = [0]
	Y =  0

	def assert_coherance(self):
		assert len(self.X) == 1

		assert self.Y == self.params[0] * 2
		assert self.X[0] % self.params[0] == 0

		#	Params
		assert len(self.params) == 1
		assert self.params[0] > 0

##########################################

class i_Normalisation(Inst):
	nom = "Normalisation"
	params = [1]
	params_str = ['C0']
	X = [0,0]
	Y =  0

	def assert_coherance(self):
		assert len(self.X) == 2
		assert self.Y == self.X[0]
		assert self.X[1] == 2*self.params[0]

		#	Params
		assert len(self.params) == 1
		assert self.params[0] > 0

class i_Div_Scal(Inst):
	nom = "A<N> / b<1>"
	params = [1]
	params_str = ['C0']
	X = [0,0]
	Y =  0

	def assert_coherance(self):
		assert len(self.X) == 2
		assert self.Y == self.X[0]
		assert self.X[1] == self.params[0]

		#	Params
		assert len(self.params) == 1
		assert self.params[0] > 0

##########################################

class i_Canalisation(Inst):
	nom = "Canal X->X*C0"
	params = [0]
	params_str = ['C0']
	X = [0]
	Y =  0

	def assert_coherance(self):
		assert len(self.X) == 1
		#assert self.Y == self.X[0]

		#	Params
		assert len(self.params) == 1
		C0 = self.params[0]
		assert self.Y == self.X[0] * C0

class i_Union(Inst):
	nom = "Union AuB"
	params = []
	params_str = []
	X = [0,0]
	Y =  0

	def assert_coherance(self):
		assert len(self.X) == 2
		assert self.Y == (self.X[0]+self.X[1])

		#	Params
		assert len(self.params) == 0

class i_Transpose2d(Inst):
	nom = "Transpose 2D"
	params = [0,0,0]
	params_str = ['Ax', 'Ay', 'C0']
	X = [0]
	Y =  0

	def assert_coherance(self):
		assert len(self.X) == 1
		assert self.Y == self.X[0]

		#	Params
		assert len(self.params) == 3
		Ax, Ay, C0 = self.params
		assert Ax*Ay*C0 == self.Y == self.X[0]

##########################################
liste_insts = [
	i__Entree,
	#
	i_Activation,
	i_Activation_Poid,
	#
	i_Poid,
	#
	i_MatMul,
	i_MatMul_Poid_AP,
	i_MatMul_Poid_PA,
	#
	i_QKtDivClef,
	#
	i_Somme,
	i_Sous,
	i_Mul,
	i_Div,
	#
	i_ISomme,
	i_IMaxMin,
	#
	i_Normalisation,
	i_Div_Scal,
	#
	i_Canalisation,
	i_Union,
	i_Transpose2d
]