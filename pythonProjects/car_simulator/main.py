from car import AutoCar, ManualCar, CAR_OPTIONS
from road import Track
from constants import *
import settings_window


HOVERING_SETTINGS_BUTTON = False
HOVERING_INFO_BUTTON = False
MANUAL = True


def restart_car(old_car=None):
    color = "cyan"

    if old_car:
        old_car.stop_engine()
        color = old_car.get_color()
        del old_car

    if MANUAL:
        car = ManualCar(CAR_MIDDLE, HEIGHT - CAR_HEIGHT - 10, color=color)

    else:
        car = AutoCar(CAR_MIDDLE, HEIGHT - CAR_HEIGHT - 10, color=color)

    track = Track(car)

    return car, track


def draw_window(window, car, track):
    window.blit(BACKGROUND_IMAGE, (0, 0))
    track.draw_track(window)
    car.draw_car(window)

    if HOVERING_SETTINGS_BUTTON:
        window.blit(SETTINGS_OPTIONS["hover"], (SETTINGS_COORDINATES, SETTINGS_COORDINATES))

    else:
        window.blit(SETTINGS_OPTIONS["no-hover"], (SETTINGS_COORDINATES, SETTINGS_COORDINATES))

    if HOVERING_INFO_BUTTON:
        pygame.draw.rect(window, LIGHT_GRAY, INFO_RECT)

    pygame.draw.rect(window, BLACK, INFO_RECT, width=1)

    text_rect = INFO_TEXT.get_rect()
    text_rect.center = INFO_RECT.center
    window.blit(INFO_TEXT, text_rect)

    pygame.draw.rect(window, BLACK, SETTINGS_RECT, width=1)

    draw_text(window, f"{abs(track.get_v())}", SPEEDOMETER.center, big_font, BLACK)
    draw_text(window, f"{car.get_rpm()}", RPM_METER.center, big_font, BLACK)
    draw_text(window, car.text(), GEAR_METER.center, big_font, BLACK)

    if MANUAL:
        draw_text(window, "M", MANUAL_INDICATOR.center, little_font, RED)

    pygame.display.update()


def main():
    global HOVERING_SETTINGS_BUTTON, HOVERING_INFO_BUTTON, MANUAL

    window = pygame.display.set_mode((WIDTH, HEIGHT))

    car, track = restart_car()

    clock = pygame.time.Clock()
    to_exit = False
    restart = False

    while not to_exit:
        clock.tick(FPS)
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                to_exit = True

            HOVERING_SETTINGS_BUTTON = SETTINGS_RECT.collidepoint(mouse_x, mouse_y)
            HOVERING_INFO_BUTTON = INFO_RECT.collidepoint(mouse_x, mouse_y)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if SETTINGS_RECT.collidepoint(mouse_x, mouse_y):
                    color, manual = settings_window.main(list(CAR_OPTIONS.keys()), car.get_color(), MANUAL)

                    car.set_image(color)

                    if manual != MANUAL:
                        MANUAL = manual
                        restart = True

                if INFO_RECT.collidepoint(mouse_x, mouse_y):
                    info()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    restart = True

                if event.key == pygame.K_p:
                    car.switch_hand_break()

        if restart:
            car, track = restart_car(car)
            restart = False

            continue

        key_pressed = pygame.key.get_pressed()

        try:
            change_x, change_y = car.move_car(key_pressed)
        except Exception as e:
            pop_msg("Engine failure", str(e))
            restart = True
            continue

        if track.can_move_track():
            track.move_track(change_x, change_y)

        draw_window(window, car, track)

    pygame.quit()


if __name__ == "__main__":
    main()
