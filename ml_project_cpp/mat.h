#pragma once

#include <iostream>
#include <vector>
#include <string>
#include <assert.h>
#include <math.h>
#include <algorithm>
#include <iomanip>
#include <fstream>
#include <random>
#include <sstream>
#include "ActivationFunction.h"
#include <stdint.h>
#include "raylib.h"



class Mat
{
public:
	Mat() { _rows = 0;  _cols = 0; };
	Mat(size_t rows, size_t cols);
	Mat(const Mat& other);
	Mat operator=(const Mat& other);
	Mat(std::string fileName);
	~Mat() {};

	size_t getRows() const { return _rows; };
	size_t getCols() const { return _cols; };
	std::vector<std::vector<float>> getData() const { return _data; };

	void matRand(float low, float high);
	void matFill(float num);
	void matInitArr(float* data, size_t size);
	void matInitArr(std::vector<float> data);
	std::vector<float>& matGetRow(size_t row);

	void matMerge(Mat& other);
	Mat matSplit(size_t colIdx); // The left side is *this the right side is the return value

	void matActivation(const ActivationFunction* func);

	void matShuffleRows();

	void matAddRow();
	void matAddRow(std::vector<float>& row);
	void matAddRow(Mat& row);
	void matRemoveRow(size_t row);

	bool matSave(std::ofstream& file);
	bool matSave(std::string fileName);

	bool matLoad(std::ifstream& file);
	bool matLoad(std::string fileName);

	Mat matLoadFromImage(std::string imagePath, bool shuffle=true); // *this will become the input matrix and the function returns the output matrix

	std::vector<float> create1dArray() const;

	Mat matGetOffsetRows(size_t rowStart);
	void matCropRows(size_t rowIdx);


	// operators
	bool operator==(const Mat& other) const;
	bool operator!=(const Mat& other) const;
	Mat operator+=(const Mat& other);
	Mat operator-=(const Mat& other);
	Mat operator+(const Mat& other);
	Mat operator-(const Mat& other);
	Mat operator*(const Mat& other);
	Mat operator*(float scalar);
	float& operator()(size_t row, size_t col);
	const float& operator()(size_t row, size_t col) const;

	float& operator()(size_t index);
	const float& operator()(size_t index) const;

	static void matDot(Mat& dst, const Mat& a, const Mat& b);

	// for printing
	friend std::ostream& operator<<(std::ostream& os, const Mat& matrix);

private:
	std::vector<std::vector<float>> _data;
	size_t _rows;
	size_t _cols;
};