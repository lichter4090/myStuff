// Gym is a GUI app that trains your neuron network with the data you give.
// After the learning, the program creates a binary file that could be loaded
// to a different program using nn.h

#define NN_IMPL
#define NN_ENABLE_IMAGE
#define NN_ENABLE_GYM
#define NN_ENABLE_ARCH_LOAD
#include "nn.h"

#include "stb_image_write.h"


#define WIDTH 1710
#define HEIGHT 900
#define FPS 60

#define STR_LEN 256



const size_t MAX_ITERATION = 1000 * 120;


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
	nnRand(network, -1, 1);

	useSig();

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
	float rate = 5;

	plot* cost_plot = plotAlloc();

	nnImage image = nnImageAlloc(28, 28, BLACK, 20);

	bool paused = false;
	
	cost_plot->max = nnCostFunc(network, input, output);

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
					cost_plot->data[cost_plot->size - 1] = nnCostFunc(network, input, output);
				}
				else
				{
					addCellToPlot(cost_plot);
					cost_plot->data[cost_plot->size - 1] = nnCostFunc(network, input, output);
				}

				i++;
			}
		}
		
		drawWindow(i, MAX_ITERATION, 3, PLOT_ARG, cost_plot, NN_ARG, network, NN_IMAGE_ARG, image);
	}

	CloseWindow();

	nnCheckValidness(network, input, output, false, 0.5) ? printf("100%% right network\n") : printf("Failed to get 100%% right\n");

	int size = 28;
	Mat* row = NULL;
	printf("NN image:\n");
	for (int i = 0; i < data->rows; i++)
	{
		if (i % size == 0)
		{
			printf("\n");
		}

		row = matGetRow(input, i);
		matCopy(NN_INPUT(network), row);
		matFree(row);

		nnForward(network);
		uint8_t pixel = (uint8_t)(MAT_AT(NN_OUTPUT(network), 0, 0) * 255.f);

		if (pixel)
		{
			printf("%3u", pixel);
		}
		else
		{
			printf("    ");
		}
	}

	printf("\nReal image:\n");
	for (int i = 0; i < data->rows; i++)
	{
		if (i % size == 0)
		{
			printf("\n");
		}

		uint8_t pixel = (uint8_t)(MAT_AT(output, i, 0) * 255.f);

		if (pixel)
		{
			printf("%3u", pixel);
		}
		else
		{
			printf("    ");
		}
	}

	int out_width = 512;
	int out_height = 512;
	uint8_t* out_pixels = malloc(sizeof(uint8_t) * out_width * out_height);

	if (!out_pixels)
	{
		exit(1);
	}

	for (int y = 0; y < out_height; y++)
	{
		for (int x = 0; x < out_width; x++)
		{
			MAT_AT(NN_INPUT(network), 0, 0) = (float)x / (out_width - 1);
			MAT_AT(NN_INPUT(network), 0, 1) = (float)y / (out_height - 1);

			nnForward(network);

			out_pixels[y * out_width + x] = (uint8_t)MAT_AT(NN_OUTPUT(network), 0, 0) * (uint8_t)255;
		}
	}

	const char* out_file_path = "img.png";
	if (!stbi_write_png(out_file_path, out_width, out_height, 1, out_pixels, out_width * sizeof(*out_pixels)))
	{
		fprintf(stderr, "Error: Could not save image %s as png\n", out_file_path);
		exit(1);
	}

	printf("Generated %s\n", out_file_path);



	nnFree(network);
	nnFree(gradient);

	matFree(data);
	matFree(input);
	matFree(output);

	free(arch);
	free(cost_plot);
	free(out_pixels);
	return 0;
}
