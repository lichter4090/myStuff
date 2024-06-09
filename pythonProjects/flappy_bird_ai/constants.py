import pygame

WINDOW_SIZE = 500
BIRD_DIM = 35
BIRD_X = 100
BIRD_Y = int(WINDOW_SIZE // 2 - BIRD_DIM // 2)

FPS = 60

white = (255, 255, 255)
yellow = (255, 255, 0)
black = (0, 0, 0)

g = 0.45
flap = 9

BIRD_IMG = pygame.transform.scale(pygame.image.load("img/bird.png"), (BIRD_DIM, BIRD_DIM))
FLAP_ANGLE = 4.5


PIPE_SPEED = -3
MIN_SIZE_OF_PIPE = BIRD_DIM + 5
PIPE_GAP = BIRD_DIM + 100
PIPE_WIDTH = 50
PIPE_IMG = pygame.image.load("img/pipe.png")

BACKGROUND = pygame.transform.scale(pygame.image.load("img/background.jpg"), (WINDOW_SIZE, WINDOW_SIZE))

pygame.font.init()
big_font = pygame.font.Font('freesansbold.ttf', 60)
little_font = pygame.font.Font('freesansbold.ttf', 20)


def draw_text(window, text, center_coordinates, font, color):
    label = font.render(text, True, color)
    text_rect = label.get_rect()
    text_rect.center = center_coordinates
    window.blit(label, text_rect)


TITLE_Y = 20
TEXT_Y = TITLE_Y + 30
START_TEMP = 10
