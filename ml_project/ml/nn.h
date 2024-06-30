#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <stdbool.h>
#include <string.h>
#include <stdarg.h>
#include <stdint.h>


#ifndef NN_H
#define NN_H

typedef struct Mat
{
	size_t rows;
	size_t cols;
	float* es;
} Mat;


typedef struct nn
{
	size_t num_of_layers;
	Mat** ws;
	Mat** bs;
	Mat** as;
	
} nn;


float rand_float();
float sigmoidf(float x);

Mat* matAlloc(size_t raws, size_t cols);//returns a pointer to a matrix in size rows*cols with allocated array in the right size
void matRand(Mat* m, float low, float high);//randomises a matrix's data
void matFill(Mat* m, float num);//fills a matrix with a specific number
void matInitArr(Mat* m, float arr[], size_t size);//init data of an array to a matrix
void matDot(Mat* dst, Mat* a, Mat* b);//multiplys two matrixes and puts the solution in the dst matrix
void matSum(Mat* dst, Mat* a);//sums two matrixes and puts the solution in the dst matrix
Mat* matGetRow(Mat* m, size_t row_num);//returns matrix that is made out a single row of a certin matrix
void matCopy(Mat* dst, Mat* src);//copys data of the src matrix to the dst matrix
void matPrint(Mat* m, char* name, size_t padding);//prints a matrix
void matSig(Mat* m);//runs the sigmoid function on all of the matrix's data
void matRelu(Mat* m);// runs the relu function on all of the matrx's data
void matMerge(Mat* output, Mat* m1, Mat* m2); // function for merging matrixes (combines from the columns), opposite of matSplit
void matSplit(Mat* complete_mat, Mat* m1, Mat* m2, size_t col_num); // function splits a matrix into two matrixes (splits by the columns)
void matSave(FILE* output_file, Mat* matrix); // function for saving a matrix in a file
Mat* matLoad(FILE* input_file); // function for loading a matrix from a file (copying it to the given pointer)
void matShuffleRows(Mat* m); // function for shuffling matrix's row
void matAddRow(Mat* m); // add row at end of mat
void matFree(Mat* m);//frees the dynamiclly allocated data of a matrix


nn* nnAlloc(size_t* arch, size_t arch_count);//returns a pointer to a neuron network in size of the given array (if the array is {2, 2, 1} then the network will be made out of 2 neurons connected to aonther tow neurons connected to one neuron)
void nnFill(nn* network, float num);
void nnRand(nn* network, float low, float high);//randomises a neuron network's data (only the weights and biases)
void nnPrint(nn* network, char* name);//prints a neuron network
void nnForward(nn* network);//gets the output of the machine (based on its current parameters)
float nnCostFunc(nn* network, Mat* input, Mat* output);//returns the distance of the current output of the machine from the real output (should be 0)
void nnFiniteDiff(nn* network, nn* gradient, Mat* input, Mat* output, float eps);//intis the slopes of each parameter based on the cost function to the gradient neuron network (the gradient neuron network must be in the same size as the network of the parameters
void nnBackProp(nn* network, nn* gradient, Mat* input, Mat* output);
void nnApplyGradient(nn* network, nn* gradient, float rate);//function changes the parameters of a neuron network based on the gradient that were most likely calculated from the nnFIniteDiff() function
void nnPrintTruthTable(nn* network, Mat* input, Mat* output, bool print_as_bits);//prints the truth table of the given inputs and the outcomes of the machine
bool nnCheckValidness(nn* network, Mat* input, Mat* output, bool binary_flag, float eps); // function returns true if the network's output for each row of the input is the same as the output
void nnFree(nn* network);//frees the dynamiclly allocated data of a network



#define MAT_AT(m, r, c) (m)->es[(r)*(m)->cols + (c)]
#define MAT_PRINT(m) matPrint((m), #m, 0);
#define NN_PRINT(n) nnPrint((n), #n);
#define ARR_LEN(arr) sizeof((arr)) / sizeof((arr)[0])

#define NN_INPUT(n) (n)->as[0]
#define NN_OUTPUT(n) (n)->as[(n)->num_of_layers]


#endif // !NN_H

#ifdef NN_IMPL

bool USE_SIG = false;
bool USE_RELU = false;


void useSig()
{
	if (USE_RELU)
	{
		fprintf(stderr, "Already using relu");
		exit(1);
	}

	USE_SIG = true;
	USE_RELU = false;
}

