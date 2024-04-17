#define NN_IMPL

#include "nn.h"
#include <raylib.h>

#define WIDTH 800
#define HEIGHT 600


#define FILE_NAME "nn.png"


const int NEURON_RADIOS = 25;
const int layer_border_vpad = 50;
const int layer_border_hpad = 50;


void nn_render(nn* network)
{
	size_t arch_count = network->num_of_layers + 1;
	int nn_height = HEIGHT - 2 * layer_border_vpad;
	int nn_width = WIDTH - 2 * layer_border_hpad; // the room for the network

	int layer_x = WIDTH / 2 - nn_width / 2;
	int layer_y = HEIGHT / 2 - nn_height / 2; // the start of the drawing

	int layer_hpad = nn_width / arch_count; // distance between layers
	int cx1, cy1, cx2, cy2, layer_vpad1, layer_vpad2;

	InitWindow(WIDTH, HEIGHT, "Neuron Network");
	SetTargetFPS(60);
	
	while (!WindowShouldClose())
	{
		for (size_t l = 0; l < arch_count; l++)
		{
			BeginDrawing();
			{
				ClearBackground(DARKGRAY);
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

							DrawLine(cx1, cy1, cx2, cy2, GREEN);
						}
					}

					switch (l)
					{
					case 0:
						DrawCircle(cx1, cy1, NEURON_RADIOS, LIGHTGRAY);
						break;

					default:
						DrawCircle(cx1, cy1, NEURON_RADIOS, RED);
					}

				}
				EndDrawing();
			}
		}
	}
	
	CloseWindow();
}


int main(void)
{
	srand(time(0));

	size_t arch[] = { 3, 9, 9, 1};
	size_t arch_count = ARR_LEN(arch);

	nn* network = nnAlloc(arch, arch_count);
	nnRand(network, -10, 10);

	nn_render(network);

	nnFree(network);
	return 0;
}