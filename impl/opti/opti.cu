#include "opti.cuh"

#include "../impl_template/tmpl_etc.cu"

uint hists[] = {
	SGD_____HISTOIRE,
	MOMENT__HISTOIRE,
	RMSPROP_HISTOIRE,
	ADAM____HISTOIRE
};

void opti(
	Mdl_t     *     mdl,
	BTCUSDT_t * btcusdt,
	uint      *   ts__d,
	uint              I,
	uint       tous_les,
	uint        methode,
	float         alpha)
{
	//	--- Drop Out ---
	FOR(0, i, mdl->insts) {
		if (mdl->inst[i]->drop_out == 0) {
			mdl->inst[i]->drop_out_oui_non = 0;
		} else {
			uint y_drop_out[mdl->inst[i]->Y];
			FOR(0, j, mdl->inst[i]->Y) y_drop_out[j] = (rnd()<mdl->inst[i]->drop_out ? 1 : 0);
			mdl->inst[i]->drop_out_oui_non = cpu_vers_gpu<uint>(y_drop_out, mdl->inst[i]->Y);
		}
	}

	//	--- Hist ---
	float *** hist = alloc<float**>(hists[methode]);
	FOR(0, h, hists[methode]) {
		hist[h] = alloc<float*>(mdl->insts);
		FOR(0, i, mdl->insts) {
			hist[h][i] = cudalloc<float>(mdl->inst[i]->P);
			// = 0
		}
	}

	//	--- Plume ---
	mdl_plume_grad(mdl, btcusdt, ts__d);
	//
	float _max_abs_grad = 1;//mdl_max_abs_grad(mdl);
	if (_max_abs_grad == 0) ERR("Le grad max est = 0");
	//
	alpha /= _max_abs_grad;
	//
	printf("alpha=%f, max_abs_grad=%f => nouveau alpha=%f\n", alpha, _max_abs_grad, alpha / _max_abs_grad);
	//
	//	--- Opti  ---
	FOR(0, i, I) {
		if (i != 0) {
			//	dF(x)
			mdl_allez_retour(mdl, btcusdt, ts__d);

			//	x = x - dx
			if (methode == SGD    ) sgd    (mdl, hist, i, alpha, i);
			if (methode == MOMENT ) moment (mdl, hist, i, alpha, i);
			if (methode == RMSPROP) rmsprop(mdl, hist, i, alpha, i);
			if (methode == ADAM   ) adam   (mdl, hist, i, alpha, i);
		}
		//
		if (i % tous_les == 0) {
			float s = mdl_S(mdl, btcusdt, ts__d);
			float * p0 = mdl_pourcent(mdl, btcusdt, ts__d, 0.0);
			float * p1 = mdl_pourcent(mdl, btcusdt, ts__d, 1.0);
			float * p8 = mdl_pourcent(mdl, btcusdt, ts__d, 4.0);
			//

			printf("%3.i/%3.i score = %f (", i, I, s);

			printf("^0:{");
			FOR(0, p, btcusdt->Y) printf("\033[96m%f%%\033[0m ", p0[p]);
			printf("}  ");

			printf("^1:{");
			FOR(0, p, btcusdt->Y) printf("\033[96m%f%%\033[0m ", p1[p]);
			printf("}  ");

			printf("^4:{");
			FOR(0, p, btcusdt->Y) printf("\033[96m%f%%\033[0m ", p8[p]);
			printf("}");

			printf(")\n");

			free(p0);
			free(p1);
			free(p8);
		};
	};
	//
	//
	FOR(0, h, hists[methode]) {
		FOR(0, i, mdl->insts) {
			cudafree<float>(hist[h][i]);
		}
		free(hist[h]);
	}
	free(hist);

	//	--- Drop Out ---
	FOR(0, i, mdl->insts) {
		if (mdl->inst[i]->drop_out == 0) {
			//
		} else {
			cudafree<uint>(mdl->inst[i]->drop_out_oui_non);
			mdl->inst[i]->drop_out_oui_non = 0;
		}
	}
}