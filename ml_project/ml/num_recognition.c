#define _CRT_SECURE_NO_WARNINGS

#define NN_IMPL
#define NN_ENABLE_ARCH_LOAD
#include "nn.h"


const size_t MAX_ITERATION = 10000;

void validate(nn* network, Mat* test_input, Mat* test_output)
{
	Mat* row_of_input = NULL;
	int stats = 0;

	for (size_t i = 0; i < test_input->rows; i++)
	{
		row_of_input = matGetRow(test_input, i);

		matCopy(NN_INPUT(network), row_of_input);
		matFree(row_of_input);

		nnForward(network);

		int actual_num = 0;
		int nn_thinks_that = 0;
		int grade = 0;

		for (size_t j = 0; j < test_output->cols; j++)
		{
			if (MAT_AT(test_output, i, j) == 1)
				actual_num = (int)j;
		}

		for (size_t j = 0; j < test_output->cols; j++)
		{
			if (MAT_AT(NN_OUTPUT(network), i, j) > grade)
				nn_thinks_that = (int)j;
		}

		if (actual_num == nn_thinks_that)
		{
			stats++;
		}
	}

	printf("Validate=%.2f\n", (float)stats / test_input->rows);
}


int main(int argc, char** argv)
{
	srand((unsigned int)time(NULL));
	const char* program = args_shift(&argc, &argv);

	if (argc <= 0)
	{
		fprintf(stderr, "Usage: program <architecture file path> <data file path> <test file path>\n");
		fprintf(stderr, "Error: no architecture file was provided\n");
		exit(1);
	}

	const char* arch_file_path = args_shift(&argc, &argv);

	if (argc <= 0)
	{
		fprintf(stderr, "Usage: program <architecture file path> <data file path> <test file path>\n");
		fprintf(stderr, "Error: no data file was provided\n");
		exit(1);
	}

	const char* data_file_path = args_shift(&argc, &argv);

	if (argc <= 0)
	{
		fprintf(stderr, "Usage: program <architecture file path> <data file path> <test file path>\n");
		fprintf(stderr, "Error: no test file was provided\n");
		exit(1);
	}

	const char* test_file_path = args_shift(&argc, &argv);

	size_t arch_size = 0;
	size_t* arch = loadArchFromFile(arch_file_path, &arch_size);

	nn* network = nnAlloc(arch, arch_size);
	nn* gradient = nnAlloc(arch, arch_size);
	nnRand(network, -1, 1);

	FILE* in = fopen(data_file_path, "rb");
	FILE* test_in = fopen(test_file_path, "rb");

	if (!in)
	{
		fprintf(stderr, "Error: could not open data file %s\n", data_file_path);
		exit(1);
	}

	if (!test_in)
	{
		fprintf(stderr, "Error: could not open test file %s\n", test_file_path);
		fclose(in);
	}

	Mat* data = matLoad(in);
	Mat* test = matLoad(test_in);

	fclose(in);
	fclose(test_in);

	size_t input_size = arch[0];
	size_t output_size = arch[arch_size - 1];

	if (data->cols != input_size + output_size)
	{
		fprintf(stderr, "Error: invalid architecture\n");
		exit(1);
	}

	Mat* input = matAlloc(data->rows, input_size);
	Mat* output = matAlloc(data->rows, output_size);

	Mat* test_input = matAlloc(test->rows, input_size);
	Mat* test_output = matAlloc(test->rows, output_size);

	matSplit(data, input, output, input_size);
	matSplit(test, test_input, test_output, input_size);


	float rate = 0.001;

	useRelu();
	printf("%d\n", (int)input->rows);
	for (size_t i = 0; i < MAX_ITERATION; i++)
	{
		nnBackProp(network, gradient, input, output);
		nnApplyGradient(network, gradient, rate);

		if (i % 10 == 0)
		{
			printf("cost=%f, epoch=%zu\n", nnCostFunc(network, input, output), i);
			validate(network, test_input, test_output);
		}
	}


	Mat* row_of_input = NULL;
	int stats = 0;

	for (size_t i = 0; i < test_input->rows; i++)
	{
		row_of_input = matGetRow(test_input, i);

		matCopy(NN_INPUT(network), row_of_input);
		matFree(row_of_input);

		nnForward(network);

		int actual_num = 0;
		int nn_thinks_that = 0;
		int grade = 0;

		for (size_t j = 0; j < test_output->cols; j++)
		{
			if (MAT_AT(test_output, i, j) == 1)
				actual_num = (int)j;
		}

		for (size_t j = 0; j < test_output->cols; j++)
		{
			if (MAT_AT(NN_OUTPUT(network), i, j) > grade)
				nn_thinks_that = (int)j;
		}

		printf("\nReal number was %d and the nn though it was %d ", actual_num, nn_thinks_that);

		if (actual_num == nn_thinks_that)
		{
			printf("Got it Right!!!");
			stats++;
		}
		printf("\n");
	}

	printf("Managed to get %d/%zu\n", stats, test_input->rows);

	nnFree(network);
	nnFree(gradient);

	matFree(data);
	matFree(input);
	matFree(output);

	matFree(test);
	matFree(test_input);
	matFree(test_output);

	free(arch);

	getchar();
	return 0;
}