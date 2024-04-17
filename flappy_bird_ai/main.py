import pygame.key

from constants import *
from bird import Bird
from pipe import Pipe

SCORE = 0


def draw_window(window, bird, pipes):
    window.blit(BACKGROUND, (0, 0))

    bird.draw(window)

    for pipe in pipes:
        pipe.draw(window)

    draw_text(window, f"{SCORE}", (WINDOW_SIZE // 2, TEXT_Y), big_font, black)
    pygame.display.update()


def main():
    global SCORE

    window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    bird = Bird()
    lst_of_pipes = []

    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()

    started = False
    to_exit = False

    while not to_exit:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                to_exit = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not started:
                    bird.reset()
                    lst_of_pipes = [Pipe()]
                    SCORE = 0

                bird.flap()
                started = True

        new_pipes = []

        try:
            if started:
                bird.move_single_frame()

                for pipe in lst_of_pipes:
                    try:
                        pipe.move_single_frame()
                        new_pipes.append(pipe)

                    except RuntimeError:
                        new_pipes.append(pipe)
                        new_pipes.append(Pipe())
                        SCORE += 1

                    except OSError:
                        pass
            else:
                new_pipes = lst_of_pipes.copy()

        except RuntimeError:
            started = False

        lst_of_pipes = new_pipes.copy()

        if started:
            for pipe in lst_of_pipes:
                if pipe.check_collide(bird):
                    started = False

        draw_window(window, bird, lst_of_pipes)


if __name__ == "__main__":
    main()
