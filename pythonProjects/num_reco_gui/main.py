from model_loader import Model
import pygame
from pixel import *

pygame.init()


PIXEL_SIZE = 20
PIC_SIZE = 28

FPS = 60

WHITE = (255, 255, 255)

FONT_SIZE = 20

HEIGHT = PIXEL_SIZE * PIC_SIZE + FONT_SIZE * 2
WIDTH = PIXEL_SIZE * PIC_SIZE

little_font = pygame.font.Font('freesansbold.ttf', FONT_SIZE)


def draw_text(window: pygame.Surface, text: str, center_coordinates: tuple[int, int], font: pygame.font.Font, color: tuple[int, int, int]):
    label = font.render(text, True, color)
    text_rect = label.get_rect()
    text_rect.center = center_coordinates
    window.blit(label, text_rect)


def draw(window: pygame.Surface, pixels: PixelMat, model: Model):
    window.fill(WHITE)

    pixels.draw(window)

    text = model.get_predicted_num()

    if text is not None:
        conf = model.get_confidence() * 100
        text = f"Predicted Number: {text} | Model Confidence: {conf:.2f}%"
    else:
        text = ""

    draw_text(window, text, (WIDTH // 2, HEIGHT - FONT_SIZE), little_font, BLACK)

    pygame.display.update()


def main(model_file_name: str):
    model = Model(model_file_name)

    pixels = PixelMat(PIXEL_SIZE, PIC_SIZE)

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Number Recognition")
    clock = pygame.time.Clock()

    to_run = True

    while to_run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                to_run = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pixels.reset_mat()
                model.predict_image(pixels.export_image())

        if pixels.check_pixel_collide():
            model.predict_image(pixels.export_image())

        draw(window, pixels, model)


if __name__ == "__main__":
    main("model.h5")
