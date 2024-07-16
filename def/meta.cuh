#pragma once

#include "etc.cuh"

//	Les Parantèses () sont importantes.

#define GRAND_T 16

#define MEGA_T (24)

#define t_MODE(t, mega_t) ( (t)*MEGA_T + (mega_t) )