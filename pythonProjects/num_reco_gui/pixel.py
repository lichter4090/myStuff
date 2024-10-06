from pygame import Rect, Surface
from pygame.draw import rect as draw_rect
import numpy as np
from PIL import Image
from pygame.mouse import get_pressed, get_pos


GREY = (100, 100, 100)
BLACK = (0, 0, 0)


class Pixel(Rect):
    def __init__(self, x: int, y: int, size: int):
        super().__init__(x, y, size, size)

        self.color = GREY

    def change_color(self) -> bool:
        if self.color == BLACK:
            return False

        self.color = BLACK

        return True

    def reset(self) -> bool:
        if self.color == GREY:
            return False

        self.color = GREY

        return True

    def draw(self, window: Surface):
        draw_rect(window, self.color, self)

    def get_pixel_val(self):
        if self.color == GREY:
            return 0.0

        return 1.0


class PixelMat:
    def __init__(self, pixel_size: int, dim: int):
        self.mat = list()
        self.pic_size = pixel_size * dim
        self.pixel_size = pixel_size

        for y in range(0, self.pic_size, pixel_size):
            row = list()

            for x in range(0, self.pic_size, pixel_size):
                row.append(Pixel(x, y, pixel_size))

            self.mat.append(row)

    def __getitem__(self, row):
        return self.mat[row]

    def __setitem__(self, row, value):
        self.mat[row] = value

    def __delitem__(self, row):
        del self.data[row]

    def draw(self, window):
        for row in self.mat:
            for pixel in row:
                pixel.draw(window)

    def export_image(self) -> list[float]:
        lst_1d = list()

        for row in self.mat:
            lst_1d += list(map(lambda pixel: pixel.get_pixel_val(), row))

        return lst_1d

    def reset_mat(self):
        for row in self.mat:
            for pixel in row:
                pixel.reset()

    def export_image_png(self, file_path: str):
        # Export the pixel matrix as a 28x28 grayscale image
        pixel_data = np.array(self.export_image()).reshape(28, 28)

        # Convert the 0-1 matrix to a 0-255 grayscale matrix
        pixel_data = (pixel_data * 255).astype(np.uint8)

        # Create an image object from the pixel data
        img = Image.fromarray(pixel_data, mode='L')  # 'L' mode for grayscale

        # Save the image as a PNG
        img.save(file_path)

    def check_pixel_collide(self) -> bool:
        mouse_press = get_pressed()

        if mouse_press[0] or mouse_press[2]:
            mouse_x, mouse_y = get_pos()

            if 0 <= mouse_x <= self.pic_size and 0 <= mouse_y <= self.pic_size:
                col = mouse_x // self.pixel_size
                row = mouse_y // self.pixel_size

                if mouse_press[0]:
                    return self.mat[row][col].change_color()

                return self.mat[row][col].reset()

        return False
