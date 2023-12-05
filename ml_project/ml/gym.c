// Gym is a GUI app that trains your neuron network with the data you give.
// After the learning, the program creates a binary file that could be loaded
// to a different program using nn.h


#define _CRT_SECURE_NO_WARNINGS

#define NN_IMPL
#define NN_ENABLE_GYM
#define NN_ENABLE_ARCH_LOAD
#include "nn.h"

#define WIDTH 1200
#define HEIGHT 900
#define FPS 60


const size_t MAX_ITERATION = 1000 * 50;



int main(int argc, char** argv)
{
	srand((unsigned int)time(NULL));
	const char* program = args_shift(&argc, &argv);

	if (argc <= 0)
	{
		fprintf(stderr, "Usage: program <architecture file path> <data file path>\n");
		fprintf(stderr, "Error: no architecture file was provided\n");
		exit(1);
	}

	const char* arch_file_path = args_shift(&argc, &argv);

	if (argc <= 0)
	{
		fprintf(stderr, "Usage: program <architecture file path> <data file path>\n");
		fprintf(stderr, "Error: no data file was provided\n");
		exit(1);
	}

	const char* data_file_path = args_shift(&argc, &argv);

	size_t arch_size = 0;
	size_t* arch = loadArchFromFile(arch_file_path, &arch_size);

	nn* network = nnAlloc(arch, arch_size);
	nn* gradient = nnAlloc(arch, arch_size);
	nnRand(network, 0, 0.1);

	FILE* in = fopen(data_file_path, "rb");

	if (!in)
	{
		fprintf(stderr, "Error: could not open data file %s\n", data_file_path);
		exit(1);
	}

	Mat* data = matLoad(in);
	fclose(in);


	size_t input_size = arch[0];
	size_t output_size = arch[arch_size - 1];

	if (data->cols != input_size + output_size)
	{
		fprintf(stderr, "Error: invalid architecture\n");
		exit(1);
	}

	Mat* input = matAlloc(data->rows, input_size);
	Mat* output = matAlloc(data->rows, output_size);

	matSplit(data, input, output, input_size);


	createWindow(WIDTH, HEIGHT, FPS);

	size_t i = 0;
	float rate = 0.00000000000001;

	useSig(false);

	plot* cost_plot = plotAlloc();

	bool paused = false;
	
	nnPrintTruthTable(network, input, output, false);

	while (!WindowShouldClose() && i < MAX_ITERATION)
	{
		if (i < MAX_ITERATION)
		{
			if (IsKeyPressed(KEY_SPACE))
			{
				paused = !paused;
			}

			for (size_t j = 0; j < 103 && i < MAX_ITERATION && !paused; j++)
			{
				nnBackProp(network, gradient, input, output);
				nnApplyGradient(network, gradient, rate);

				if (cost_plot->size > GRAPH_SIZE)
				{
					shiftLeftPlot(cost_plot);
				}
				else
				{
					addCellToPlot(cost_plot);
				}
				addValueToPlot(cost_plot, nnCostFunc(network, input, output));

				i++;
			}
		}

		drawWindow(i, MAX_ITERATION, 2, PLOT_ARG, cost_plot, NN_ARG, network);
	}
	CloseWindow();
	
	//nnCheckValidness(network, input, output, false, 0.5) ? printf("100%% right network\n") : printf("Failed to get 100%% right\n");
	nnPrintTruthTable(network, input, output, false);

	nnFree(network);
	nnFree(gradient);

	matFree(data);
	matFree(input);
	matFree(output);

	free(arch);
	free(cost_plot);

	return 0;
}