#! /usr/bin/python3

import struct as st
from random import shuffle
from math import exp

from CONTEXTE import D, N, P, INTERVALLE_MAX, DEPART
from CONTEXTE import MEGA_T

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

OK = lambda s: print(f"[OK] {s}")

def lire(fichier):
	with open(fichier, 'rb') as co:
		bins = co.read()
		(L,) = st.unpack('I', bins[:4])
		return st.unpack('f'*L, bins[4:])

def softmax(l):
	e = [exp(i) for i in l]
	s = sum(e)
	return [i/s for i in e]

def norme(l):
	_min, _max = min(l), max(l)
	return [(e-_min)/(_max - _min) for e in l]

def norme_théorique(l, _min, _max):
	return [(e-_min)/(_max - _min) for e in l]

def norme_relative(l):
	__max = max([abs(min(l)), abs(max(l))])
	_min, _max = -__max, +__max
	return [(e-_min)/(_max - _min) for e in l]

def diff(l):
	return [a-b for a,b in zip(l[1:], l[:-1])]

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#python3 prixs/dar.py PRIXS={HEURES} prixs/tester_model_donnee.bin BTC, ETH, ...

from sys import argv
assert len(argv) > (1 + 2)
PRIXS       = int(argv[1].split('=')[1])
fichier_bin = argv[2 ]
MARCHEES    = argv[3:]
print(f'PRIXS={PRIXS}, DEPART={DEPART}, P={P}, MEGA_T={MEGA_T}')
assert (PRIXS - DEPART-P) // MEGA_T > 0
assert any('BTC' in marchee for marchee in MARCHEES)

sources_nom = ['prixs', 'low', 'high', 'median', 'volumes', 'volumes_A', 'volumes_U']
sources     = {
	marchee : {
		nom_extraction  : lire(f'prixs/{marchee}USDT/{nom_extraction}.bin')
		for nom_extraction in [
			'prixs',
			'low', 'high', 'median',
			'volumes', 'volumes_A', 'volumes_U']
		}
	for marchee in MARCHEES#["BTC", "ETH"]
}
print(PRIXS, [len(v) for m,ex in sources.items() for k,v in ex.items()])
assert all(len(v)==PRIXS for m,ex in sources.items() for k,v in ex.items())

###############################################################################################################

from prixs.outils import ema, direct, macd, chiffre

heures = 1, 2, 5#, 12, 48#, 168, 300

DIRECT = [
	{
		'ligne' : diff(    direct(ema(sources[m][ex], K=i))),
		'interv': i*j,
		'type_de_norme':norme
	}
	for m in MARCHEES
		for ex in ('prixs',)# 'low', 'high')#, 'volumes', 'volumes_A', 'volumes_U',)
			for i in heures
				for j in (1,)#(1/2, 1, 2)
					if 1 <= (i*j) < INTERVALLE_MAX
]

MACD = [
	{
		'ligne' : diff( macd(ema(sources[m][ex], K=i), e=i*j*k)),
		'interv': i*j,
		'type_de_norme':norme_relative
	}
	for m in MARCHEES
		for ex in ('prixs',)
			for i in heures
				for j in (1,)#(1/2, 1, 2)
					for k in (1,) #(1/4, 1/2, 1)#(1/8, 1/4, 1/2)
						if 1 <= (i*j) < INTERVALLE_MAX
]

CHIFFRE = [
	{
		'ligne' : diff( chiffre(ema(sources[m][ex], K=i), __chiffre=k)),
		'interv': i*j,
		'type_de_norme': lambda *a: norme_théorique(*a, _min=0, _max=1.0)
	}
	for m in MARCHEES
		for ex in ('prixs',)
			for i in heures
				for j in (1,)#:(1/2, 1, 2)
					for k in (1000, 10000)
						if 1 <= (i*j) < INTERVALLE_MAX
]

#RSI

#Stockastique Rsi

#AO

#%R

#eventuellement, chiffre haut / bas, norme [0;+1], [-1;0] (car on prefere des signaux a de la géométrie)

###############################################################################################################

T = PRIXS - DEPART - P

lignes = []

TRANSFORMATIONS = (DIRECT+MACD)#+CHIFFRE)

for l in TRANSFORMATIONS:
	assert len(l['ligne']) >= T
	lignes += [l]
LIGNES = len(lignes)

print(f"LIGNES = {LIGNES}")
print(f"T = {T}")
print(f"D = {D}")
print(f"N = {N}")
print(f"P = {P}")

###############################################################################################################

g = lambda x: (exp(5*x) - 1) / (exp(5*1) - 1)

def D_ification(l):		#[0;1] -> D*[0;1]
	assert all(0 <= i <= +1 for i in l)
	m=[[ g(1-abs(x - d/(D-1))  ) for d in range(D)] for x in l ]
	#return [ (1 if m[i][d]==max(m[i]) else 0) for i,x in enumerate(l) for d in range(D) ]
	sm = [(l) for l in m]
	return [e for l in sm for e in l]

prixs = sources[MARCHEES[0]]['prixs']

print("prixs : ", prixs[-5:])

with open(fichier_bin, "wb") as co:
	co.write(st.pack('I', T))
	co.write(st.pack('I'*4, LIGNES, D, N, P))

	entrees = []
	sorties = []

	for t in range(DEPART, PRIXS - P - ((PRIXS-DEPART-P)%MEGA_T)):
		
		for l in lignes:
			entrees += D_ification(l['type_de_norme']([ l['ligne'][t - n*int(l['interv'])] for n in range(N)]))
		
		sorties += [(prixs[t+p+1]/prixs[t+p]-1) for p in range(P)]

	print(f'Quelques entrées : {entrees[:4], entrees[-4:]}')

	co.write(st.pack('f'*len(entrees), *entrees))
	co.write(st.pack('f'*len(sorties), *sorties))