void useRelu()
{
	if (USE_SIG)
	{
		fprintf(stderr, "Already using sigmoid");
		exit(1);
	}

	USE_RELU = true;
	USE_SIG = false;
}


float rand_float(void)
{
	return (float)rand() / (float)RAND_MAX;
}


float sigmoidf(float x)
{
	return 1.f / (1.f + expf(-x));
}

float reluf(float x)
{
	if (x > 0)
	{
		return x;
	}

	return 0.0;
}


void matFill(Mat* m, float num)
{
	for (size_t rows = 0; rows < m->rows; rows++)
	{
		for (size_t cols = 0; cols < m->cols; cols++)
		{
			MAT_AT(m, rows, cols) = num;
		}
	}
}


void matInitArr(Mat* m, float arr[], size_t size)
{
	for (size_t i = 0; i < size; i++)
	{
		MAT_AT(m, 0, i) = arr[i];
	}
}


Mat* matAlloc(size_t rows, size_t cols)
{
	Mat* m = (Mat*)malloc(sizeof(Mat));

	if (m == NULL)
	{
		exit(1);
	}

	m->rows = rows;
	m->cols = cols;
	m->es = (float*)malloc(sizeof(*(m->es)) * rows * cols);

	if (m->es == NULL)
	{
		free(m);
		exit(1);
	}

	return m;
}


void matRand(Mat* m, float low, float high)
{
	for (size_t rows = 0; rows < m->rows; rows++)
	{
		for (size_t cols = 0; cols < m->cols; cols++)
		{
			MAT_AT(m, rows, cols) = rand_float() * (high - low) + low;
		}
	}
}


void matDot(Mat* dst, Mat* a, Mat* b)
{
	if (a->cols != b->rows || dst->rows != a->rows || dst->cols != b->cols)
	{
		exit(1);
	}

	size_t n = a->cols;

	for (size_t rows = 0; rows < dst->rows; rows++)
	{
		for (size_t cols = 0; cols < dst->cols; cols++)
		{
			MAT_AT(dst, rows, cols) = 0;
			for (size_t i = 0; i < n; i++)
			{
				MAT_AT(dst, rows, cols) += MAT_AT(a, rows, i) * MAT_AT(b, i, cols);
			}
		}
	}
}


void matSum(Mat* dst, Mat* a)
{
	if (dst->rows != a->rows || dst->cols != a->cols)
	{
		exit(1);
	}

	for (size_t rows = 0; rows < dst->rows; rows++)
	{
		for (size_t cols = 0; cols < dst->cols; cols++)
		{
			MAT_AT(dst, rows, cols) += MAT_AT(a, rows, cols);
		}
	}
}


Mat* matGetRow(Mat* m, size_t row_num)
{
	Mat* row = matAlloc(1, m->cols);

	for (size_t i = 0; i < m->cols; i++)
	{
		row->es[i] = MAT_AT(m, row_num, i);
	}

	return row;
}


void matCopy(Mat* dst, Mat* src)
{
	if (dst->rows != src->rows || dst->cols != src->cols)
	{
		exit(1);
	}
	
	for (size_t row = 0; row < src->rows; row++)
	{
		for (size_t col = 0; col < src->cols; col++)
		{
			MAT_AT(dst, row, col) = MAT_AT(src, row, col);
		}
	}

}


void matPrint(Mat* m, char* name, size_t padding)
{
	printf("%*s%s: [\n", (int)padding, "", name);

	for (size_t rows = 0; rows < m->rows; rows++)
	{
		printf("%*s    ", (int)padding, "");
		for (size_t cols = 0; cols < m->cols; cols++)
		{
			printf("%f ", MAT_AT(m, rows, cols));
		}
		printf("\n");
	}
	printf("%*s]\n", (int)padding, "");
}


void matSig(Mat* m)
{
	for (size_t rows = 0; rows < m->rows; rows++)
	{
		for (size_t cols = 0; cols < m->cols; cols++)
		{
			MAT_AT(m, rows, cols) = sigmoidf(MAT_AT(m, rows, cols));
		}
	}
}

void matRelu(Mat* m)
{
	for (size_t rows = 0; rows < m->rows; rows++)
	{
		for (size_t cols = 0; cols < m->cols; cols++)
		{
			MAT_AT(m, rows, cols) = reluf(MAT_AT(m, rows, cols));
		}
	}
}


