#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>

#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
#include <stdint.h>

#define NN_IMPL
#include "nn.h"

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

	const char* img_path = args_shift(&argc, &argv);

	int img_width, img_height, img_comp;
	uint8_t* img_pixels = (uint8_t*)stbi_load(img_path, &img_width, &img_height, &img_comp, 0);

	if (!img_pixels)
	{
		fprintf(stderr, "Error: Could not read image %s\n", img_path);
		exit(1);
	}

	if (img_comp != 1)
	{
		fprintf(stderr, "Error: %s is %d bits image. Only 8 bit grayscale images are supported\n", img_path, img_comp * 8);
		exit(1);
	}

	Mat* training = matAlloc((size_t)img_width * img_height, 3);

	float nx, ny, nb;
	size_t i = 0;

	for (int y = 0; y < img_height; y++)
	{
		for (int x = 0; x < img_width; x++)
		{
			i = (size_t)y * img_width + x;

			MAT_AT(training, i, 0) = (float)x / (img_width - 1);
			MAT_AT(training, i, 1) = (float)y / (img_height - 1);
			MAT_AT(training, i, 2) = img_pixels[i] / 255.f;
		}
	}

	const char* out_file_path = "img.mat";
	FILE* out = fopen(out_file_path, "wb");

	if (!out)
	{
		fprintf(stderr, "Error: Could not save training matrix of image\n");
		exit(1);
	}

	matSave(out, training);
	fclose(out);

	printf("Generated %s to %s\n", img_path, out_file_path);

	matFree(training);
	getchar();
	return 0;
}