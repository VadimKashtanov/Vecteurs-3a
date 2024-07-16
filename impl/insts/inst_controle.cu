#include "insts.cuh"

__global__
static void kerd_inst_zero_mega_t(float * y, uint Y, uint mega_t)
{
	uint _y = threadIdx.x + blockIdx.x * blockDim.x;
	uint _t = threadIdx.y + blockIdx.y * blockDim.y;
	//
	if (_y < Y && _t < GRAND_T) {
		y[t_MODE(_t, mega_t)*Y + _y] = 0.0;
	};
};

void inst_zero_mega_t(Inst_t * inst, uint mega_t) {
	//kerd_inst_zero_mega_t<<<DIM2(inst->Y, GRAND_T, 16,16)>>>(
	kerd_inst_zero_mega_t<<<dim3(KERD(inst->Y,16), KERD(GRAND_T,16)),dim3(16,16)>>>(
		inst->y__d,
		inst->Y,
		mega_t
	);
};

//	----------------------------------------------

__global__
static void kerd_drop_out(float * y, uint Y, uint mega_t, uint * oui_non)
{
	uint _y = threadIdx.x + blockIdx.x * blockDim.x;
	uint _t = threadIdx.y + blockIdx.y * blockDim.y;
	//
	if (_y < Y && _t < GRAND_T) {
		if (oui_non[_y] == 1) {
			y[(t_MODE(_t, mega_t))*Y + _y] = 0.0;
		}
	};
};

void inst_drop_out(Inst_t * inst, uint mega_t) {
	if (inst->drop_out_oui_non != 0) {
		kerd_drop_out<<<dim3(KERD(inst->Y,16), KERD(GRAND_T,16)),dim3(16,16)>>>(
			inst->y__d,
			inst->Y,
			mega_t,
			inst->drop_out_oui_non
		);
	};
};

//	-------------------------------------------------

//	Peut importe la valeur de y (=0 ou pas), il y a un Gradient.
//	Sauf que la on deconnecte un neurone, donc il faut annuler le gradient.

__global__
static void kerd_drop_out_deriv(float * dy, uint Y, uint mega_t, uint * oui_non)
{
	uint _y = threadIdx.x + blockIdx.x * blockDim.x;
	uint _t = threadIdx.y + blockIdx.y * blockDim.y;
	//
	if (_y < Y && _t < GRAND_T) {
		if (oui_non[_y] == 1) {
			dy[(t_MODE(_t, mega_t))*Y + _y] = 0.0;
		}
	};
};

void inst_drop_out_df(Inst_t * inst, uint mega_t) {
	if (inst->drop_out_oui_non != 0) {
		kerd_drop_out_deriv<<<dim3(KERD(inst->Y,16), KERD(GRAND_T,16)),dim3(16,16)>>>(
			inst->dy__d,
			inst->Y,
			mega_t,
			inst->drop_out_oui_non
		);
	};
};