#define NN_IMPL
#include "nn.h"


#include <crtdbg.h>

#define _CRTDBG_MAP_ALLOC


#define MIN 0
#define MAX 1

float input_arr[] = { 0, 0, 0, 1, 1, 0, 1, 1 };
float output_arr[] = { 0, 1, 1, 1 };


int main(void)
{
	srand(time(NULL));

	float rate = 1e-1;

	size_t arch[] = { 2, 2, 1 };
	nn* network = nnAlloc(arch, ARR_LEN(arch));
	nn* gradient = nnAlloc(arch, ARR_LEN(arch));

	NN_PRINT(network);
	getchar();
	return 0;

	Mat* input = matAlloc(4, 2);
	Mat* output = matAlloc(4, 1);

	matInitArr(input, input_arr, ARR_LEN(input_arr));
	matInitArr(output, output_arr, ARR_LEN(output_arr));

	nnRand(network, MIN, MAX);

	for (size_t i = 0; i < 1000; i++)
	{
		nnBackProp(network, gradient, input, output);
		nnApplyGradient(network, gradient, rate);
	}

	nnPrintTruthTable(network, input, output, true);

	matFree(output);
	matFree(input);
	nnFree(network);
	nnFree(gradient);

	printf("Leaks: %d", _CrtDumpMemoryLeaks());
	getchar();
	return 0;
}