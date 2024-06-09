/*********************************
* Class: MAGSHIMIM C2			 *
* Week:                			 *
* Name:                          *
* Credits:                       *
**********************************/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>


float sigmoidf(float x)
{
	return 1.f / (1.f + expf(-x));
}

// OR - gate
float or_train[][3] = {
	{0, 0, 0},
	{0, 1, 1},
	{1, 0, 1},
	{1, 1, 1},
};

float and_train[][3] = {
	{0, 0, 0},
	{0, 1, 0},
	{1, 0, 0},
	{1, 1, 1},
};


float nand_train[][3] = {
	{0, 0, 1},
	{0, 1, 1},
	{1, 0, 1},
	{1, 1, 0},
};

float(* train)[3] = nand_train;
size_t train_count = 4;

#define train_count 4

float rand_float(void)
{
	return (float)rand() / (float)RAND_MAX;
}


float cost_func(float w1, float w2, float b)
{
	// y = x*w; y - output or or gate, x1, x2 - parameters, w - some number
	float x1, x2, y, d;
	float result = 0.0f;

	for (size_t i = 0; i < train_count; i++)
	{
		x1 = train[i][0];
		x2 = train[i][1];
		y = sigmoidf(x1 * w1 + x2 * w2 + b);

		d = y - train[i][2];  // the distance
		result += d * d;
	}

	result /= train_count; // get the result

	return result;
}

int main(void)
{
	srand(time(0));
	float w1 = rand_float();
	float w2 = rand_float();

	float bias = rand_float();

	float eps = 1e-1;
	float rate = 1e-1;
	float cost_func_result, dw1, dw2, db;

	for (size_t i = 0; i < 3000*1000; i++)
	{
		cost_func_result = cost_func(w1, w2, bias);
		//printf("w1: %f, w2: %f, bias: %f, cost func: %f\n", w1, w2, bias, cost_func_result);
		
		dw1 = (cost_func(w1 + eps, w2, bias) - cost_func_result) / eps;
		dw2 = (cost_func(w1, w2 + eps, bias) - cost_func_result) / eps;
		db = (cost_func(w1, w2, bias + eps) - cost_func_result) / eps;


		w1 -= rate * dw1;
		w2 -= rate * dw2;
		bias -= rate * db;
	}
	
	printf("w1: %f, w2: %f, bias: %f, cost func: %f\n", w1, w2, bias, cost_func(w1, w2, bias));

	for (size_t i = 0; i < 2; i++)
	{
		for (size_t j = 0; j < 2; j++)
		{
			printf("%zu | %zu = %f\n", i, j, sigmoidf(i * w1 + j * w2 + bias));
		}
	}


	getchar();
	return 0;
}