void matMerge(Mat* output, Mat* m1, Mat* m2)
{
	if (m1->rows != m2->rows || output->rows != m1->rows || output->cols != m1->cols + m2->cols)
	{
		printf("Error: merging matrixes");
		exit(1);
	}


	for (size_t i = 0; i < output->rows; i++)
	{
		for (size_t j = 0; j < m1->cols; j++)
		{
			MAT_AT(output, i, j) = MAT_AT(m1, i, j);
		}

		for (size_t j = 0; j < m2->cols; j++)
		{
			MAT_AT(output, i, j + m1->cols) = MAT_AT(m2, i, j);
		}
	}
}


void matSplit(Mat* complete_mat, Mat* m1, Mat* m2, size_t col_num)
{
	if (col_num >= complete_mat->cols || m1->rows != m2->rows || complete_mat->rows != m1->rows || complete_mat->cols != m1->cols + m2->cols)
	{
		printf("Error: spliting matrixes");
		exit(1);
	}

	for (size_t i = 0; i < complete_mat->rows; i++)
	{
		for (size_t j = 0; j < col_num; j++)
		{
			MAT_AT(m1, i, j) = MAT_AT(complete_mat, i, j);
		}

		for (size_t j = col_num; j < complete_mat->cols; j++)
		{
			MAT_AT(m2, i, j - col_num) = MAT_AT(complete_mat, i, j);
		}
	}
}


void matSave(FILE* output_file, Mat* matrix)
{
	const char* magic = "nn.h.mat";
	size_t num_of_elements = matrix->cols;
	size_t n, m;

	fwrite(magic, strlen(magic), 1, output_file);
	fwrite(&(matrix->rows), sizeof(matrix->rows), 1, output_file);
	fwrite(&(matrix->cols), sizeof(matrix->cols), 1, output_file);
	

	for (size_t i = 0; i < matrix->rows; i++)
	{
		n = fwrite(&MAT_AT(matrix, i, 0), sizeof(*(matrix->es)), num_of_elements, output_file);
		
		while (n < num_of_elements && !ferror(output_file))
		{
			m = fwrite(matrix->es + n, sizeof(*(matrix->es)), num_of_elements - n, output_file);

			n += m;
		}
	}
}


Mat* matLoad(FILE* input_file)
{
	char magic[256] = "";
	char magic_should_be[] = "nn.h.mat";
	char ch = ' ';

	size_t n, m, rows, cols;
	Mat* new_matrix = NULL;

	fread(&magic, strlen(magic_should_be), 1, input_file);

	if (strcmp(magic, magic_should_be))
	{
		printf("Failed to load matrix\n");
		exit(1);
	}

	fread(&rows, sizeof(rows), 1, input_file);
	fread(&cols, sizeof(cols), 1, input_file);

	new_matrix = matAlloc(rows, cols);

	n = fread(new_matrix->es, sizeof(*new_matrix->es), rows * cols, input_file);
	while (n < rows * cols && !ferror(input_file))
	{
		m = fread(new_matrix->es, sizeof(*new_matrix->es) + n, rows * cols - n, input_file);
		n += m;
	}

	return new_matrix;
}


void matShuffleRows(Mat* m)
{
	size_t rand_num = 0;
	float temp;

	for (size_t i = 0; i < m->rows; i++)
	{
		rand_num = i + rand() % (m->rows - i);

		for (size_t j = 0; (j < m->cols) && (i != rand_num); j++)
		{
			temp = MAT_AT(m, i, j);

			MAT_AT(m, i, j) = MAT_AT(m, rand_num, j);
			MAT_AT(m, rand_num, j) = temp;
		}
	}
}

void matAddRow(Mat* m)
{
	m->rows += 1;

	m->es = (float*)realloc(m->es, sizeof(*(m->es)) * m->rows * m->cols);
	
	if (!m->es)
	{
		fprintf(stderr, "Error allocating more row");
		exit(1);
	}

	for (size_t i = 0; i < m->cols; i++)
	{
		MAT_AT(m, m->rows - 1, i) = 0;
	}
}


void matFree(Mat* m)
{
	free(m->es);
	free(m);
}


