#include "Draw.h"

#define STR_LEN 128

// merge colors
Color InterpolateColor(Color color1, Color color2, float t)
{
	Color result;
	result.r = (unsigned char)(color1.r * (1.0f - t) + color2.r * t);
	result.g = (unsigned char)(color1.g * (1.0f - t) + color2.g * t);
	result.b = (unsigned char)(color1.b * (1.0f - t) + color2.b * t);

	result.a = 255;
	return result;
}


void TruthTable::draw(int x, int y, int w, int h)
{
	int FONT_SIZE_NORMAL = h / 30;
	int fontSize = 0;
	int rowY = 0;
	int startY = 0;

	std::ostringstream stringStream;
	std::string line;

	_network->printTruthTable(_input, stringStream);

	std::istringstream iss(stringStream.str());

	DrawText("Truth Table", x + (int)(w / 2) - 6 * FONT_SIZE_NORMAL, y - FONT_SIZE_NORMAL * 2, FONT_SIZE_NORMAL, LIGHTGRAY);

	while (std::getline(iss, line))
	{
		if (fontSize == 0)
		{
			fontSize = 1000 / line.size();

			startY = y + h / 2 - (fontSize * (_input.getRows() * 2 - 1) / 2);
		}

		DrawText(line.c_str(), x, startY, fontSize, WHITE);

		startY += fontSize;
	}
}



Plot::Plot(int graphSize, std::string name, std::function<float()> func)
	: _graphSize(graphSize), _name(name), _trackedFunction(func)
{
	;
}

void Plot::draw(int x, int y, int w, int h)
{
	float max = *std::max_element(_data.begin(), _data.end()), x1, x2, y1, y2;

	int FONT_SIZE = h / 30;
	int LITTLE_PAD = w / 120;

	int acctualWidth = w - LITTLE_PAD - FONT_SIZE;
	int acctualX = x + FONT_SIZE;

	for (size_t i = 0; i < _data.size() - 1; i++)
	{
		x1 = acctualX + (float)acctualWidth / _graphSize * i;
		y1 = y + (1 - (_data[i] / max)) * h; // y axis is from up to down

		x2 = acctualX + (float)acctualWidth / _graphSize * (i + 1);
		y2 = y + (1 - (_data[i + 1] / max)) * h;

		DrawLineEx(CLITERAL(Vector2) { x1, y1 }, CLITERAL(Vector2) { x2, y2 }, h * 0.004f, RED);

		DrawCircle((int)x1, (int)y1, h * 0.004f, RED); // draw point
	}

	char buff[STR_LEN] = "";

	snprintf(buff, STR_LEN, "%.3f", _data[_data.size() - 1]);

	std::string title = _name;
	title += ": " + std::string(buff);

	// draw title
	DrawText(title.c_str(), x + (int)(w / 2) - ((int)title.size() / 2) * FONT_SIZE, y - FONT_SIZE * 2, FONT_SIZE, LIGHTGRAY);


	memset(buff, 0, STR_LEN);
	snprintf(buff, STR_LEN, "%.2f", max);

	DrawText(buff, x, y - FONT_SIZE, FONT_SIZE, LIGHTGRAY);
	DrawText("0", x, y + h - FONT_SIZE, FONT_SIZE, LIGHTGRAY);

	// draw boundries
	DrawLine(acctualX, y, acctualX + acctualWidth, y, RED); // top left to top right
	DrawLine(acctualX, y + h, acctualX + acctualWidth, y + h, RED); // button left to buttom right
	DrawLine(acctualX + acctualWidth, y, acctualX + acctualWidth, y + h, RED); // top right to button right
	DrawLine(acctualX, y, acctualX, y + h, RED); // top left to buttom left
}

void Plot::update()
{
    if (_data.size() >= _graphSize) {
        _data.erase(_data.begin());  // Remove the oldest element (from the front)
    }
    _data.push_back(_trackedFunction());
}



ImageObject::ImageObject(int width, int height, std::vector<float> data) : _width(width), _height(height)
{
	assert(width * height == data.size());

	_img = GenImageColor(_width, _height, BLACK);
	unsigned char pixel;

	for (int y = 0; y < _height; y++)
	{
		for (int x = 0; x < _width; x++)
		{
			pixel = data[y * _width + x] * 255.f;

			ImageDrawPixel(&_img, x, y, Color{ pixel, pixel, pixel, 255 });
		}
	}
}

void ImageObject::draw(int x, int y, int w, int h)
{
	Texture2D texture = LoadTextureFromImage(_img);

	UpdateTexture(texture, _img.data);
	DrawTextureEx(texture, Vector2{(float)x, (float)y}, 0, 20, WHITE);
}

void ImageObject::update()
{
	;
}



ImageObjectNN::ImageObjectNN(int width, int height, nn* network) : ImageObject(width, height, std::vector<float>(width* height)), _network(network)
{
}

void ImageObjectNN::draw(int x, int y, int w, int h)
{
	unsigned char pixel;
	Mat input(1, 2), output;

	for (int y = 0; y < _height; y++)
	{
		for (int x = 0; x < _width; x++)
		{
			input(0, 0) = x;
			input(0, 1) = y;

			output = _network->forward(input);

			pixel = output(0, 0) * 255.f;

			ImageDrawPixel(&_img, x, y, Color{ pixel, pixel, pixel, 255 });
		}
	}
	
	Texture2D texture = LoadTextureFromImage(_img);

	UpdateTexture(texture, _img.data);
	DrawTextureEx(texture, Vector2{ (float)x, (float)y }, 0, 20, WHITE);
}

