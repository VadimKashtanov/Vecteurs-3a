#include "mdl.cuh"

#include "../../impl_template/tmpl_etc.cu"

void mdl_allez_retour(Mdl_t * mdl, BTCUSDT_t * btcusdt, uint * ts__d) {
	mdl_f (mdl, btcusdt, ts__d);
	//
	mdl_dy_zero(mdl);
	//
	df_btcusdt(
		btcusdt,
		mdl->inst[mdl->inst_sortie]-> y__d,
		mdl->inst[mdl->inst_sortie]->dy__d,
		ts__d
	);
	mdl_df(mdl, btcusdt, ts__d);
};