nn* nnAlloc(size_t* arch, size_t arch_count)
{
	if (arch_count <= 0)
	{
		exit(1);
	}
	
	nn* new_network = (nn*)malloc(sizeof(nn));

	if (new_network == NULL)
	{
		exit(1);
	}
	
	new_network->num_of_layers = arch_count - 1;

	new_network->ws = (Mat**)malloc(sizeof(Mat*) * new_network->num_of_layers);
	new_network->bs = (Mat**)malloc(sizeof(Mat*) * new_network->num_of_layers);
	new_network->as = (Mat**)malloc(sizeof(Mat*) * arch_count);

	if (new_network->ws == NULL || new_network->bs == NULL || new_network->as == NULL)
	{
		nnFree(new_network);
		exit(1);
	}

	new_network->as[0] = matAlloc(1, arch[0]);
	matFill(new_network->as[0], 0);

	for (int i = 1; i < arch_count; i++)
	{
		new_network->ws[i - 1] = matAlloc(new_network->as[i - 1]->cols, arch[i]);
		new_network->bs[i - 1] = matAlloc(1, arch[i]);
		new_network->as[i] = matAlloc(1, arch[i]);

		matFill(new_network->ws[i - 1], 0);
		matFill(new_network->bs[i - 1], 0);
		matFill(new_network->as[i], 0);
	}	

	return new_network;
}


void nnFill(nn* network, float num)
{
	for (size_t layer = 0; layer < network->num_of_layers; layer++)
	{
		matFill(network->ws[layer], num);
		matFill(network->bs[layer], num);
		matFill(network->as[layer], num);
	}
	matFill(NN_OUTPUT(network), num);
}


void nnRand(nn* network, float low, float high)
{
	for (size_t i = 0; i < network->num_of_layers; i++)
	{
		matRand(network->ws[i], low, high);
		matRand(network->bs[i], low, high);
	}
}


void nnPrint(nn* network, char* name)
{
	char buf[256] = "";

	printf("%s: [\n", name);
	for (size_t i = 0; i < network->num_of_layers; i++)
	{
		snprintf(buf, 256, "w%zu", i);
		matPrint(network->ws[i], buf, 4);

		snprintf(buf, 256, "b%zu", i);
		matPrint(network->bs[i], buf, 4);
	}
	printf("]\n");
}


void nnForward(nn* network)
{
	for (size_t i = 0; i < network->num_of_layers; i++)
	{
		matDot(network->as[i + 1], network->as[i], network->ws[i]);
		matSum(network->as[i + 1], network->bs[i]);

		if (network->num_of_layers - 1 == i)
		{
			matSig(network->as[i + 1]);
			continue;
		}

		if (USE_SIG)
		{
			matSig(network->as[i + 1]);
		}

		if (USE_RELU)
		{
			matRelu(network->as[i + 1]);
		}


		//for (int i = 0; i < 784; i++)
		//{
		//	if (i % 28 == 0)
		//	{
		//		printf("\n");
		//	}
		//
		//	uint8_t pixel = (uint8_t)(MAT_AT(NN_INPUT(network), 0, i) * 255.f);
		//
		//	if (pixel)
		//	{
		//		printf("%3u", pixel);
		//	}
		//	else
		//	{
		//		printf("    ");
		//	}
		//}
		//
		//
		//MAT_PRINT(NN_OUTPUT(network));
	}
}


float nnCostFunc(nn* network, Mat* input, Mat* output)
{
	if (input->rows != output->rows || output->cols != NN_OUTPUT(network)->cols)
	{
		exit(1);
	}
	
	float d;
	float result = 0.0f;
	Mat* row_of_input = NULL;

	for (size_t i = 0; i < input->rows; i++)
	{
		row_of_input = matGetRow(input, i);
		matCopy(NN_INPUT(network), row_of_input);
		matFree(row_of_input);

		nnForward(network);

		for (size_t j = 0; j < output->cols; j++)
		{
			d = MAT_AT(NN_OUTPUT(network), 0, j) - MAT_AT(output, i, j);
			result += d * d;
		}
	}
	result /= input->rows;

	return result;
}


