#include "mdl.cuh"

#include "../../impl_template/tmpl_etc.cu"

//	-- Fichiez --
Mdl_t * cree_mdl_depuis_st_bin(char * fichier) {
	FILE * fp = FOPEN(fichier, "rb");
	//
	Mdl_t * ret = alloc<Mdl_t>(1);
	FREAD(&ret->insts, sizeof(uint), 1, fp);
	//
	ret->inst = alloc<Inst_t*>(ret->insts);
	FOR(0, i, ret->insts) {
		ret->inst[i] = lire_inst_pre_mdl(fp);
	};
	//
	FREAD(&ret->inst_entree, sizeof(uint), 1, fp);
	FREAD(&ret->inst_sortie, sizeof(uint), 1, fp);
	//printf("%i %i %i\n", ret->inst_entree, ret->inst_sortie, ret->insts);
	ASSERT(ret->inst_entree ==            0);
	ASSERT(ret->inst_sortie == ret->insts-1);
	//
	//ASSERT(feof(fp));
	fclose(fp);
	//
	mdl_optimisation(ret);
	//
	return ret;
};

Mdl_t * ouvrire_mdl(char * fichier) {
	FILE * fp = FOPEN(fichier, "rb");
	//
	Mdl_t * ret = alloc<Mdl_t>(1);
	FREAD(&ret->insts, sizeof(uint), 1, fp);
	//
	ret->inst = alloc<Inst_t*>(ret->insts);
	FOR(0, i, ret->insts) {
		ret->inst[i] = lire_inst(fp);
	};
	//
	FREAD(&ret->inst_entree, sizeof(uint), 1, fp);
	FREAD(&ret->inst_sortie, sizeof(uint), 1, fp);
	//
	//ASSERT(feof(fp));
	fclose(fp);
	//
	mdl_optimisation(ret);
	//
	return ret;
};

void ecrire_mdl(char * fichier, Mdl_t * mdl) {
	FILE * fp = FOPEN(fichier, "wb");
	//
	FWRITE(&mdl->insts, sizeof(uint), 1, fp);
	//
	FOR(0, i, mdl->insts) {
		ecrire_inst(fp, mdl->inst[i]);
	};
	//
	FWRITE(&mdl->inst_entree, sizeof(uint), 1, fp);
	FWRITE(&mdl->inst_sortie, sizeof(uint), 1, fp);
	//
	fclose(fp);
};

void liberer_mdl(Mdl_t * mdl) {
	FOR(0, i, mdl->insts) liberer_inst(mdl->inst[i]);
	free(mdl->inst);
	//
	FOR(0, i, mdl->BLOQUES) free(mdl->instructions[i]);
	free(mdl->instructions);
	free(mdl->elements);
	//
	free(mdl);
};

//	-- Verification --
void mdl_verif(Mdl_t * mdl, BTCUSDT_t * btcusdt) {
	ASSERT(mdl->inst[mdl->inst_entree]->ID == 0);

	FOR(0, i, mdl->insts) {
		FOR(0, j, inst_Xs[mdl->inst[i]->ID]) {
			if (i != mdl->inst_entree) {
				ASSERT(mdl->inst[i]->x_Y[j] == mdl->inst[mdl->inst[i]->x_pos[j]]->Y);
				//
				if (mdl->inst[i]->x_t[j] == 0) {
					ASSERT(mdl->inst[i]->x_pos[j] != i);	//en t=0 une inst peut pas s'auto x
				}
			}
		}
	}

	ASSERT(btcusdt->X == mdl->inst[mdl->inst_entree]->x_Y[0]);
	ASSERT(      1    == mdl->inst[mdl->inst_sortie]->Y     );
};