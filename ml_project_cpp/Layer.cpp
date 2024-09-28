#include "Layer.h"

Layer::Layer(int inputSize, int outputSize, std::shared_ptr<ActivationFunction> activation)
{
	_weights = Mat(inputSize, outputSize);
	_biases = Mat(1, outputSize);

	_gradientW = _weights;
	_gradientB = _biases;

	_weights.matRand(-1, 1);
	_biases.matRand(-0.5, 0.5);

	_activationFunc = activation;

	_amountOfInputs = inputSize;
	_amountOfNeurons = outputSize;
}

Layer::Layer(std::ifstream& file)
{
	load(file);

	_gradientW = _weights;
	_gradientB = _biases;

	_gradientW.matFill(0);
	_gradientB.matFill(0);

	_amountOfInputs = (int)_weights.getRows();
	_amountOfNeurons = (int)_weights.getCols();
}

Mat Layer::forward(Mat& input)
{
	Mat output = input * _weights;
	output += _biases;

	output.matActivation(_activationFunc.get());

	_output = output;
	_input = input;

	return output;
}

Mat Layer::backward(Mat& differences, float learningRate)
{
	Mat deltas(1, _amountOfNeurons);
	Mat inputGradient(1, _amountOfInputs);
	float weightGradient = 0.0;

	for (size_t i = 0; i < _amountOfNeurons; i++)
	{
		deltas(0, i) = differences(0, i) * _activationFunc->calc_derivative(_output(0, i));
	}

	for (size_t i = 0; i < _amountOfNeurons; i++)
	{
		for (size_t j = 0; j < _amountOfInputs; j++) // each row of weights represents an input
		{
			weightGradient = deltas(0, i) * _input(0, j); // get gradient of weight

			_gradientW(j, i) += weightGradient;
		}

		_gradientB(0, i) += deltas(0, i);
	}

	for (size_t i = 0; i < _amountOfInputs; i++) // each row of weights represents an input
	{
		for (size_t j = 0; j < _amountOfNeurons; j++)
		{
			inputGradient(0, i) += deltas(0, j) * _weights(i, j); // matrix multipication (each input in index 0, i is being multipied by all weights in row i)
		}
	}

	return inputGradient;
}

bool Layer::save(std::ofstream& file)
{
	if (!file.is_open())
		return false;

	unsigned char code = _activationFunc.get()->code();

	file.write(reinterpret_cast<const char*>(&code), sizeof(code));

	return _weights.matSave(file) && _biases.matSave(file);
}

bool Layer::save(std::string fileName)
{
	std::ofstream file(fileName, std::ios::binary);

	bool val = save(file);

	file.close();

	return val;
}

bool Layer::load(std::ifstream& file)
{
	if (!file.is_open())
		return false;

	unsigned char code;

	file.read(reinterpret_cast<char*>(&code), sizeof(unsigned char));

	_activationFunc = getInstance(code);

	return _weights.matLoad(file) && _biases.matLoad(file);
}

bool Layer::load(std::string fileName)
{
	std::ifstream file(fileName);
	
	bool val = load(file);

	file.close();

	return val;
}

void Layer::avgGradient(size_t amountOfSamples)
{
	for (size_t row = 0; row < _gradientW.getRows(); row++)
	{
		for (size_t col = 0; col < _gradientW.getCols(); col++)
		{
			_gradientW(row, col) /= (float)amountOfSamples;
		}
	}

	for (size_t col = 0; col < _gradientB.getCols(); col++)
	{
		_gradientB(col) /= (float)amountOfSamples;
	}
}

void Layer::applyGradient(size_t amountOfSamples, float learningRate)
{
	avgGradient(amountOfSamples);
	
	for (size_t row = 0; row < _weights.getRows(); row++)
	{
		for (size_t col = 0; col < _weights.getCols(); col++)
		{
			_weights(row, col) -= _gradientW(row, col) * learningRate;
		}
	}

	for (size_t col = 0; col < _biases.getCols(); col++)
	{
		_biases(col) -= _gradientB(col) * learningRate;
	}
}

void Layer::resetGradient()
{
	_gradientW.matFill(0);
	_gradientB.matFill(0);
}

std::ostream& operator<<(std::ostream& os, const Layer& layer)
{
	os << std::setprecision(2) << std::fixed;
	os << "  " << layer._activationFunc.get()->name() << ":\n\n";

	Mat weights(layer._weights.getRows(), 1);

	for (size_t neuron = 0; neuron < layer._weights.getCols(); neuron++)
	{
		os << "    Neuron " << neuron + 1 << ":\n      Weights | biases\n";

		for (size_t row = 0; row < layer._weights.getRows() - 1; row++)
		{
			os << "        " << layer._weights(row, neuron) << "\n";
		}

		os << "        " << layer._weights(layer._weights.getRows() - 1, neuron) << "     " << layer._biases(0, neuron) << "\n\n";
	}

	return os;
}
