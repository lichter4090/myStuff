import os
import pygame


pygame.font.init()
little_font = pygame.font.Font('freesansbold.ttf', 20)
big_font = pygame.font.Font('freesansbold.ttf', 60)


WIDTH, HEIGHT = 600, 600
BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load("Assets/background.jpg"), (WIDTH, HEIGHT))
FPS = 60

CAR_WIDTH = 75
CAR_HEIGHT = 165
CAR_MIDDLE = WIDTH // 2 - CAR_WIDTH // 2

ROAD_WIDTH = 200
ROAD_HEIGHT = HEIGHT
ROAD_MIDDLE = WIDTH // 2 - ROAD_WIDTH // 2

MAX_ACC = 2
FRICTION = 1
MAX_SPEED = 150

GREY = 75, 75, 75
BLACK = 0, 0, 0

SETTINGS_SIZE = 40
SETTINGS_COORDINATES = 5

SPEEDOMETER_SIZE = 50


def extract_files_from_folder(folder_name, key_name, w, h, key_word_for_opposite="aaaaaaaaa"):
    files = {}
    for filename in os.listdir(folder_name):
        if key_name in filename:
            image = pygame.image.load(os.path.join(folder_name, filename))

            if key_word_for_opposite in filename:
                scaled_image = pygame.transform.scale(image, (h, w))

            else:
                scaled_image = pygame.transform.scale(image, (w, h))

            files[filename.split("_")[0]] = scaled_image

    return files