void nnFiniteDiff(nn* network, nn* gradient, Mat* input, Mat* output, float eps)
{	
	float current_diff = nnCostFunc(network, input, output);
	float saved;

	
	for (size_t mat_idx = 0; mat_idx < network->num_of_layers; mat_idx++)
	{
		for (size_t row = 0; row < network->ws[mat_idx]->rows; row++)// improve weights
		{
			for (size_t col = 0; col < network->ws[mat_idx]->cols; col++)
			{
				saved = MAT_AT(network->ws[mat_idx], row, col);

				MAT_AT(network->ws[mat_idx], row, col) += eps;
				MAT_AT(gradient->ws[mat_idx], row, col) = (nnCostFunc(network, input, output) - current_diff) / eps;//get the current slope
				MAT_AT(network->ws[mat_idx], row, col) = saved;
			}
		}

		for (size_t row = 0; row < network->bs[mat_idx]->rows; row++)// improve biases
		{
			for (size_t col = 0; col < network->bs[mat_idx]->cols; col++)
			{
				saved = MAT_AT(network->bs[mat_idx], row, col);

				MAT_AT(network->bs[mat_idx], row, col) += eps;
				MAT_AT(gradient->bs[mat_idx], row, col) = (nnCostFunc(network, input, output) - current_diff) / eps;//get the current slope
				MAT_AT(network->bs[mat_idx], row, col) = saved;
			}
		}
	}
}


void nnBackProp(nn* network, nn* gradient, Mat* input, Mat* output)
{
	if (input->rows != output->rows || NN_OUTPUT(network)->cols != output->cols)
	{
		exit(1);
	}
	nnFill(gradient, 0);

	size_t n = input->rows;
	float a = 0.0, da = 0.0, pa = 0.0, w = 0.0;
	Mat* row = NULL;

	for (size_t i = 0; i < n; i++) // current sample
	{
		row = matGetRow(input, i);
		matCopy(NN_INPUT(network), row);
		matFree(row);
		nnForward(network);

		for (size_t s = 0; s <= network->num_of_layers; s++)
		{
			matFill(gradient->as[s], 0);
		}

		for (size_t j = 0; j < output->cols; j++)  // get all the diffrences
		{
			MAT_AT(NN_OUTPUT(gradient), 0, j) = MAT_AT(NN_OUTPUT(network), 0, j) - MAT_AT(output, i, j);
		}

		for (size_t l = network->num_of_layers; l > 0; l--)  // current layer
		{
			for (size_t j = 0; j < network->as[l]->cols; j++)  // current activation (cols)
			{
				a = MAT_AT(network->as[l], 0, j);
				da = MAT_AT(gradient->as[l], 0, j);
				MAT_AT(gradient->bs[l - 1], 0, j) += 2 * da * a * (1 - a);

				for (size_t k = 0; k < network->as[l - 1]->cols; k++)  // current activation (rows - because of the matrix multipication)
				{
					pa = MAT_AT(network->as[l - 1], 0, k);
					w = MAT_AT(network->ws[l - 1], k, j);
					MAT_AT(gradient->ws[l - 1], k, j) += 2 * da * a * (1 - a) * pa;
					
					MAT_AT(gradient->as[l - 1], 0, k) += 2 * da * a * (1 - a) * w;
				}
			}
		}
	}

	for (size_t i = 0; i < gradient->num_of_layers; i++)
	{
		for (size_t row = 0; row < gradient->ws[i]->rows; row++)
		{
			for (size_t col = 0; col < gradient->ws[i]->cols; col++)
			{
				MAT_AT(gradient->ws[i], row, col) /= n;
			}
		}

		for (size_t row = 0; row < gradient->bs[i]->rows; row++)
		{
			for (size_t col = 0; col < gradient->bs[i]->cols; col++)
			{
				MAT_AT(gradient->bs[i], row, col) /= n;
			}
		}
	}
}


void nnApplyGradient(nn* network, nn* gradient, float rate)
{
	for (size_t mat_idx = 0; mat_idx < network->num_of_layers; mat_idx++)
	{
		for (size_t row = 0; row < network->ws[mat_idx]->rows; row++)// improve weights
		{
			for (size_t col = 0; col < network->ws[mat_idx]->cols; col++)
			{
				MAT_AT(network->ws[mat_idx], row, col) -= rate * MAT_AT(gradient->ws[mat_idx], row, col);
			}
		}

		for (size_t row = 0; row < network->bs[mat_idx]->rows; row++)// improve biases
		{
			for (size_t col = 0; col < network->bs[mat_idx]->cols; col++)
			{
				MAT_AT(network->bs[mat_idx], row, col) -= rate * MAT_AT(gradient->bs[mat_idx], row, col);
			}
		}
	}
}


