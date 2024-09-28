#include "mat.h"


Mat::Mat(size_t rows, size_t cols) : _rows(rows), _cols(cols)
{
	for (int row = 0; row < rows; row++)
	{
		_data.push_back(std::vector<float>(cols));
	}
}

Mat::Mat(const Mat& other)
{
	_rows = other._rows;
	_cols = other._cols;
	_data = other._data;
}

Mat Mat::operator=(const Mat& other)
{
	_rows = other._rows;
	_cols = other._cols;
	_data = other._data;

	return *this;
}

Mat::Mat(std::string fileName)
{
	_rows = 0;
	_cols = 0;

	if (!matLoad(fileName))
	{
		throw std::exception("Error loading matrix");
	}
}

void Mat::matRand(float low, float high)
{
	std::random_device rd;
	std::mt19937 gen(rd());
	std::uniform_real_distribution<float> distrib(low, high);
	

	for (size_t rows = 0; rows < _rows; rows++)
	{
		for (size_t cols = 0; cols < _cols; cols++)
		{
			_data[rows][cols] = distrib(gen);
		}
	}
}

void Mat::matFill(float num)
{
	for (auto& row : _data)
	{
		for (auto& cell : row)
		{
			cell = num;
		}
	}
}

void Mat::matInitArr(float* data, size_t size)
{
	assert(size == _cols * _rows);

	size_t i = 0;
	for (auto& row : _data)
	{
		for (auto& cell : row)
		{
			cell = data[i];
			i++;
		}
	}
}

void Mat::matInitArr(std::vector<float> data)
{
	assert(data.size() == (_cols * _rows));

	for (size_t row = 0; row < _rows; row++)
	{
		for (size_t col = 0; col < _cols; col++)
		{
			_data[row][col] = data[row * _cols + col];
		}
	}
}

std::vector<float>& Mat::matGetRow(size_t row)
{
	assert(row < _rows && row >= 0);

	return _data[row];
}

void Mat::matMerge(Mat& other)
{
	assert(other._rows == _rows);
	std::vector<float> otherRow;

	_cols += other._cols;

	for (size_t i = 0; i < _rows; i++)
	{
		otherRow = other.matGetRow(i);
		_data[i].insert(_data[i].end(), otherRow.begin(), otherRow.end());
	}
}

Mat Mat::matSplit(size_t colIdx)
{
	size_t rightSideSize = _cols - colIdx;
	Mat rightSide(0, rightSideSize);
	std::vector<float> row;
	std::vector<float> rowToAdd;

	for (size_t rowIdx = 0; rowIdx < _rows; rowIdx++)
	{
		row = _data[rowIdx];

		for (size_t i = colIdx; i < _cols; i++)
		{
			rowToAdd.push_back(_data[rowIdx][i]);
			_data[rowIdx].erase(_data[rowIdx].begin() + i);
		}

		rightSide.matAddRow(rowToAdd);
		rowToAdd.clear();
	}

	_cols = colIdx;


	return rightSide;
}

void Mat::matActivation(const ActivationFunction* func)
{
	for (size_t rows = 0; rows < _rows; rows++)
	{
		for (size_t cols = 0; cols < _cols; cols++)
		{
			_data[rows][cols] = func->calc(_data[rows][cols]);
		}
	}
}

void Mat::matShuffleRows()
{
	std::random_shuffle(_data.begin(), _data.end());
}

void Mat::matAddRow()
{
	_rows++;

	_data.push_back(std::vector<float>(_cols));
}

void Mat::matAddRow(std::vector<float>& row)
{
	_rows++;

	_data.push_back(row);
}

void Mat::matAddRow(Mat& row)
{
	_rows++;

	_data.push_back(row.matGetRow(0));
}

void Mat::matRemoveRow(size_t row)
{
	assert(_rows != 0 && row < _rows && row >= 0);

	size_t i = 0;
	auto it = _data.begin();

	for (it; i < row; it++) {}

	_data.erase(it);
	_rows--;
}

bool Mat::matSave(std::ofstream& file)
{
	if (!file.is_open())
		return false;

	file.write(reinterpret_cast<const char*>(&_rows), sizeof(_rows));
	file.write(reinterpret_cast<const char*>(&_cols), sizeof(_cols));

	for (const auto& row : _data)
	{
		file.write(reinterpret_cast<const char*>(row.data()), row.size() * sizeof(float));
	}

	return true;
}

bool Mat::matSave(std::string fileName)
{
	std::ofstream file(fileName, std::ios::binary);

	bool val = matSave(file);

	file.close();

	return val;
}

bool Mat::matLoad(std::ifstream& file)
{
	if (!file.is_open())
		return false;

	file.read(reinterpret_cast<char*>(&_rows), sizeof(_rows));
	file.read(reinterpret_cast<char*>(&_cols), sizeof(_cols));

	_data = std::vector<std::vector<float>>();

	for (int row = 0; row < _rows; row++)
	{
		_data.push_back(std::vector<float>(_cols));
	}

	for (int i = 0; i < _rows; ++i)
	{
		file.read(reinterpret_cast<char*>(_data[i].data()), _cols * sizeof(float));
	}

	return true;
}

