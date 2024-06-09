#define _CRT_SECURE_NO_WARNINGS

#define NN_IMPL
#include "nn.h"
#include <stdio.h>


#define ROWS 4

int main(void)
{
	const char* out_file_path = "data/snake.mat";
	const int con = 3;
	size_t row = 0;
	Mat* training = matAlloc(ROWS, 2);
	FILE* out = NULL;

	float arr[] = { 24, 0, 26, 5, 31, 10, 52, 15 };

	matInitArr(training, arr, 8);

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

	return 0;
}