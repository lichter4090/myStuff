#pragma once

#include <raylib.h>
#include <functional>
#include <tuple>
#include <sstream>
#include "nn.h"


class RaylibObject
{
public:	
	RaylibObject() { ; };

	virtual void draw(int x, int y, int w, int h) = 0;
	virtual void update() = 0;
};


class TruthTable : RaylibObject
{
public:
	TruthTable(nn* network, Mat& input) : _network(network), _input(input) { ; }

	virtual void draw(int x, int y, int w, int h) override;
	virtual void update() override { ; } // only show results in draw function

private:
	nn* _network;
	Mat _input;
};

// class for plotting a positive only function
class Plot : public RaylibObject
{
public:
	Plot(int graphSize, std::string name, std::function<float()> func);

	virtual void draw(int x, int y, int w, int h) override;
	virtual void update() override;

private:
	int _graphSize;
	std::string _name;
	std::function<float()> _trackedFunction; // Function to track
	std::vector<float> _data;
};


class ImageObject : public RaylibObject
{
public:
	ImageObject(int width, int height, std::vector<float> data);

	virtual void draw(int x, int y, int w, int h) override;
	virtual void update() override;

protected:
	int _width;
	int _height;

	Image _img;
};


class ImageObjectNN : public ImageObject
{
public:	
	ImageObjectNN(int width, int height, nn* network);

	virtual void draw(int x, int y, int w, int h) override;
	virtual void update() override;


private:
	nn* _network;
};


class NNDrawObject : public RaylibObject
{
public:
	NNDrawObject(nn* other, Mat& input, Mat& output, float learningRate);

	virtual void draw(int x, int y, int w, int h) override;
	virtual void update() override;

private:
	size_t epoch=0;

	nn* _network;
	Mat _input, _output;

	float _lr;
};


class Drawer
{
public:	
	Drawer(int w, int h, int fps) : _w(w), _h(h), _fps(fps) { ; }

	void addObject(RaylibObject* obj) { _objects.push_back(obj); }
	void simulate(size_t amountOfIterations);


private:
	int _w, _h, _fps;
	bool _paused = false;

	std::vector<RaylibObject*> _objects;

	void draw(size_t i, size_t amountOfIterations);
	void createWindow();
};
