#include "nn.h"
#include "Draw.h"


std::vector<float> input_arr = {
0, 0,
0, 1,
1, 0,
1, 1
};

std::vector<float> output_arr = {
0,
1,
1,
0
};


int main()
{
	int w = 1710, h = 900, fps = 60;

	Drawer drawer(w, h, fps);

	Mat input(4, 2);
	Mat output(4, 1);

	input.matInitArr(input_arr);
	output.matInitArr(output_arr);

	nn network(2);

	network.addLayer(2, Sigmoid::getInstance());
	network.addLayer(1, Sigmoid::getInstance());

	NNDrawObject drawObject(&network, input, output, 1.f);
	Plot plt(100000, "Cost", [&](){ return network.costFunction(input, output);});
	TruthTable tt(&network, input);


	drawer.addObject((RaylibObject*)&plt);
	drawer.addObject((RaylibObject*)&drawObject);
	drawer.addObject((RaylibObject*)&tt);


	drawer.simulate(100000);

	std::cout << network << "\n";

	network.printTruthTable(input);

	std::cout << "Cost: " << network.costFunction(input, output) << "\n";

	return 0;
}
