#pragma once

#include <math.h>
#include <memory>
#include <string>

enum CODES {NO_ACTIVATION, SIGMOID, RELU};

class ActivationFunction
{
public:	
	virtual const float calc(float x) const = 0;
	virtual const float calc_derivative(float x) const = 0; 

	virtual const char* name() const = 0;
	virtual unsigned char code() const = 0;
};

class NoActivation : public ActivationFunction
{
public:
	virtual const float calc(float x) const override { return x; };
	virtual const float calc_derivative(float x) const override { return 1; }

	static std::shared_ptr<ActivationFunction> getInstance() { if (!instance) { instance = std::shared_ptr<ActivationFunction>(new NoActivation); } return instance; }

	virtual const char* name() const override { return "No Activation"; }
	virtual unsigned char code() const override { return NO_ACTIVATION; }

private:
	static std::shared_ptr<ActivationFunction> instance;
};

class Sigmoid : public ActivationFunction
{
public:
	virtual const float calc(float x) const override { return 1.f / (1.f + expf(-x)); }
	virtual const float calc_derivative(float x) const override { return x * (1 - x); }

	static std::shared_ptr<ActivationFunction> getInstance() { if (!instance) { instance = std::shared_ptr<ActivationFunction>(new Sigmoid); } return instance; }

	virtual const char* name() const override { return "Sigmoid"; }
	virtual unsigned char code() const override { return SIGMOID; }

private:
	static std::shared_ptr<ActivationFunction> instance;
};

class Relu : public ActivationFunction
{
public:
	virtual const float calc(float x) const override { if (x > 0) { return x; } return 0; }
	virtual const float calc_derivative(float x) const override { if (x > 0) { return 1; } return 0; }

	static std::shared_ptr<ActivationFunction> getInstance() { if (!instance) { instance = std::shared_ptr<ActivationFunction>(new Relu); } return instance; }

	virtual const char* name() const override { return "Relu"; }
	virtual unsigned char code() const override { return RELU; }

private:
	static std::shared_ptr<ActivationFunction> instance;
};


std::shared_ptr<ActivationFunction> getInstance(unsigned char code);
