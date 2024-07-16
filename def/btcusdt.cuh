#pragma once

#include "meta.cuh"

#define  score_p2(y,w,C) ( powf(y-w, C  )/(float)C )
#define dscore_p2(y,w,C) ( powf(y-w, C-1)          )

//	------------------------------------

#define  D(y,c)  score_p2(y, sng(c), 2)
#define dD(y,c) dscore_p2(y, sng(c), 2)

#define K(y,c) /*( 1.0/(1.0 + expf(-fabs(c)*30)) )//*/powf(fabs(c)*100, 1.00)
#define R(y,c) (sng(y)==sng(c) ? 1.0 : 1.0)

#define  S(y,c) ( D(y,c) * K(y,c) * R(y,c))
#define dS(y,c) (dD(y,c) * K(y,c) * R(y,c))

//	------------------------------------

typedef struct {
	//
	uint X;	//	L*N*D
	uint Y;	//	P
	//
	uint T;

	//	Espaces
	float * entrees__d;	//	X * T
	float * sorties__d;	//	Y * T
} BTCUSDT_t;

BTCUSDT_t * cree_btcusdt(char * fichier);
void     liberer_btcusdt(BTCUSDT_t * btcusdt);
//
float *  pourcent_btcusdt(BTCUSDT_t * btcusdt, float * y__d, uint * ts__d, float coef_puissance);
//
float  f_btcusdt(BTCUSDT_t * btcusdt, float * y__d,                uint * ts__d);
void  df_btcusdt(BTCUSDT_t * btcusdt, float * y__d, float * dy__d, uint * ts__d);