void nnPrintTruthTable(nn* network, Mat* input, Mat* output, bool print_as_bits)
{
	Mat* input_row = NULL;

	printf("Cost: %f\n\n", nnCostFunc(network, input, output));


	for (size_t i = 0; i < input->rows; i++)
	{
		input_row = matGetRow(input, i);
		matCopy(NN_INPUT(network), input_row);

		nnForward(network);
		
		printf("( ");
		for (size_t j = 0; j < input->cols; j++)
		{
			printf("%.2f ", MAT_AT(input, i, j));
		}
		printf(") -> ( ");

		for (size_t j = 0; j < output->cols; j++)
		{
			if (print_as_bits)
			{
				printf("%d ", MAT_AT(NN_OUTPUT(network), 0, j) > 0.5);
			}
			else
			{
				printf("%.2f ", MAT_AT(NN_OUTPUT(network), 0, j));
			}
		}
		printf(")\n\n");

		matFree(input_row);
	}
}


bool nnCheckValidness(nn* network, Mat* input, Mat* output, bool binary_flag, float eps)
{
	bool ok = true;
	Mat* row = NULL;
	float value = 0;

	for (size_t i = 0; (i < output->rows) && ok; i++)
	{
		row = matGetRow(input, i);
		matCopy(NN_INPUT(network), row);
		nnForward(network);

		for (size_t j = 0; j < (output->cols) && ok; j++)
		{
			value = MAT_AT(NN_OUTPUT(network), 0, j);
			
			if (binary_flag)
			{
				value = (value > 0.5) ? 1.0f : 0.0f;
			}


			ok = fabs((double)MAT_AT(output, i, j) - (double)value) <= eps;

			if (!ok)
			{
				printf("Wrong value at Row: %zu\n", i);
			}
		}

		matFree(row);
	}

	return ok;
}


void nnFree(nn* network)
{
	matFree(network->as[0]);
	for (size_t i = 0; i < network->num_of_layers; i++)
	{
		matFree(network->ws[i]);
		matFree(network->bs[i]);
		matFree(network->as[i + 1]);
	}
	free(network->ws);
	free(network->bs);
	free(network->as);
	free(network);
}

#endif // NN_IMPL


#ifdef NN_ENABLE_IMAGE
#include <raylib.h>

typedef struct nnImage
{
	Image prev_img;
	Texture2D prev_texture;
	int w;
	int h;
	float scale;
} nnImage;


nnImage nnImageAlloc(int w, int h, Color color, float scale)
{
	Image prev_img = GenImageColor(w, h, color);
	Texture2D prev_texture = LoadTextureFromImage(prev_img);

	return CLITERAL(nnImage) {prev_img, prev_texture, w, h, scale};
}


#endif


#ifdef NN_ENABLE_GYM

size_t GRAPH_SIZE = 5000;

#define STR_LEN 256

enum ArgType { NN_ARG, NN_IMAGE_ARG, PLOT_ARG, INVALID_ARG };


typedef struct plot {
	float* data;
	size_t size;
	float max;

} plot;


#ifndef NN_ENABLE_IMAGE
#include <raylib.h>


#endif // !NN_ENABLE_IMAGE


Color background_color = { 0x18, 0x18, 0x18, 0xFF }; // by default, could be changed


plot* plotAlloc()
{
	plot* p = (plot*)malloc(sizeof(plot));

	if (!p)
	{
		exit(1);
	}

	p->data = NULL;
	p->size = 0;

	return p;
}


void changeBackgroundColor(Color new_value)
{
	background_color = new_value;
}


void addCellToPlot(plot* p)
{
	float* new_arr = NULL;
	float* temp = p->data;

	p->size++;

	new_arr = (float*)realloc(p->data, p->size * sizeof(float));

	if (!new_arr)
	{
		free(temp);
		exit(1);
	}

	p->data = new_arr;
}


void shiftLeftPlot(plot* p)
{
	for (size_t i = 0; i < p->size - 1; i++)
	{
		p->data[i] = p->data[i + 1];
	}
}


void addValueToPlot(plot* p, float value)
{
	p->data[p->size - 1] = value;

	if (value > p->max)
	{
		p->max = value;
	}
}

