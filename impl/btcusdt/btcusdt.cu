#include "btcusdt.cuh"

#include "../../impl_template/tmpl_etc.cu"

BTCUSDT_t * cree_btcusdt(char * fichier) {
	//
	BTCUSDT_t * ret = (BTCUSDT_t*)malloc(sizeof(BTCUSDT_t));

	//
	FILE * fp = fopen(fichier, "rb");
	ASSERT(fp != 0);
	FREAD(&ret->T, sizeof(uint), 1, fp);
	
	//
	uint LIGNES, D, N, P;
	FREAD(&LIGNES, sizeof(uint), 1, fp);
	FREAD(&D,      sizeof(uint), 1, fp);
	FREAD(&N,      sizeof(uint), 1, fp);
	FREAD(&P,      sizeof(uint), 1, fp);

	//
	ret->X = D * N * LIGNES;
	ret->Y = P;

	//
	float * x = alloc<float>(ret->T * ret->X);
	FREAD(x, sizeof(float), ret->T * ret->X, fp);
	ret->entrees__d = cpu_vers_gpu<float>(x, ret->X * ret->T);
	free(x);

	//
	float * y = alloc<float>(ret->T * ret->Y);
	FREAD(y, sizeof(float), ret->T * ret->Y, fp);
	ret->sorties__d = cpu_vers_gpu<float>(y, ret->Y * ret->T);
	free(y);

	//
	fclose(fp);

	printf("BTCUSDT : X=%i Y=%i T=%i\n", ret->X, ret->Y, ret->T);

	//
	return ret;
};

void liberer_btcusdt(BTCUSDT_t * donnee) {
	cudafree<float>(donnee->entrees__d);
	cudafree<float>(donnee->sorties__d);
};