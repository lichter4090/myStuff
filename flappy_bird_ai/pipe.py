import pygame.draw

from constants import *
from random import randint


class Pipe(pygame.Rect):
    def __init__(self):
        self.height_of_upper = randint(MIN_SIZE_OF_PIPE, WINDOW_SIZE - MIN_SIZE_OF_PIPE - PIPE_GAP)
        super().__init__(WINDOW_SIZE, self.height_of_upper + PIPE_GAP, PIPE_WIDTH, WINDOW_SIZE - self.height_of_upper - PIPE_GAP)
        # lower pipe is self

        self.send_point = True

    def move_single_frame(self):
        self.x += PIPE_SPEED

        if self.x + PIPE_WIDTH < 0:
            raise OSError  # means to remove the pipe from the list

        if self.send_point and self.x + PIPE_WIDTH < BIRD_X:
            self.send_point = False
            raise RuntimeError  # can add new pipe

    def draw(self, window):
        upper = pygame.transform.flip(pygame.transform.scale(PIPE_IMG, (PIPE_WIDTH, self.height_of_upper)), False, True)
        lower = pygame.transform.scale(PIPE_IMG, (PIPE_WIDTH, WINDOW_SIZE - self.y))

        window.blit(upper, (self.x, 0))
        window.blit(lower, (self.x, self.y))

    def check_collide(self, other: pygame.Rect):
        upper_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height_of_upper)

        return other.colliderect(upper_rect) or other.colliderect(self)
