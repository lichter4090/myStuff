#pragma once

#include "Layer.h"



class nn
{
public:
	nn(int amountOfInputs);
	nn(std::string fileName);
	nn() { ; }
	nn(const nn& other) { (*this) = other; }
	~nn() {};

	size_t numOfLayers() const { return _layers.size(); }
	std::vector<int> getArch() const { return _architecture; }

	void addLayer(int amountOfNeurons, std::shared_ptr<ActivationFunction> func);
	Mat forward(Mat& input);

	// train functions. One iteration of learning.
	void train(Mat& input, Mat& output, float learningRate, size_t epoch);
	void trainBackword(Mat& input, Mat& output, float learningRate);
	void trainForward(Mat& input, Mat& output, float learningRate);

	// cost function
	float costFunction(Mat& input, Mat& output);
	Mat costFuncionGradients(size_t amountOfSamples, Mat& output, Mat& targets);


	void printTruthTable(Mat& input, std::ostream& os = std::cout);

	bool save(std::string fileName);
	bool load(std::string fileName);

	Mat getWeightsOfLayer(size_t layerIdx) { return _layers[layerIdx].getWeights(); }
	Mat getBiasesOfLayer(size_t layerIdx) { return _layers[layerIdx].getBiases(); }

	size_t getLayers() { return _layers.size(); }
	std::string getNameOfActivation(size_t idx) { return _layers[idx].getNameOfActivation(); }

	// for printing
	friend std::ostream& operator<<(std::ostream& os, const nn& network);

private:
	void applyGradient(size_t amountOfSamples, float learningRate);

	Mat _inputRow;
	std::vector<int> _architecture;
	std::vector<Layer> _layers;
};