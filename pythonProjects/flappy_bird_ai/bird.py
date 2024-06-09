from pygame import Rect
from constants import *


class Bird(Rect):
    def __init__(self, x=BIRD_X, y=BIRD_Y):
        super().__init__(x, y, BIRD_DIM, BIRD_DIM)
        self.v = 0

    def reset(self):
        self.x = BIRD_X
        self.y = BIRD_Y

    def flap(self):
        self.v = -1 * flap

    def move_single_frame(self):
        self.v += g
        self.y += self.v

        if self.y < 0:
            self.y = 0
            self.v = 0

        elif self.y + BIRD_DIM > WINDOW_SIZE:
            self.y = WINDOW_SIZE - BIRD_DIM
            raise RuntimeError

    def draw(self, window):
        rotated = pygame.transform.rotate(BIRD_IMG, self.v * -FLAP_ANGLE)
        window.blit(rotated, (self.x, self.y))

