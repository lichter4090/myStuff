/*********************************
* Class: MAGSHIMIM C2			 *
* Week:                			 *
* Name:                          *
* Credits:                       *
**********************************/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

float train[][2] = {
	{0, 0},
	{1, 4},
	{2, 8},
	{3, 12},
	{4, 16},
};

#define train_count (sizeof(train)/sizeof(train[0]))

float rand_float(void)
{
	return (float)rand() / (float)RAND_MAX;
}


float cost_func(float w, float b)
{
	// y = x*w; y - output, x - parameter, w - some number
	float x, y, d;
	float result = 0.0f;

	for (size_t i = 0; i < train_count; i++)
	{
		x = train[i][0];
		y = x * w + b;

		d = y - train[i][1];  // the distance
		result += d * d;
	}

	result /= train_count; // get the result

	return result;
}

int main(void)
{
	srand(time(0));
	float w = rand_float() * 10.0f;
	float b = rand_float() * 5.0f;

	float eps = 1e-3;
	float rate = 1e-3;
	float dw, db;
	float cost_try;



	printf("cost: %f, w: %f, b: %f\n", cost_func(w, b), w, b);


	for (size_t i = 0; i < train_count; i++)
	{
		printf("%f -> %f\n", train[i][0], (train[i][0] * w) + b);
	}


	for (size_t i = 0; i < 1000 * 1000; i++)
	{
		cost_try = cost_func(w, b);
		dw = (cost_func(w + eps, b) - cost_try) / eps;
		db = (cost_func(w, b + eps) - cost_try) / eps;

		w -= rate * dw;
		b -= rate * db;
	}



	printf("cost: %f, w: %f, b: %f\n", cost_func(w, b), w, b);


	for (size_t i = 0; i < train_count; i++)
	{
		printf("%f -> %f\n", train[i][0], (train[i][0] * w) + b);
	}


	getchar();
	return 0;
}
