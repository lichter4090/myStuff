#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>

#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
#include <stdint.h>

#define NN_IMPL
#include "nn.h"

#include "dirent.h"

#define DIMENTION 28

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


int main(int argc, char** argv)
{
	const char* program = args_shift(&argc, &argv);

	if (argc <= 0)
	{
		fprintf(stderr, "Usage: %s <image path>\n", program);
		fprintf(stderr, "Error: No png file was inpued\n");
		exit(1);
	}

	const char* numbers_path = args_shift(&argc, &argv);
	char dir_name[256] = { 0 };

	strcat(dir_name, numbers_path);
	strcat(dir_name, "\\");
	strcat(dir_name, "0");
	
	size_t index_of_char_dir_name = strcspn(dir_name, "0");

	char photo_name = "0.png";
	int img_width, img_height, img_comp;
	DIR* photos_dir = NULL;
	struct dirent* dir = NULL;
	uint8_t* img_pixels = NULL;

	Mat* input = matAlloc(0, (size_t)DIMENTION * DIMENTION);
	Mat* output = matAlloc(0, (size_t)10);


	size_t num_of_photos = 0;
	int current_num = 0;

	for (int i = 0; i < 10; i++)
	{
		dir_name[index_of_char_dir_name] = (char)((char)i + '0');
		photos_dir = opendir(dir_name);

		if (!photos_dir)
		{
			fprintf(stderr, "Cannot open dir %s", dir_name);
		}

		while ((dir = readdir(photos_dir)) != NULL)
		{
			if (strcmp(dir->d_name, ".") == 0 || strcmp(dir->d_name, "..") == 0)//. and .. are file name's that are in every directory and they are'nt for editing so avoid those files
				continue;
			
			char full_path[512] = { 0 };

			strcat(full_path, dir_name);
			strcat(full_path, "\\");
			strcat(full_path, dir->d_name);

			img_pixels = (uint8_t*)stbi_load(full_path, &img_width, &img_height, &img_comp, 0);

			if (img_width != img_height || img_width != DIMENTION)
			{
				fprintf(stderr, "Error: only 28x28 pictures");
				exit(1);
			}

			if (!img_pixels)
			{
				fprintf(stderr, "Error: Could not read image %s\n", full_path);
				exit(1);
			}

			if (img_comp != 1)
			{
				fprintf(stderr, "Error: %s is %d bits image. Only 8 bit grayscale images are supported\n", full_path, img_comp * 8);
				exit(1);
			}

			matAddRow(input);
			matAddRow(output);

			for (size_t i = 0; i < DIMENTION * DIMENTION; i++)
			{
				MAT_AT(input, num_of_photos, i) = img_pixels[i] / 255.f;
			}
			
			char output_num[] = "0000000000";

			output_num[i] = '1';

			for (size_t i = 0; i < 10; i++)
			{
				MAT_AT(output, num_of_photos, i) = output_num[i] - '0';
			}

			num_of_photos += 1;
		}
	}

	MAT_PRINT(output);
	Mat* training = matAlloc(input->rows, input->cols + output->cols);

	matMerge(training, input, output);

	const char* out_file_path = "img_nums.mat";
	FILE* out = fopen(out_file_path, "wb");

	if (!out)
	{
		fprintf(stderr, "Error: Could not save training matrix of image\n");
		exit(1);
	}

	matSave(out, training);
	fclose(out);

	Mat* row_of_input = NULL;

	for (size_t i = 0; i < input->rows; i++)
	{
		row_of_input = matGetRow(input, i);

		for (int i = 0; i < row_of_input->cols; i++)
		{
			if (i % 28 == 0)
				printf("\n");

			uint8_t pixel = (uint8_t)(MAT_AT(row_of_input, 0, i) * 255.f);

			if (pixel)
			{
				printf("%3u ", pixel);
			}
			else
			{
				printf("    ");
			}
		}

		int actual_num = 0;

		for (size_t j = 0; j < output->cols; j++)
		{
			if (MAT_AT(output, i, j) == 1)
				actual_num = (int)j;
		}

		printf("\nReal number was %d\n", actual_num);
	}

	printf("Generated %s to %s\n", numbers_path, out_file_path);

	matFree(training);
	matFree(input);
	matFree(output);
	getchar();
	return 0;
}