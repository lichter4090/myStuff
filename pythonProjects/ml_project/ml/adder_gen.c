#define _CRT_SECURE_NO_WARNINGS

#define NN_IMPL
#include "nn.h"
#include <stdio.h>
#include <math.h>

#define BITS 4

#define MIN 0
#define MAX 1


int main(void)
{
	srand(time(NULL));
	size_t n = (1 << BITS);
	size_t rows = n * n;

	Mat* training = matAlloc(rows, BITS * 3 + 1);
	Mat* input = matAlloc(rows, BITS * 2);
	Mat* output = matAlloc(rows, BITS + 1);

	int sum = 0, iter = 0;
	float val = 0.0;

	for (size_t bit = 0; bit < BITS * 2; bit++)
	{
		sum = 0;
		val = 0.0;
		iter = pow(2, BITS * 2 - bit - 1);

		for (size_t i = 0; i < rows; i++)
		{
			MAT_AT(input, i, bit) = val;


			if ((i + 1) % iter == 0)
			{
				val = !val;
			}
		}
	}

	for (size_t j = 0; j < rows; j++)
	{
		sum = 0;
		
		for (size_t i = 0; i < BITS * 2; i++)
		{
			sum += pow(2, (BITS * 2 - i - 1) % BITS) * MAT_AT(input, j, i);
		}

		if (sum >= pow(2, BITS)) // if overflow
		{
			MAT_AT(output, j, BITS) = 1.0;
			sum = sum % (int)(pow(2, BITS) - 1);
		}
		else
		{
			MAT_AT(output, j, BITS) = 0.0;
		}


		for (size_t i = 0; i < BITS; i++)
		{
			if (sum - pow(2, BITS - i - 1) >= 0)
			{
				sum -= pow(2, BITS - i - 1);
				MAT_AT(output, j, i) = 1.0;
			}
			else
			{
				MAT_AT(output, j, i) = 0.0;
			}
		}
	}

	matMerge(training, input, output);

	const char* out_file_path = "adder.mat";
	FILE* out = fopen(out_file_path, "wb");

	if (!out)
	{
		fprintf(stderr, "Error: could not open file %s\n", out_file_path);
		exit(1);
	}
	printf("Saved the data to %s", out_file_path);

	matSave(out, training);
	fclose(out);

	matFree(input);
	matFree(output);
	matFree(training);

	getchar();
	return 0;
}