#define _CRT_SECURE_NO_WARNINGS

#include "nn.h"
#include "Draw.h"



int main()
{
	int w = 1710, h = 900, fps = 60;

	Drawer drawer(w, h, fps);

	Mat input;
	Mat output = input.matLoadFromImage("data\\8.png");

	Mat originalI = input;
	Mat originalO = output;

	input.matMerge(output);
	input.matShuffleRows();

	output = input.matSplit(2);

	nn network(2);

	network.addLayer(6, Sigmoid::getInstance());
	network.addLayer(6, Sigmoid::getInstance());
	network.addLayer(1, Sigmoid::getInstance());

	NNDrawObject drawObject(&network, input, output, 20.f);
	Plot plt(100000, "Cost", [&](){ return network.costFunction(input, output);});


	ImageObject img(28, 28, originalO.create1dArray());
	ImageObjectNN im(28, 28, &network);

	drawer.addObject((RaylibObject*)&plt);
	drawer.addObject((RaylibObject*)&drawObject);
	drawer.addObject((RaylibObject*)&im);

	drawer.simulate(100000);

	std::cout << "Cost: " << network.costFunction(input, output) << "\n";

	network.save("nn.nn");
	return 0;
}
