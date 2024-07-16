from tkinter_cree_dossier.tkinter_mdl import Module_Mdl 
from tkinter_cree_dossier.tkinter_dico_inst import Dico

from tkinter_cree_dossier.tkinter_modules_inst_liste import *

from tkinter_cree_dossier.tkinter_mdl_plus import *

img_chaine                = "tkinter_cree_dossier/modules_images/chaine.png"
img_residue               = "tkinter_cree_dossier/modules_images/residue.png"
img_chaine_residue        = "tkinter_cree_dossier/modules_images/chaine_residue.png"
img_residue_chaine        = "tkinter_cree_dossier/modules_images/residue_chaine.png"
img_chaine_residue_chaine = "tkinter_cree_dossier/modules_images/chaine_residue_chaine.png"

conn = lambda sortie,inst,entree: (sortie, (inst,entree))

#########################################################################################

f_tanh     = 0
f_logistic = 1
f_gauss    = 2
f_ReLu     = 3
f_exp      = 4
f_Id       = 5

#########################################################################################

class SOMME3(Module_Mdl):
	nom = "A+B+C"
	X, Y = [0,0,0], [0]
	X_noms, Y_noms = ["A","B","C"], ["Y"]
	params = {
	}
	def cree_ix(self):
		#	Params
		A = self.X[0]
		B = self.X[1]
		C = self.X[2]
		Y = self.Y[0]

		assert A==B==C==Y

		#	------------------

		self.ix = [
			a_b :=Dico(i=i_Somme2, X=[Y,Y], x=[None,None], xt=[None,None], y=Y, p=[], sortie=True , do=self.do,dc=self.dc),
			ab_c:=Dico(i=i_Somme2, X=[Y,Y], x=[a_b,None],  xt=[0,   None], y=Y, p=[], sortie=True , do=self.do,dc=self.dc),
		]

		return self.ix

#########################################################################################

class AB_plus_CD(Module_Mdl):
	nom = "A*B + C*D"
	X, Y = [0,0,0,0], [0]
	X_noms, Y_noms = ["A","B","C","D"], ["Y"] # LSTM [X], [H]
	params = {
	}
	def cree_ix(self):
		#	Params
		A = self.X[0]
		B = self.X[1]
		C = self.X[2]
		D = self.X[3]
		Y = self.Y[0]

		assert A==B==C==D==Y

		#	------------------

		self.ix = [
			ab:=Dico(i=i_Mul,     X=[Y,Y], x=[None,None], xt=[None,None], y=Y, p=[], sortie=False, do=self.do,dc=self.dc),
			cd:=Dico(i=i_Mul,     X=[Y,Y], x=[None,None], xt=[None,None], y=Y, p=[], sortie=False, do=self.do,dc=self.dc),
			abcd:=Dico(i=i_Somme, X=[Y,Y], x=[ab,cd],     xt=[0,0],       y=Y, p=[], sortie=True , do=self.do,dc=self.dc),
		]

		return self.ix

#########################################################################################

class SOFTMAX(Module_Mdl):
	bg, fg = 'yellow', 'black'
	nom = "Softmax"
	X, Y = [0], [0]
	X_noms, Y_noms = ["X"], ["Y"]
	params = {
		'C0' : 1
	}
	def cree_ix(self):
		#	Params
		X = self.X[0]
		Y = self.Y[0]

		C0 = self.params['C0']

		assert X==Y

		#	------------------

		self.ix = [
			_expx   := Dico(i=i_Activation,       X=[Y],   x=[None],        xt=[None], y=Y, p=[f_exp], sortie=False   , do=self.do,dc=self.dc),
			somme   := Dico(i=i_ISomme,            X=[Y],   x=[_expx],       xt=[0],    y=C0, p=[C0],  sortie=False, do=self.do,dc=self.dc),
			softmax := Dico(i=i_Div_Scal, X=[Y,C0], x=[_expx,somme], xt=[0,0],  y=Y, p=[C0],  sortie=True , do=self.do,dc=self.dc),
		]

		return self.ix

class NORMALISATION(Module_Mdl):
	bg, fg = 'blue', 'black'
	nom = "Normalisation"
	X, Y = [0], [0]
	X_noms, Y_noms = ["X"], ["Y"]
	params = {
		'C0' : 1
	}
	def cree_ix(self):
		#	Params
		X = self.X[0]
		Y = self.Y[0]

		C0 = self.params['C0']

		assert X==Y

		#	------------------

		self.elements = {
			'x' : MODULE_i_Y(X=[X], Y=[X], params={}, do=0,dc=0).cree_ix(),
			
			'minmax' : MODULE_i_IMaxMin(X=[X], Y=[2*C0], params={'C0':C0}, do=0,dc=0).cree_ix(),
			'(e-min)/(max-min)' : MODULE_i_Normalisation(X=[X, 2*C0], Y=[Y], params={'C0':C0}, do=self.do,dc=0).cree_ix(),
		}

		self.connections = {
			'x' : {0:None},
			'minmax' : {0:('x',0)},
			'(e-min)/(max-min)' : {
				0:('x',0),
				1:('minmax',0)
			}
		}

		self.cree_elements_connections()
		return self.ix