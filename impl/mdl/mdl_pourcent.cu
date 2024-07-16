#include "mdl.cuh"

float * mdl_pourcent(Mdl_t * mdl, BTCUSDT_t * btcusdt, uint * ts__d, float coef_puissance) {
	mdl_f(mdl, btcusdt, ts__d);
	return pourcent_btcusdt(btcusdt, mdl->inst[mdl->inst_sortie]->y__d, ts__d, coef_puissance);
};