void nnRenderRaylib(nn* network, int padx, int pady, int w, int h)
{
	const float NEURON_RADIOS = h * 0.04f;
	int FONT_SIZE = h / 30;
	int LITTLE_PAD = w / 120;
	const float THICK = h * 0.008f;
	const int layer_border_vpad = 50;
	const int layer_border_hpad = 50;

	int arch_count = (int)network->num_of_layers + 1;
	int nn_height = h - 2 * layer_border_vpad;
	int nn_width = w - 2 * layer_border_hpad; // the room for the network

	int layer_x = padx + w / 2 - nn_width / 2;
	int layer_y = pady + h / 2 - nn_height / 2; // the start of the drawing

	int layer_hpad = nn_width / arch_count; // distance between layers
	int cx1, cy1, cx2, cy2, layer_vpad1, layer_vpad2;

	Color low_color = DARKPURPLE;
	Color high_color = GREEN;

	DrawText("Neuron Network:", w / 2 + padx * 4 / 5, pady - FONT_SIZE * 2, FONT_SIZE, LIGHTGRAY);

	float value = 0;

	for (int l = 0; l < arch_count; l++)
	{
		layer_vpad1 = nn_height / (int)network->as[l]->cols; // distance between each neuron
		cx1 = layer_x + l * layer_hpad + layer_hpad / 2;

		for (int i = 0; i < network->as[l]->cols; i++)
		{
			cy1 = layer_y + i * layer_vpad1 + layer_vpad1 / 2;

			if (l + 1 < arch_count)
			{
				layer_vpad2 = nn_height / (int)network->as[l + 1]->cols;
				for (int j = 0; j < network->as[l + 1]->cols; j++)
				{
					cx2 = layer_x + (l + 1) * layer_hpad + layer_hpad / 2;
					cy2 = layer_y + j * layer_vpad2 + layer_vpad2 / 2;

					value = sigmoidf(MAT_AT(network->ws[l], j, i));
					value -= 0.5;
					value = fabs(value * 2); // value is between 0 and 1 where 0 will be 0

					high_color.a = (unsigned char)floorf(255.f * value);
					Vector2 start = { (float)cx1, (float)cy1 };
					Vector2 end = { (float)cx2, (float)cy2 };
					DrawLineEx(start, end, (float)fabs(value) * THICK, ColorAlphaBlend(low_color, high_color, WHITE));
				}
			}

			switch (l)
			{
			case 0:
				DrawCircle(cx1, cy1, NEURON_RADIOS, LIGHTGRAY);
				break;

			default:
				value = sigmoidf(MAT_AT(network->bs[l - 1], 0, i));
				value -= 0.5;
				value = fabs(value * 2);

				high_color.a = (unsigned char)floorf(255.f * value);
				DrawCircle(cx1, cy1, NEURON_RADIOS, ColorAlphaBlend(low_color, high_color, WHITE));
			}

		}
	}
}


void costRenderRaylib(plot* p, int padx, int pady, int w, int h)
{
	float min = 0, max = p->max, x1, x2, y1, y2;

	int FONT_SIZE = h / 30;
	int LITTLE_PAD = w / 120;

	size_t n = GRAPH_SIZE;

	DrawText("Cost func:", w / 3 + padx, pady - FONT_SIZE * 2, FONT_SIZE, LIGHTGRAY);

	for (size_t i = 0; i + 1 < p->size; i++)
	{
		x1 = padx + (float)w / n * i;
		y1 = pady + (1 - ((p->data[i] - min) / (max - min))) * h;

		x2 = padx + (float)w / n * (i + 1);
		y2 = pady + (1 - ((p->data[i + 1] - min) / (max - min))) * h;

		DrawLineEx(CLITERAL(Vector2) { x1, y1 }, CLITERAL(Vector2) { x2, y2 }, h * 0.004f, RED);
		DrawLine(padx, pady, padx + w + LITTLE_PAD, pady, RED); // top left to top right
		DrawLine(padx, pady + h, padx + w + LITTLE_PAD, pady + h, RED); // button left to buttom right
		DrawLine(padx + w + LITTLE_PAD, pady, padx + w + LITTLE_PAD, pady + h, RED); // top right to button rights
		DrawLine(padx, pady, padx, pady + h, RED); // top left to buttom left
		DrawCircle((int)x1, (int)y1, h * 0.004f, RED);
	}

	DrawText("0", padx + LITTLE_PAD * 2 + w, pady + h - LITTLE_PAD, FONT_SIZE, LIGHTGRAY);
}


void createWindow(int w, int h, int fps)
{
	SetConfigFlags(FLAG_WINDOW_RESIZABLE);
	InitWindow(w, h, "gym");
	SetTargetFPS(fps);
}


