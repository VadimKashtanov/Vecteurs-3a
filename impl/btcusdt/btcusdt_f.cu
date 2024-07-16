#include "btcusdt.cuh"

#include "../../impl_template/tmpl_etc.cu"

static __global__ void k__f_btcusdt(
	float * somme_score,
	float * y, float * p1p0,
	uint * ts__d,
	uint Y,
	uint T)
{
	uint t = threadIdx.x + blockIdx.x * blockDim.x;
	//
	if (t < GRAND_T) {
		//
		float s=0;
		//
		FOR(0, mega_t, MEGA_T) {
			uint ty        = t_MODE(t, mega_t);
			uint t_btcusdt = ts__d[t] + mega_t;
			assert(t_btcusdt < T);
			//
			float _y = y[ty*Y + 0];
			assert(_y >= -1 && _y <= +1);
			//
			float _p1p0 = p1p0[t_btcusdt*1 + mega_t];
			//
			s += S(_y, _p1p0);
		}
		//
		atomicAdd(&somme_score[0], s);
	}
};

float f_btcusdt(BTCUSDT_t * btcusdt, float * y__d, uint * ts__d) {
	uint Y = btcusdt->Y;
	//
	//
	float * somme__d = cudalloc<float>(1);
	k__f_btcusdt<<<dim3(KERD(GRAND_T, 16)), dim3(16)>>>(
		somme__d,
		y__d, btcusdt->sorties__d,
		ts__d,
		Y,
		btcusdt->T
	);
	ATTENDRE_CUDA();
	//
	//
	float * somme = gpu_vers_cpu<float>(somme__d, 1);
	//
	float score = somme[0] / ((float)(GRAND_T * MEGA_T));
	//
	//
	cudafree<float>(somme__d   );
	    free       (somme      );
	//
	return score;
};