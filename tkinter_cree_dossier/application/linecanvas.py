from tkinter_cree_dossier.application._etc import *

class DraggableFrame(tk.Frame):
	def __init__(self, parent, application, x, y, module, numero, *args, **kwargs):
		tk.Frame.__init__(self, parent.canvas, *args, **kwargs)
		self.parent = parent
		self.application = application
		#
		self.bind("<Button-1>",  self.on_drag_start)
		self.bind("<B1-Motion>", self.on_drag_motion)
		self.place(x=x, y=y)
		#	---
		self.module = module
		#   ---
		self.numero = numero
		self.lbl = tk.Label(self, text=module.nom + f'  #{numero}', bg='white')
		self.lbl.grid(row=0, column=0, columnspan=3)
		#	---------
		tk.Button(self, text="X", fg='red', command=self.suppr_la_frame).grid(row=0, column=4)
		#   --- X ---
		#self.xs = [Entree(self, f'X{i}', x) for i,x in enumerate(module.X)]
		self.ps = [Entree(self, f'{nom}', p, bg='white') for i,(nom,p) in enumerate(module.params.items())]
		#self.ys = [Entree(self, f'Y{i}', y) for i,y in enumerate(module.Y)]

		self.xs = []
		for i,x in enumerate(module.X):
			self.xs += [Entree(self, f'X{i}', x, bg='white')]
			tk.Button(self, text='.', command=lambda _x=i:self.sel_B(_x)).grid (row=1+i, column=0)
			self.xs[-1].grid                                                   (row=1+i, column=1)
		#
		for i,p in enumerate(self.ps): p.grid                                  (row=1+i, column=2)
		#
		self.ys = []
		for i,y in enumerate(module.Y):
			self.ys += [Entree(self, f'Y{i}', y, bg='white')]
			self.ys[-1].grid                                                  (row=1+i, column=3)
			tk.Button(self, text='.', command=lambda _y=i:self.sel_A(_y)).grid(row=1+i, column=4)
		#
		self.drop_connect = Entree(self, "Dc%", 0)
		self.drop_____out = Entree(self, "Do%", 0)

		self.drop_connect.grid(row=1+max([len(module.X), len(module.Y), len(module.params.items())])+1, column=1, columnspan=2)
		self.drop_____out.grid(row=1+max([len(module.X), len(module.Y), len(module.params.items())])+1, column=3, columnspan=2)

	def mettre_a_jour_module(self):
		for x in range(len(self.xs)):
			self.module.X[x] = eval(self.xs[x].val.get())
		for p in range(len(self.ps)):
			self.module.params[self.ps[p].A] = eval(self.ps[p].val.get())
		for y in range(len(self.ys)):
			self.module.Y[y] = eval(self.ys[y].val.get())

		self.module.do = eval(self.drop_____out.val.get())
		self.module.dc = eval(self.drop_connect.val.get())

	def set_entree_depuis_valeurs_module(self):
		for x in range(len(self.xs)):
			self.xs[x].val.set(str(self.module.X[x]))
		for p in range(len(self.ps)):
			self.ps[p].val.set(str(self.module.params[self.ps[p].A]))
		for y in range(len(self.ys)):
			self.ys[y].val.set(str(self.module.Y[y]))

		self.drop_____out.val.set(str(self.module.do))
		self.drop_connect.val.set(str(self.module.dc))

		self.lbl.config(text=self.module.nom + f'  #{self.numero}')

	def sel_A(self, _y):
		self.application.boutons.connections.instA.set  (str(self.numero))
		self.application.boutons.connections.sortieA.set(str(     _y    ))
	
	def sel_B(self, _x):
		self.application.boutons.connections.instB.set  (str(self.numero))
		self.application.boutons.connections.entréeB.set(str(     _x    ))

	def suppr_la_frame(self):
		self.application.suppr_une_frame(self.numero)
	
	def on_drag_start(self, event):
		self._drag_start_x = event.x
		self._drag_start_y = event.y
	
	def on_drag_motion(self, event):
		delta_x = event.x - self._drag_start_x
		delta_y = event.y - self._drag_start_y
		new_x = self.winfo_x() + delta_x
		new_y = self.winfo_y() + delta_y
		#
		self.place(x=new_x, y=new_y)
		self.mettre_a_jour_module()
		self.application.canvas.update_lines()  # Update lines through parent canvas

	def parametriser_le_module(self):
		self.mettre_a_jour_module()

