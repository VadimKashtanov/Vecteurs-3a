#include "btcusdt.cuh"

#include "../../impl_template/tmpl_etc.cu"

static __global__ void k__pourcent_btcusdt(
	float * somme, float * potentiel,
	float * y, float * p1p0,
	float coef_puissance,
	uint * ts__d,
	uint Y)
{
	uint t      = threadIdx.x + blockIdx.x * blockDim.x;
	uint mega_t = threadIdx.y + blockIdx.y * blockDim.y;
	//
	if (t < GRAND_T && mega_t < MEGA_T) {
		uint ty        = t_MODE(t, mega_t);
		uint t_btcusdt = ts__d[t] + mega_t;
		//
		uint a_t_il_predit = (sng(p1p0[t_btcusdt]) == sng(y[ty*Y + 0]));
		//
		float _____somme = powf(fabs(p1p0[t_btcusdt]), coef_puissance) * a_t_il_predit;
		float _potentiel = powf(fabs(p1p0[t_btcusdt]), coef_puissance) * true         ;
		//
		atomicAdd(&somme    [0], _____somme);
		atomicAdd(&potentiel[0], _potentiel);
	}
};

float *  pourcent_btcusdt(BTCUSDT_t * btcusdt, float * y__d, uint * ts__d, float coef_puissance) {
	uint Y = btcusdt->Y;
	//
	float *     somme__d = cudalloc<float>(1);
	float * potentiel__d = cudalloc<float>(1);
	//
	k__pourcent_btcusdt<<<dim3(KERD(GRAND_T, 16), KERD(MEGA_T, 8)), dim3(16,8)>>>(
		somme__d, potentiel__d,
		y__d, btcusdt->sorties__d,
		coef_puissance,
		ts__d,
		Y
	);
	ATTENDRE_CUDA();
	//
	float * somme     = gpu_vers_cpu<float>(    somme__d, 1);
	float * potentiel = gpu_vers_cpu<float>(potentiel__d, 1);
	//
	float * ret = alloc<float>(1);
	FOR(0, p, 1) ret[p] = somme[p] / potentiel[p];
	//
	cudafree<float>(    somme__d);
	cudafree<float>(potentiel__d);
	    free(           somme   );
	    free(       potentiel   );
	//
	return ret;
};