bool Mat::matLoad(std::string fileName)
{
	std::ifstream inFile(fileName, std::ios::binary);
	
	bool val = matLoad(inFile);

	inFile.close();

	return val;
}

Mat Mat::matLoadFromImage(std::string imagePath, bool shuffle)
{
	int imgWidth, imgHeight;
	unsigned char* data;

	Image img = LoadImage(imagePath.c_str());

	imgWidth = img.width;
	imgHeight = img.height;
	data = (unsigned char*)img.data;

	if (!data)
	{
		std::string error = "Could not read image " + imagePath + "\n";

		throw std::exception(error.c_str());
	}

	if (img.format != PIXELFORMAT_UNCOMPRESSED_GRAYSCALE)
	{
		std::string error = imagePath + " is not 8 bit grayscale image\n";
		
		throw std::exception(error.c_str());
	}

	_rows = imgWidth * imgHeight;
	_cols = 2;

	_data = std::vector<std::vector<float>>();

	for (int row = 0; row < _rows; row++)
	{
		_data.push_back(std::vector<float>(_cols));
	}// reset data

	Mat output(_rows, 1);
	size_t i = 0;

	for (int y = 0; y < imgHeight; y++)
	{
		for (int x = 0; x < imgWidth; x++)
		{
			i = (size_t)y * imgWidth + x;

			_data[i][0] = (float)x / (imgWidth - 1);
			_data[i][1] = (float)x / (imgWidth - 1);
			output(i, 0) = data[i] / 255.f;
		}
	}

	return output;
}

std::vector<float> Mat::create1dArray() const
{
	std::vector<float> output;

	for (auto& row : _data)
	{
		output.insert(output.end(), row.begin(), row.end());
	}

	return output;
}

Mat Mat::matGetOffsetRows(size_t rowStart)
{
	Mat offsetMat(0, _cols);

	for (size_t row = rowStart; row < _rows; row++)
	{
		offsetMat.matAddRow(_data[row]);
	}

	return offsetMat;
}

void Mat::matCropRows(size_t rowIdx)
{
	for (size_t row = rowIdx; row < _rows; row++)
	{
		_data.erase(_data.begin() + rowIdx);
	}

	_rows = rowIdx;
}

bool Mat::operator==(const Mat& other) const
{
	return _data == other._data;
}

bool Mat::operator!=(const Mat& other) const
{
	return !(*this == other);
}

Mat Mat::operator+=(const Mat& other)
{
	return (*this) + other;
}

Mat Mat::operator-=(const Mat& other)
{
	return (*this) - other;
}

Mat Mat::operator+(const Mat& other)
{
	assert(_rows == other._rows && _cols == other._cols);

	for (int row = 0; row < _rows; row++)
	{
		for (int col = 0; col < _cols; col++)
		{
			_data[row][col] += other(row, col);
		}
	}

	return *this;
}

Mat Mat::operator-(const Mat& other)
{
	assert(_rows == other._rows && _cols == other._cols);

	for (int row = 0; row < _rows; row++)
	{
		for (int col = 0; col < _cols; col++)
		{
			_data[row][col] -= other(row, col);
		}
	}

	return *this;
}

Mat Mat::operator*(const Mat& other)
{
	assert(_cols == other._rows);

	Mat dst(_rows, other._cols);

	matDot(dst, *this, other);
	
	return dst;
}

Mat Mat::operator*(float scalar)
{
	for (size_t row = 0; row < _rows; row++)
	{
		for (size_t col = 0; col < _cols; col++)
		{
			_data[row][col] *= scalar;
		}
	}

	return *this;
}

float& Mat::operator()(size_t row, size_t col)
{
	assert(_rows > row && _cols > col && row >= 0 && col >= 0);
	return _data[row][col];
}

const float& Mat::operator()(size_t row, size_t col) const
{
	assert(_rows > row && _cols > col && row >= 0 && col >= 0);
	return _data[row][col];
}

float& Mat::operator()(size_t index)
{
	size_t row = index / _cols;
	size_t col = index % _cols;

	return (*this)(row, col);
}

const float& Mat::operator()(size_t index) const
{
	size_t row = index / _cols;
	size_t col = index % _cols;

	return (*this)(row, col);
}

void Mat::matDot(Mat& dst, const Mat& a, const Mat& b)
{
	assert(a._cols == b._rows && dst._rows == a._rows && dst._cols == b._cols);

	size_t n = a._cols;

	for (int rows = 0; rows < dst._rows; rows++)
	{
		for (int cols = 0; cols < dst._cols; cols++)
		{
			dst(rows, cols) = 0;

			for (int i = 0; i < n; i++)
			{
				dst(rows, cols) += a(rows, i) * b(i, cols);
			}
		}
	}
}

std::ostream& operator<<(std::ostream& os, const Mat& matrix)
{
	os << std::setprecision(2) << std::fixed;

	for (int rows = 0; rows < matrix.getRows(); rows++)
	{
		for (int cols = 0; cols < matrix.getCols(); cols++)
		{
			os << matrix(rows, cols) << " ";
		}
		os << "\n";
	}

	return os;
}
