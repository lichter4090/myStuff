#include "nn.h"



nn::nn(int amountOfInputs)
{
	_architecture.push_back(amountOfInputs);
	_inputRow = Mat(1, amountOfInputs);
}

nn::nn(std::string fileName)
{
	if (!load(fileName))
		throw std::exception("Failed to load nn");
}

void nn::addLayer(int amountOfNeurons, std::shared_ptr<ActivationFunction> func)
{
	size_t amountOfLayers = _layers.size();
	_architecture.push_back(amountOfNeurons);

	Layer layer(_architecture[amountOfLayers], amountOfNeurons, func);

	_layers.push_back(layer);
}

Mat nn::forward(Mat& input)
{
	Mat currentOutput;

	currentOutput = _layers[0].forward(input);

	for (size_t layerIdx = 1; layerIdx < _layers.size(); layerIdx++)
	{
		currentOutput = _layers[layerIdx].forward(currentOutput);
	}

	return currentOutput;
}

void nn::train(Mat& input, Mat& output, float learningRate, size_t epoch)
{
	Mat currentOutput;
	Mat outputGradients;
	Mat outputRow(1, output.getCols());

	size_t batchSize = 28;
	size_t batchCount = input.getRows() / batchSize;
	size_t currentBatch = epoch % batchCount;

	Mat batchInput;
	Mat batchOutput;

	for (size_t layerIdx = 0; layerIdx < _layers.size(); layerIdx++)
	{
		_layers[layerIdx].resetGradient();
	}

	batchInput = input.matGetOffsetRows(currentBatch * batchSize);
	batchOutput = output.matGetOffsetRows(currentBatch * batchSize);

	batchInput.matCropRows(batchSize);
	batchOutput.matCropRows(batchSize);

	trainBackword(batchInput, batchOutput, learningRate);
}

void nn::trainBackword(Mat& input, Mat& output, float learningRate)
{
	Mat currentOutput;
	Mat outputGradients;
	Mat outputRow(1, output.getCols());
	
	for (size_t row = 0; row < input.getRows(); row++)
	{
		_inputRow.matInitArr(input.matGetRow(row));

		currentOutput = forward(_inputRow);

		outputRow.matInitArr(output.matGetRow(row));

		outputGradients = costFuncionGradients(input.getRows(), currentOutput, outputRow);

		for (int layerIdx = (int)_layers.size() - 1; layerIdx >= 0; layerIdx--)
		{
			outputGradients = _layers[layerIdx].backward(outputGradients, learningRate);
		}
	}

	applyGradient(input.getRows(), learningRate);
}

void nn::trainForward(Mat& input, Mat& output, float learningRate)
{
	float current = costFunction(input, output);
	float saved;
	float eps = 0.0001f;
	float diff;
	
	std::vector<std::vector<float>> gradientWeight(_layers.size());
	std::vector<std::vector<float>> gradientBias(_layers.size());


	for (size_t layer = 0; layer < _layers.size(); layer++)
	{
		Layer& l = _layers[layer];
		l.resetGradient();

		for (size_t row = 0; row < l.getWeights().getRows(); row++)// improve weights
		{
			for (size_t col = 0; col < l.getWeights().getCols(); col++)
			{
				saved = l.getWeights()(row, col);

				l.getWeights()(row, col) += eps;

				diff = (costFunction(input, output) - current) / eps;

				l.getWeights()(row, col) = saved;

				l.getGradientW()(row, col) = diff;
			}
		}

		for (size_t row = 0; row < l.getBiases().getRows(); row++)// improve biases
		{
			for (size_t col = 0; col < l.getBiases().getCols(); col++)
			{
				saved = l.getBiases()(row, col);

				l.getBiases()(row, col) += eps;

				diff = (costFunction(input, output) - current) / eps;

				l.getBiases()(row, col) = saved;
				
				l.getGradientB()(row, col) = diff;
			}
		}
	}

	applyGradient(input.getRows(), learningRate);
}

float nn::costFunction(Mat& input, Mat& output)
{
	float loss = 0.0, d;
	Mat currentOutput;

	for (size_t row = 0; row < input.getRows(); row++)
	{
		_inputRow.matInitArr(input.matGetRow(row));

		currentOutput = forward(_inputRow);
		
		for (size_t col = 0; col < output.getCols(); col++)
		{
			d = currentOutput(0, col) - output(row, col);
			loss += d * d;
		}
	}
	return loss / input.getRows();
}

Mat nn::costFuncionGradients(size_t amountOfSamples, Mat& output, Mat& targets)
{
	Mat gradients(1, output.getCols());
	float diff;

	for (size_t i = 0; i < output.getCols(); i++)
	{
		diff = output(0, i) - targets(0, i);

		gradients(0, i) = (2.f / amountOfSamples) * diff;
	}

	return gradients;
}

void nn::printTruthTable(Mat& input, std::ostream& os)
{
	os << std::setprecision(2) << std::fixed;

	Mat currentOutput;

	for (size_t row = 0; row < input.getRows(); row++)
	{
		_inputRow.matInitArr(input.matGetRow(row));
		currentOutput = forward(_inputRow);

		for (size_t i = 0; i < _inputRow.getCols() - 1; i++)
		{
			os << _inputRow(0, i) << ", ";
		}

		os << _inputRow(0, _inputRow.getCols() - 1);


		os << " -> ";

		for (size_t i = 0; i < currentOutput.getCols() - 1; i++)
		{
			os << currentOutput(0, i) << ", ";
		}

		os << currentOutput(0, currentOutput.getCols() - 1) << "\n\n";
	}
}

bool nn::save(std::string fileName)
{
	std::ofstream file(fileName);

	if (!file.is_open())
		return false;

	size_t size = _layers.size();

	file.write(reinterpret_cast<const char*>(&size), sizeof(size));

	size_t amountOfInputs = _inputRow.getCols();

	file.write(reinterpret_cast<const char*>(&amountOfInputs), sizeof(amountOfInputs));

	for (Layer& layer : _layers)
	{
		layer.save(file);
	}
	
	file.close();

	return true;
}

bool nn::load(std::string fileName)
{
	std::ifstream file(fileName);
	
	if (!file.is_open())
		return false;

	size_t size, amountOfInputs;

	file.read(reinterpret_cast<char*>(&size), sizeof(size));
	file.read(reinterpret_cast<char*>(&amountOfInputs), sizeof(amountOfInputs));

	for (size_t i = 0; i < size; i++)
	{
		Layer l(file);

		_layers.push_back(l);
	}

	file.close();

	_inputRow = Mat(1, amountOfInputs);

	_architecture = std::vector<int>();

	_architecture.push_back((int)amountOfInputs);
	
	for (auto& layer : _layers)
	{
		_architecture.push_back(layer.getAmountOfNeurons());
	}

	return true;
}

void nn::applyGradient(size_t amountOfSamples, float learningRate)
{
	for (size_t layer = 0; layer < _layers.size(); layer++)
	{
		_layers[layer].applyGradient(amountOfSamples, learningRate);
	}
}

std::ostream& operator<<(std::ostream& os, const nn& network)
{
	for (size_t layer = 0; layer < network._layers.size(); layer++)
	{
		os << "Layer " << layer + 1 << ":\n";
		os << network._layers[layer];
		os << "\n";
	}

	return os;
}