class LineCanvas(tk.Canvas):
	def __init__(self, parent, application, *args, **kwargs):
		tk.Canvas.__init__(self, parent, *args, **kwargs)
		self.parent = parent
		self.application = application
		self.application.prochain_numero_a_donner = 0
		#
		self.lignes = []
		self.textes = []

		self.connections = [
			# (instA,sortieA), (instB,entreeB), t
		]

	def B_a_déjà_cette_entrée_assignée(self, A, B):
		for (iA,sA), (iB,eB), t in self.connections:
			if B[0] == iB:
				if eB == B[1]:
					return True
		return False

	def ajouter_connections(self, A, B, t):
		if t in (0, -1):
			if len(A) == len(B) == 2:
				if (A[0] in self.application.numeros() and B[0] in self.application.numeros()):
					if (A[1] < len(self.application.trouver_frame(A[0]).ys) and B[1] < len(self.application.trouver_frame(B[0]).xs)):
						if not (A,B) in self.connections:
							if not self.B_a_déjà_cette_entrée_assignée(A, B):
								self.connections += [[A,B,t]]
							else:
								messagebox.showwarning("Attention", f"{B[0]} a déjà son entrée {B[1]} assignée")
						else:
							messagebox.showwarning("Attention", f"La connection {A[0]}.{A[1]} -> {B[0]}.{B[1]} existe déjà")
					else:
						messagebox.showwarning("Attention", f"A ou B n'a pas d'entree ou de sortie {A[1]} ou {B[1]}")
				else:
					messagebox.showwarning("Attention", f"A:{A[0]} et/ou B:{B[0]} n'existe pas")
			else:
				messagebox.showwarning("Attention", f"La connection A={A} B={B} est invalide")
		else:
			messagebox.showwarning("Attention", f"t={t} est invalide. t doit etre dans (0,-1)")

		self.update_lines()
	
	def add_line(self, depart, fin, t):
		_moins_1 = (t == -1)
		ligne = self.create_line(depart[0], depart[1], fin[0], fin[1], width=2, arrow=tk.LAST, fill=('light grey' if _moins_1 else 'black'))
		texte = self.create_text(
			depart[0] + (fin[0]-depart[0])/2,
			depart[1] + (fin[1]-depart[1])/2,
			text = f'#{len(self.lignes)}' + ('[-1]' if t==-1 else ''),
			anchor="nw", fill=('light grey' if _moins_1 else 'black'))
		self.lignes += [ligne] #gc()
		self.textes += [texte] #gc()
	
	def update_lines(self):
		self.delete("all")
		#
		self.lignes      = []
		#
		for (instA, sortieA), (instB,entreeB),t in self.connections:
			frameA, frameB = self.application.trouver_frame(instA), self.application.trouver_frame(instB)
			#
			Xa = frameA.winfo_width ()
			Ya = frameA.winfo_height()
			Xb = frameB.winfo_width ()
			Yb = frameB.winfo_height()
			#
			Ax, Ay = frameA.winfo_x(), frameA.winfo_y()
			Bx, By = frameB.winfo_x(), frameB.winfo_y()
			#
			depart = [Ax+Xa, Ay+45+sortieA*30]
			fin    = [Bx,    By+45+entreeB*30]
			#
			#	Ajouter un léger décalage
			depart[0] += 10
			fin   [0] -= 10
			#
			self.add_line(depart, fin, t)
