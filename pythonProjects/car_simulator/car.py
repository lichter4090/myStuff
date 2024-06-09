from constants import *


CAR_OPTIONS = extract_files_from_folder("Assets", "car", CAR_WIDTH, CAR_HEIGHT)

ROTATION = 4


class Car(pygame.Rect):
    def __init__(self, x, y, color="cyan"):
        super().__init__(x, y, CAR_WIDTH, CAR_HEIGHT)
        self.image = CAR_OPTIONS[color]
        self.angle = 0

    def get_color(self):
        for key, value in CAR_OPTIONS.items():
            if value == self.image:
                return key

    def get_coordinates(self):
        return self.x, self.y

    def get_image(self):
        return self.image

    def set_image(self, color):
        if color not in CAR_OPTIONS.keys():
            return

        self.image = CAR_OPTIONS[color]

    def draw_car(self, window):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        window.blit(rotated_image, self.get_coordinates())

    def move_car(self, key_pressed):
        if key_pressed[pygame.K_RIGHT]:
            self.angle -= ROTATION

        if key_pressed[pygame.K_LEFT]:
            self.angle += ROTATION

    def get_angle(self):
        return self.angle
