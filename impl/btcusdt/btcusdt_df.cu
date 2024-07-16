#include "btcusdt.cuh"

#include "../../impl_template/tmpl_etc.cu"

static __global__ void k__df_btcusdt(
	float * y, float * p1p0, float * dy,
	uint * ts__d,
	uint Y,
	uint T)
{
	uint t = threadIdx.x + blockIdx.x * blockDim.x;
	//
	if (t < GRAND_T) {
		FOR(0, mega_t, MEGA_T) {
			uint ty        = t_MODE(t, mega_t);
			uint t_btcusdt = ts__d[t] + mega_t;
			assert(t_btcusdt < T);
			//
			//
			float _y = y[ty*Y + 0];
			assert(_y >= -1 && _y <= +1);
			//
			float _p1p0 = p1p0[t_btcusdt*1 + mega_t];
			//
			float _ds = dS(_y, _p1p0);
			dy[ty*Y + 0] = _ds / ((float)(GRAND_T * MEGA_T));
		};
	};
};

void df_btcusdt(BTCUSDT_t * btcusdt, float * y__d, float * dy__d, uint * ts__d) {
	uint Y = btcusdt->Y;
	//
	//
	k__df_btcusdt<<<dim3(KERD(GRAND_T, 16)), dim3(16)>>>(
		y__d, btcusdt->sorties__d, dy__d,
		ts__d,
		Y,
		btcusdt->T
	);
	ATTENDRE_CUDA();
};