void ImageObjectNN::update()
{
	;
}



NNDrawObject::NNDrawObject(nn* other, Mat& input, Mat& output, float learningRate) : _network(other), _input(input), _output(output), _lr(learningRate)
{
	;
}

void NNDrawObject::draw(int x, int y, int w, int h)
{
	auto sig = Sigmoid::getInstance();

	const float NEURON_RADIOS = h * 0.04f;
	int FONT_SIZE = h / 30;
	int LITTLE_PAD = w / 120;
	const float THICK = h * 0.008f;
	const int borderV = 50;
	const int borderH = 50;


	std::vector<int> arch = _network->getArch();
	int archCount = (int)arch.size();

	int nnHeight = h - 2 * borderV;
	int nnWidth = w - 2 * borderH; // the room for the network

	int startX = x + w / 2 - nnWidth / 2;
	int startY = y + h / 2 - nnHeight / 2; // the start of the drawing

	int layerDistanceX = nnWidth / archCount; // distance between layers

	int layerX, layerY, nextLayerX, nextLayerY, layerDistanceY, nextLayerDistanceY;

	Color lowColor = DARKPURPLE;
	Color highColor = GREEN;

	DrawText("Neural Network:", x + (int)(w / 2) - (int)(FONT_SIZE * 7.5), y - FONT_SIZE * 2, FONT_SIZE, LIGHTGRAY);

	float value = 0;

	for (int layerIdx = 0; layerIdx < archCount; layerIdx++)
	{
		layerDistanceY = nnHeight / arch[layerIdx]; // distance between each neuron

		layerX = startX + layerIdx * layerDistanceX + layerDistanceX / 2;

		if (layerIdx > 0)
		{
			std::string activationName = _network->getNameOfActivation(layerIdx - 1);
			DrawText(activationName.c_str(), layerX - ((int)activationName.size() / 3) * FONT_SIZE, y, FONT_SIZE, LIGHTGRAY);
		}

		for (int neuron = 0; neuron < arch[layerIdx]; neuron++)
		{
			layerY = startY + neuron * layerDistanceY + layerDistanceY / 2;

			if (layerIdx + 1 < archCount) // if it is not the last layer
			{
				nextLayerDistanceY = nnHeight / (int)arch[layerIdx + 1];
				nextLayerX = startX + (layerIdx + 1) * layerDistanceX + layerDistanceX / 2;

				for (int j = 0; j < arch[layerIdx + 1]; j++)
				{
					nextLayerY = startY + j * nextLayerDistanceY + nextLayerDistanceY / 2;

					value = sig->calc(_network->getWeightsOfLayer(layerIdx)(neuron, j));
	
					Color merged = InterpolateColor(lowColor, highColor, value);
					
					value -= 0.5;
					value = fabs(2 * value);

					merged.a = (unsigned char)floorf(255.f * value);

					Vector2 start = { (float)layerX, (float)layerY };
					Vector2 end = { (float)nextLayerX, (float)nextLayerY };

					DrawLineEx(start, end, value * THICK, merged);
				}
			}

			switch (layerIdx)
			{
			case 0:
				DrawCircle(layerX, layerY, NEURON_RADIOS, LIGHTGRAY); // input neurons
				break;

			default:
				value = sig->calc(_network->getBiasesOfLayer(layerIdx - 1)(0, neuron));

				Color merged = InterpolateColor(lowColor, highColor, value);

				DrawCircle(layerX , layerY, NEURON_RADIOS, merged);
			}

		}
	}
}

void NNDrawObject::update()
{
	_network->train(_input, _output, _lr, epoch);

	epoch++;
}



void Drawer::simulate(size_t amountOfIterations)
{
	createWindow();

	size_t i = 0;

	while (!WindowShouldClose())
	{
		if (i < amountOfIterations)
		{
			if (IsKeyPressed(KEY_SPACE))
			{
				_paused = !_paused;
			}

			for (size_t j = 0; j < 103 && i < amountOfIterations && !_paused; j++)
			{
				for (RaylibObject* obj : _objects)
				{
					obj->update();
				}

				i++;
			}
		}

		draw(i, amountOfIterations);
	}

	CloseWindow();
}

void Drawer::draw(size_t i, size_t amountOfIterations)
{
	Color backgroundColor = { 0x18, 0x18, 0x18, 0xFF };

	int size = (int)_objects.size();

	if (size == 0)
		size = 1;


	_w = GetRenderWidth(), _h = GetRenderHeight();

	int widthForEachObject = _w / size;
	int heightForEachObject = _h * 2 / 3;
	int x = 3;
	int y = _h / 6;

	BeginDrawing();
	ClearBackground(backgroundColor);

	for (RaylibObject* obj : _objects)
	{
		obj->draw(x, y, widthForEachObject, heightForEachObject);

		x += widthForEachObject;
	}

	std::string title = "Iteration: ";

	title += std::to_string(i) + "/" + std::to_string(amountOfIterations);

	if (_paused)
		title += " | paused";

	DrawText(title.c_str(), 0, 0, (int)(_h * 0.04), LIGHTGRAY);

	EndDrawing();
}

void Drawer::createWindow()
{
	SetConfigFlags(FLAG_WINDOW_RESIZABLE);
	InitWindow(_w, _h, "Machine Learning");
	SetTargetFPS(_fps);
}
