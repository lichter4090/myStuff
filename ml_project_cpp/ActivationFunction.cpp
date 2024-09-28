#include "ActivationFunction.h"

std::shared_ptr<ActivationFunction> NoActivation::instance = nullptr;
std::shared_ptr<ActivationFunction> Sigmoid::instance = nullptr;
std::shared_ptr<ActivationFunction> Relu::instance = nullptr;


std::shared_ptr<ActivationFunction> getInstance(unsigned char code)
{
	switch (code)
	{
	case NO_ACTIVATION:
		return NoActivation::getInstance();
		break;

	case SIGMOID:
		return Sigmoid::getInstance();
		break;

	case RELU:
		return Relu::getInstance();
		break;
	}

	std::string error = "No function name coded ";
	error += std::to_string(code);
	throw std::exception(error.c_str());
}