void drawWindow(size_t iteration, size_t max_iteration, int num_of_args, ...)
{
	int current_width, current_height, rw, rh, rx, ry;
	uint8_t pixel = 0;
	char buffer[STR_LEN] = "";
	current_width = GetRenderWidth(), current_height = GetRenderHeight();

	va_list args;
	va_start(args, num_of_args);

	rw = current_width / num_of_args;
	rh = current_height * 2 / 3;
	rx = 3;
	ry = current_height / 2 - rh / 2;

	nn* network = NULL;
	plot* cost_plot = NULL; // if couple of plots are inputed, make sure to put the cost plot last

	BeginDrawing();
	ClearBackground(background_color);
	{
		for (int i = 0; i < num_of_args; i++)
		{
			enum ArgType arg_type = va_arg(args, enum ArgType);

			switch (arg_type)
			{
			case NN_ARG:
			{
				network = va_arg(args, nn*);
				nnRenderRaylib(network, rx, ry, rw, rh);
				break;
			}

			case PLOT_ARG:
			{
				plot* p = va_arg(args, plot*);
				cost_plot = p;
				costRenderRaylib(p, rx, ry, rw, rh);
				break;

			}

#ifdef NN_ENABLE_IMAGE
			case NN_IMAGE_ARG:
			{
				nnImage image = va_arg(args, nnImage);
				if (!network)
				{
					break;
				}

				for (int y = 0; y < image.h; y++)
				{
					for (int x = 0; x < image.w; x++)
					{
						MAT_AT(NN_INPUT(network), 0, 0) = (float)x / (image.w - 1);
						MAT_AT(NN_INPUT(network), 0, 1) = (float)y / (image.h - 1);

						nnForward(network);
						pixel = MAT_AT(NN_OUTPUT(network), 0, 0) * 255.f;
						ImageDrawPixel(&(image.prev_img), x, y, CLITERAL(Color){pixel, pixel, pixel, 255});
					}
				}

				UpdateTexture(image.prev_texture, image.prev_img.data);
				DrawTextureEx(image.prev_texture, CLITERAL(Vector2) {(float)rx, (float)ry}, 0, image.scale, WHITE);
				break;
			}
#endif // NN_ENABLE_IMAGE

			}

			rx += rw;
		}


		if (cost_plot)
		{
			snprintf(buffer, sizeof(buffer), "Iteration: %zu/%zu, Cost: %f", iteration, max_iteration, cost_plot->data[cost_plot->size - 1]);
		}
		else
		{
			snprintf(buffer, sizeof(buffer), "Iteration: %zu/%zu, Cost: %f", iteration, max_iteration, 0.f);
		}

		DrawText(buffer, 0, 0, (int)(current_height * 0.04), LIGHTGRAY);


		EndDrawing();
	}
}

#endif  // NN_ENABLE_GYM


#ifdef NN_ENABLE_ARCH_LOAD

#define SV_IMPLEMENTATION
#include "sv.h"

#include "raylib.h"

char* args_shift(int* argc, char*** argv)
{
	if (*argc <= 0)
	{
		exit(1);
	}

	char* result = **argv;

	(*argc)--;
	(*argv) += 1;

	return result;
}


void* add_cell_to_arr(void* arr, size_t current_arr_size, size_t size_of_element)
{
	void* new_arr = NULL;
	void* temp = arr;

	new_arr = realloc(arr, current_arr_size * size_of_element);

	if (!new_arr)
	{
		free(temp);
		exit(1);
	}

	return new_arr;
}


size_t* loadArchFromFile(const char* arch_file_path, size_t* size)
{
	unsigned int buffer_len = 0;
	unsigned char* buffer = LoadFileData(arch_file_path, (int*) & buffer_len);
	int counter = 0;
	size_t* arch = NULL;
	size_t x = 0;
	String_View content = sv_from_parts((const char*)buffer, buffer_len);
	content = sv_trim_left(content);


	if (!buffer)
	{
		fprintf(stderr, "Error: could not allocate buffer\n");
		exit(1);
	}

	while (content.count > 0 && isdigit(content.data[0]))
	{
		counter++;
		x = sv_chop_u64(&content); // next number in the arch file
		arch = (size_t*)add_cell_to_arr(arch, counter, sizeof(size_t));
		arch[counter - 1] = x;
		content = sv_trim_left(content);
	}

	*size = counter;

	return arch;
}


#endif // NN_ENABLE_ARCH_LOAD
