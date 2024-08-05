from constants import *
import math
from gear_box import AutoGearBox


CAR_OPTIONS = extract_files_from_folder("Assets", "car", CAR_WIDTH, CAR_HEIGHT)


class Car(pygame.Rect):
    def __init__(self, x, y, color="cyan", v=0, auto=True):
        super().__init__(x, y, CAR_WIDTH, CAR_HEIGHT)
        self.image = CAR_OPTIONS[color]
        self.angle = 0
        self.v = v
        self.rpm = 1000
        self.parking = True
        self.mode = "P"

        if auto:
            self.gear_box = AutoGearBox()

        else:
            pass
            # self.gear_box = ManualGearBox()

    def get_mode(self):
        return self.mode

    def set_mode(self, mode):
        self.mode = mode.upper()

        if mode == "d":
            self.parking = False
            self.gear_box.shift(0, 0, 1)

        elif mode == "p":
            self.parking = True
            self.gear_box.set_neutral()

        elif mode == "n":
            self.gear_box.set_neutral()

        else:
            pass
            # self.gear = REVERSE GEAR

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

    def get_angle(self):
        return self.angle

    def get_v(self):
        return self.v

    def get_rpm(self):
        return self.rpm

    def get_gear(self):
        #if self.gear_box.is_neutral():
        #   return "N"

        return self.gear_box.get_gear()

    def move_car(self, key_pressed):
        self.rpm -= int(self.rpm * 0.01)

        if self.rpm < 1000:
            self.rpm = 1000

        if self.v != 0:
            if key_pressed[pygame.K_RIGHT]:
                self.angle -= ROTATION

            if key_pressed[pygame.K_LEFT]:
                self.angle += ROTATION

        if key_pressed[pygame.K_UP] and not self.gear_box.on_cooldown():
            self.rpm += int((1 / self.rpm) * 1000 * 640)

            if self.rpm > 8000:
                self.rpm = 8000

        elif key_pressed[pygame.K_DOWN] or self.parking:
            self.v -= MAX_ACC

            if self.v < 0:
                self.v = 0

        if self.v > 0:  # if going forward
            self.v -= FRICTION

        elif self.v < 0:  # backward
            self.v += FRICTION

        if not self.gear_box.is_neutral():
            self.rpm -= GEAR_FRICTION

            suppose_to_be = int((self.rpm * self.gear_box.get_gear()) / 100)

            if self.v < suppose_to_be:
                self.v += 0.8 * MAX_ACC

            if self.v > suppose_to_be:
                self.v = suppose_to_be

        self.gear_box.shift(self.v, self.rpm)


        return (self.v / 10) * math.sin(math.radians(self.angle)), (self.v / 10) * math.cos(math.radians(self.angle))
