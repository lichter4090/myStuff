#define _CRT_SECURE_NO_WARNINGS

#define NN_IMPL
#include "nn.h"
#include <raylib.h>

#define BITS 3

#define MIN 0
#define MAX 1


#define WIDTH 800
#define HEIGHT 600


const int NEURON_RADIOS = 25;
const int layer_border_vpad = 50;
const int layer_border_hpad = 50;


void nnRenderRaylib(nn* network)
{
	size_t arch_count = network->num_of_layers + 1;
	int nn_height = HEIGHT - 2 * layer_border_vpad;
	int nn_width = WIDTH - 2 * layer_border_hpad; // the room for the network

	int layer_x = WIDTH / 2 - nn_width / 2;
	int layer_y = HEIGHT / 2 - nn_height / 2; // the start of the drawing

	int layer_hpad = nn_width / arch_count; // distance between layers
	int cx1, cy1, cx2, cy2, layer_vpad1, layer_vpad2;

	Color background_color = { 0x18, 0x18, 0x18, 0xFF };
	Color low_color = DARKPURPLE;
	Color high_color = GREEN;

	ClearBackground(background_color);

	for (size_t l = 0; l < arch_count; l++)
	{
		layer_vpad1 = nn_height / network->as[l]->cols; // distance between each neuron
		cx1 = layer_x + l * layer_hpad + layer_hpad / 2;

		for (size_t i = 0; i < network->as[l]->cols; i++)
		{
			cy1 = layer_y + i * layer_vpad1 + layer_vpad1 / 2;

			if (l + 1 < arch_count)
			{
				layer_vpad2 = nn_height / network->as[l + 1]->cols;
				for (size_t j = 0; j < network->as[l + 1]->cols; j++)
				{
					cx2 = layer_x + (l + 1) * layer_hpad + layer_hpad / 2;
					cy2 = layer_y + j * layer_vpad2 + layer_vpad2 / 2;

					high_color.a = floorf(255.f * sigmoidf(MAT_AT(network->ws[l], j, i)));
					DrawLine(cx1, cy1, cx2, cy2, ColorAlphaBlend(low_color, high_color, WHITE));
				}
			}

			switch (l)
			{
			case 0:
				DrawCircle(cx1, cy1, NEURON_RADIOS, LIGHTGRAY);
				break;

			default:
				high_color.a = floorf(255.f * sigmoidf(MAT_AT(network->bs[l - 1], 0, i)));
				DrawCircle(cx1, cy1, NEURON_RADIOS, ColorAlphaBlend(low_color, high_color, WHITE));
			}

		}
	}
}



int main(void)
{
	srand(time(NULL));
	size_t n = (1 << BITS);
	size_t rows = n * n;
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

	size_t arch[] = { 2 * BITS, BITS * 2 + 1, BITS + 1 };
	nn* network = nnAlloc(arch, ARR_LEN(arch));
	nn* gradient = nnAlloc(arch, ARR_LEN(arch));

	nnRand(network, MIN, MAX);

	size_t rate = 1;

	InitWindow(WIDTH, HEIGHT, "Neuron Network");
	SetTargetFPS(60);

	size_t i = 0;
	while (!WindowShouldClose())
	{
		if (i < 10 * 1000)
		{
			nnBackProp(network, gradient, input, output);
			nnApplyGradient(network, gradient, rate);
			i++;
		}

		if (i % 5 == 0)
		{
			BeginDrawing();
			{
				nnRenderRaylib(network);

				EndDrawing();
			}

			printf("i: %zu, Cost: %f\n", i, nnCostFunc(network, input, output));
		}
	}

	CloseWindow();

	bool ok = true;
	Mat* row = NULL;

	for (size_t i = 0; (i < output->rows); i++)
	{
		row = matGetRow(input, i);
		matCopy(NN_INPUT(network), row);
		nnForward(network);

		for (size_t j = 0; j < output->cols; j++)
		{
			MAT_AT(NN_OUTPUT(network), 0, j) = (MAT_AT(NN_OUTPUT(network), 0, j) > 0.5) ? 1 : 0;
		}

		for (size_t j = 0; j < output->cols; j++)
		{
			if ((int)MAT_AT(output, i, j) != (int)MAT_AT(NN_OUTPUT(network), 0, j))
			{
				ok = false;
				printf("Row: %zu\n", i);
			}
		}

		free(row);
	}
	
	
	(ok) ? printf("OK\n") : printf("Failed\n");

	nnPrintTruthTable(network, input, output, true);


	matFree(input);
	matFree(output);
	nnFree(network);
	nnFree(gradient);

	getchar();
	return 0;
}