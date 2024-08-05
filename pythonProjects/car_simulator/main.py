from car import Car, CAR_OPTIONS
from road import Track
from constants import *
import settings_window

pygame.init()
pygame.font.init()

SETTINGS_RECT = pygame.Rect(SETTINGS_COORDINATES, SETTINGS_COORDINATES, SETTINGS_SIZE, SETTINGS_SIZE)
SETTINGS_OPTIONS = extract_files_from_folder("Assets", "settings", SETTINGS_SIZE, SETTINGS_SIZE)
HOVERING_SETTINGS_BUTTON = False

SPEEDOMETER = pygame.Rect(SETTINGS_COORDINATES * 3, HEIGHT - SPEEDOMETER_SIZE - SETTINGS_COORDINATES, SPEEDOMETER_SIZE, SPEEDOMETER_SIZE)
RPM_METER = pygame.Rect(WIDTH - SETTINGS_COORDINATES * 30, HEIGHT - SPEEDOMETER_SIZE - SETTINGS_COORDINATES, SPEEDOMETER_SIZE, SPEEDOMETER_SIZE)
GEAR_METER = pygame.Rect(WIDTH - SETTINGS_COORDINATES * 30, HEIGHT - SPEEDOMETER_SIZE * 2 - SETTINGS_COORDINATES, SPEEDOMETER_SIZE, SPEEDOMETER_SIZE)


def draw_window(window, car, track):
    window.blit(BACKGROUND_IMAGE, (0, 0))
    track.draw_track(window)
    car.draw_car(window)

    if HOVERING_SETTINGS_BUTTON:
        window.blit(SETTINGS_OPTIONS["hover"], (SETTINGS_COORDINATES, SETTINGS_COORDINATES))

    else:
        window.blit(SETTINGS_OPTIONS["no-hover"], (SETTINGS_COORDINATES, SETTINGS_COORDINATES))

    pygame.draw.rect(window, BLACK, SETTINGS_RECT, width=1)

    draw_text(window, f"{abs(int(track.get_v() * (1 / 3)))}", SPEEDOMETER.center, big_font, BLACK)
    draw_text(window, f"{car.get_rpm()}", RPM_METER.center, big_font, BLACK)
    draw_text(window, f"{car.get_gear()}  |  {car.get_mode()}", GEAR_METER.center, big_font, BLACK)

    pygame.display.update()


def main():
    global HOVERING_SETTINGS_BUTTON
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    car = Car(CAR_MIDDLE, HEIGHT - CAR_HEIGHT - 10)
    track = Track(car)

    clock = pygame.time.Clock()
    to_exit = False

    while not to_exit:
        clock.tick(FPS)
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                to_exit = True

            if SETTINGS_RECT.collidepoint(mouse_x, mouse_y):
                HOVERING_SETTINGS_BUTTON = True
            else:
                HOVERING_SETTINGS_BUTTON = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if SETTINGS_RECT.collidepoint(mouse_x, mouse_y):
                    car.set_image(settings_window.main(list(CAR_OPTIONS.keys()), car.get_color()))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    car = Car(CAR_MIDDLE, HEIGHT - CAR_HEIGHT - 10, color=car.get_color())
                    track = Track(car)

                if event.key in (pygame.K_d, pygame.K_p, pygame.K_r, pygame.K_n):
                    car.set_mode(chr(event.key))

        key_pressed = pygame.key.get_pressed()

        if track.can_move_track():
            track.move_track(key_pressed)

        draw_window(window, car, track)

    pygame.quit()


if __name__ == "__main__":
    main()
