#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>


// (x|y) & !(x&y) = xor

#define NUM_OF_PARAMS 9 // three neurons that each has two weights (for each binary number) and a bias


float xor_train[][3] = {
	{0, 0, 0},
	{0, 1, 1},
	{1, 0, 1},
	{1, 1, 0},
};

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


float nor_train[][3] = {
	{0, 0, 1},
	{0, 1, 0},
	{1, 0, 0},
	{1, 1, 0},
};


float(*train)[3] = xor_train;
size_t train_count = 4;


float sigmoidf(float x)
{
	return 1.f / (1.f + expf(-x));
}


float forward(float gates[], float x1, float x2)
{
	float or_result = sigmoidf(gates[0] * x1 + gates[1] * x2 + gates[2]);
	float nand_result = sigmoidf(gates[3] * x1 + gates[4] * x2 + gates[5]);
	
	return sigmoidf(gates[6] * or_result + gates[7] * nand_result + gates[8]);
}


float cost_func(float gates[])
{
	float x1, x2, y, d;
	float result = 0.0f;

	for (size_t i = 0; i < train_count; i++)
	{
		x1 = train[i][0];
		x2 = train[i][1];
		y = forward(gates, x1, x2);

		d = y - train[i][2];  // the distance
		result += d * d;
	}

	result /= train_count; // get the result

	return result;
}


float rand_float(void)
{
	return (float)rand() / (float)RAND_MAX;
}


float* rand_xor()
{
	float* m = (float*)malloc(sizeof(float) * NUM_OF_PARAMS);

	if (m == NULL)
	{
		exit(1);
	}

	for (size_t i = 0; i < NUM_OF_PARAMS; i++)
	{
		m[i] = rand_float();
	}

	return m;
}


void print_xor(float m[])
{
	for (size_t i = 0; i < NUM_OF_PARAMS; i++)
	{
		printf("Param %zu: %f\n", i, m[i]);

		if ((i + 1) % 3 == 0)
		{
			printf("\n");
		}
	}
}


float* finite_diff(float current_gates[], float eps) // function returns new array with all the slopes
{
	float current_distance = cost_func(current_gates);
	float* slopes_arr = (float*)malloc(sizeof(float) * NUM_OF_PARAMS);
	float saved;

	if (!slopes_arr)
	{
		exit(1);
	}

	for (size_t i = 0; i < NUM_OF_PARAMS; i++)
	{
		saved = current_gates[i];

		current_gates[i] += eps;
		slopes_arr[i] = (cost_func(current_gates) - current_distance) / eps;
		current_gates[i] = saved;
	}

	return slopes_arr;
}


int main(void)
{
	srand(time(NULL));
	float* gates = rand_xor();
	float* slopes = NULL;
	float rate = 1e-1, eps = 1e-1;

	for (size_t i = 0; i < 100 * 1000; i++)
	{
		slopes = finite_diff(gates, eps);

		for (size_t j = 0; j < NUM_OF_PARAMS; j++)
		{
			gates[j] -= slopes[j] * rate;
		}
		free(slopes);
	}
	printf("cost: %f\n", cost_func(gates));
	printf("------------------------\n");
	printf("weights:\n");
	print_xor(gates);
	printf("------------------------\n");
	printf("selected gate:\n");
	for (size_t i = 0; i < 2; i++)
	{
		for (size_t j = 0; j < 2; j++)
		{
			printf("%zu | %zu = %f\n", i, j, forward(gates, i, j));
		}
	}

	printf("------------------------\n");
	printf("1st neorun:\n");
	for (size_t i = 0; i < 2; i++)
	{
		for (size_t j = 0; j < 2; j++)
		{
			printf("%zu | %zu = %f\n", i, j, sigmoidf(gates[0] * i + gates[1] * j + gates[2]));
		}
	}

	printf("------------------------\n");
	printf("2nd neorun:\n");
	for (size_t i = 0; i < 2; i++)
	{
		for (size_t j = 0; j < 2; j++)
		{
			printf("%zu | %zu = %f\n", i, j, sigmoidf(gates[3] * i + gates[4] * j + gates[5]));
		}
	}

	printf("------------------------\n");
	printf("3rd neorun:\n");
	for (size_t i = 0; i < 2; i++)
	{
		for (size_t j = 0; j < 2; j++)
		{
			printf("%zu | %zu = %f\n", i, j, sigmoidf(gates[6] * i + gates[7] * j + gates[8]));
		}
	}

	free(gates);
	getchar();
	return 0;
}