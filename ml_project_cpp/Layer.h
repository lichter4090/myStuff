#pragma once

#include "mat.h"
#include <memory>
#include <cstdio>


class Layer
{
public:
	Layer(int inputSize, int outputSize, std::shared_ptr<ActivationFunction> activation); // output size is the amount of neurons in the layer
	Layer(std::ifstream& fileName);
	~Layer() {}

	Mat& getBiases() { return _biases; }
	Mat& getWeights() { return _weights; };

	Mat forward(Mat& input);
	Mat backward(Mat& differences, float learningRate);

	Mat& getGradientW() { return _gradientW; }
	Mat& getGradientB() { return _gradientB; }

	bool save(std::ofstream& file);
	bool save(std::string fileName);

	bool load(std::ifstream& file);
	bool load(std::string fileName);


	// for printing
	friend std::ostream& operator<<(std::ostream& os, const Layer& layer);
	
	void applyGradient(size_t amountOfSamples, float learningRate);
	void resetGradient();

	int getAmountOfNeurons() { return _amountOfNeurons; }
	std::string getNameOfActivation() { return _activationFunc->name(); }


private:
	void avgGradient(size_t amountOfSamples);


	Mat _biases; // size 1 x outputSize
	Mat _weights; // size inputSize x outputSize (amountOfInputs x AmountOfNeurons)
	std::shared_ptr<ActivationFunction> _activationFunc;

	Mat _output;
	Mat _input;

	int _amountOfNeurons;
	int _amountOfInputs;

	Mat _gradientW;
	Mat _gradientB;
};