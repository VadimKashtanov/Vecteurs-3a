#! /usr/bin/python3

# D - Détailles
# N - n elements dans le passé
# P - p elements dans le future

D = 7#6 # 6 niveaux de précision (0.0, 0.2, 0.4, 0.6, 0.8, 1.0)
N = 5#6#4
P = 1

INTERVALLE_MAX = 256

DEPART = INTERVALLE_MAX * N

import struct as st
with open("structure_generale.bin", 'rb') as co:
	bins = co.read()
	(I,) = st.unpack('I', bins[:4])
	elements = st.unpack('I'*int(len(bins[4:])/4), bins[4:])
	#
	MEGA_T, = elements