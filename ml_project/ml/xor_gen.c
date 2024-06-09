#define _CRT_SECURE_NO_WARNINGS

#define NN_IMPL
#include "nn.h"
#include <stdio.h>


int main(void)
{	
	const char* out_file_path = "simple.mat";
	size_t row = 0;
	Mat* training = matAlloc(4, 2);
	FILE* out = NULL;

	for (size_t i = 0; i < 4; i++)
	{
		for (size_t j = 0; j < 2; j++)
		{
			row = i * 2 + j;
			MAT_AT(training, row, 0) = i;
			MAT_AT(training, row, 1) = j;
			MAT_AT(training, row, 2) = i^j;
		}
	}

	out = fopen(out_file_path, "wb");

	if (!out)
	{
		fprintf(stderr, "Error: could not open file %s\n", out_file_path);
		exit(1);
	}
	printf("Saved the data to %s", out_file_path);

	matSave(out, training);
	fclose(out);

	matFree(training);

	getchar();
	return 0;
}