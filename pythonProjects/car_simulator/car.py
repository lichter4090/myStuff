import pygame.mixer

from constants import *
import math
from gear_box import AutoGearBox, GearBox
import threading
import io
from time import sleep


CAR_OPTIONS = extract_files_from_folder("Assets", "car", CAR_WIDTH, CAR_HEIGHT)


class ManualCar(pygame.Rect):
    def __init__(self, x, y, color="cyan", v=0):
        super().__init__(x, y, CAR_WIDTH, CAR_HEIGHT)
        self.image = CAR_OPTIONS[color]
        self.angle = 0
        self.v = v
        self.rpm = MIN_RPM
        self.hand_break = True
        self.gear_box = GearBox()

        self.engine_running = False
        self.car_running = True

        self.engine_sound_thread = None

        self.start_engine_thread = threading.Thread(target=self.start_engine, daemon=True)
        self.start_engine_thread.start()  # first engine starts

        self.engine_sound_thread = threading.Thread(target=self.engine_sound, daemon=True)
        self.engine_sound_thread.start()

    def engine_sound(self):
        prev_rpm = 0
        self.start_engine_thread.join()  # waits for the engine to start

        while self.engine_running:
            if self.rpm == prev_rpm:
                continue

            prev_rpm = self.rpm
            semitones = get_rpm_semitones(self.rpm, MAX_RPM)
            pitched_engine_sound = change_pitch(ENGINE_SOUND, semitones)

            byte_io = io.BytesIO()
            pitched_engine_sound.export(byte_io, format="wav")
            byte_io.seek(0)

            pygame.mixer.music.load(byte_io)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)

            sleep(0.05)

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
        return self.gear_box.get_gear()

    def wheel(self, right, left):
        if self.gear_box.get_gear() == REVERSE_GEAR:  # if in reverse
            right, left = left, right  # opposite the directions

        if self.v != 0:  # if car is moving
            if right:
                self.angle -= ROTATION

            if left:
                self.angle += ROTATION

    def pedals_and_engine(self, key_pressed):
        self.rpm -= int(self.rpm * 0.007)  # rpm always going down

        if self.rpm < MIN_RPM:
            self.rpm = MIN_RPM

        self.wheel(key_pressed[pygame.K_RIGHT], key_pressed[pygame.K_LEFT])

        # friction
        if self.v > 0:  # if going forward
            self.v -= FRICTION

        elif self.v < 0:  # backward
            self.v += FRICTION

        if key_pressed[pygame.K_UP] and self.engine_running:  # if pressed gas pedal and engine is running
            self.rpm += int((1 / self.rpm) * 1000 * 504)  # increase rpm
            # high rpm leads to slower rate of growth and the opposite

            if self.rpm > MAX_RPM:
                self.rpm = MAX_RPM

        elif key_pressed[pygame.K_DOWN] or self.hand_break:  # if pressed break pedal or hand break
            if self.v < MIN_RPM // 160 and not self.gear_box.is_neutral():
                raise StopWithoutClutch

            if abs(self.v) < 2 * MAX_ACC:
                self.v = 0

            elif self.v > 0:
                self.v -= MAX_ACC * 2

            else:
                self.v += MAX_ACC * 2

            # get the speed always towards 0

        if key_pressed[pygame.K_LCTRL]:  # if pressed clutch pedal
            self.gear_box.engage_clutch()

        else:  # if not
            self.gear_box.release_clutch()

    def switch_hand_break(self):
        self.hand_break = not self.hand_break

    def text(self):
        gear = self.gear_box.get_gear()
        t = str(gear)

        if gear == NEUTRAL_GEAR:
            t = "N"

        elif gear == REVERSE_GEAR:
            t = "R"

        if self.hand_break:
            t += " | P"

        return t

    def move_car(self, key_pressed):
        self.pedals_and_engine(key_pressed)

        if not self.gear_box.is_neutral():  # if wheels are connected to engine
            if self.v == 0 and self.gear_box.get_gear() not in (NEUTRAL_GEAR, 1):
                raise DidNotStartInFirstGear

            self.rpm -= GEAR_FRICTION  # gear friction

            if self.rpm < MIN_RPM:
                self.rpm = MIN_RPM

            suppose_to_be = int((self.rpm * self.gear_box.get_gear()) / 160)  # calculate the speed that the car should be based on the rpm and gear

            if abs(self.v - suppose_to_be) < MAX_ACC:
                self.v = suppose_to_be

            elif self.v <= suppose_to_be:
                self.v += MAX_ACC

            else:
                self.v -= MAX_ACC

        self.v = int(self.v)

        if self.car_running:  # if the car is running
            self.gear_box.shift(self.v, self.rpm, GearBox.extract_gear(key_pressed))

        return (self.v / 10) * math.sin(math.radians(self.angle)), (self.v / 10) * math.cos(math.radians(self.angle))
        # return the change in x-axis and change in y-axis
        # when angle is 0 the change will be only in y-axis (sin(0) == 0, cos(0) == 1)
        # when angle is 90 the change will be only in x-axis (sin(90) == 1, cos(90) == 0)

    def start_engine(self):
        sound = pygame.mixer.Sound("Assets/s.wav")
        sound.set_volume(1)
        sound.play()
        sleep(1.1)  # wait for the sound to end
        self.engine_running = True  # allows the user to press pedals and stuff

    def stop_engine(self):
        self.engine_running = False
        self.engine_sound_thread.join()  # wait for sound thread to end

    def lost(self):
        self.gear_box.engage_clutch()
        self.gear_box.shift(0, 0, NEUTRAL_GEAR)  # shift to neutral
        self.gear_box.release_clutch()

        self.hand_break = True

        self.car_running = False


class AutoCar(ManualCar):
    def __init__(self, x, y, color="cyan", v=0, auto=True):
        super().__init__(x, y, color, v)
        self.mode = "P"
        self.gear_box = AutoGearBox()

    def get_mode(self):
        return self.mode

    def switch_hand_break(self):
        pass

    def set_mode(self, mode):
        if self.mode == mode or not self.car_running or not self.engine_running:
            return

        self.mode = mode

        if mode == "D":
            self.hand_break = False
            self.gear_box.shift(0, 0, 1)

        elif mode == "P":
            self.hand_break = True
            self.gear_box.set_neutral()

        elif mode == "N":
            self.hand_break = False
            self.gear_box.set_neutral()

        elif mode == "R":
            self.gear_box.set_reverse()

    def text(self):
        gear = self.gear_box.get_gear()
        t = str(gear)

        if gear == NEUTRAL_GEAR:
            t = "N"

        elif gear == REVERSE_GEAR:
            t = "R"

        return f"{t} | {self.get_mode()}"

    def pedals_and_engine(self, key_pressed):
        self.rpm -= int(self.rpm * 0.007)  # rpm always goes down

        if self.rpm < MIN_RPM:
            self.rpm = MIN_RPM

        if self.v > 0:  # if going forward
            self.v -= FRICTION

        elif self.v < 0:  # backward
            self.v += FRICTION

        self.wheel(key_pressed[pygame.K_RIGHT], key_pressed[pygame.K_LEFT])

        if key_pressed[pygame.K_UP] and self.engine_running:  # if pressed gas pedal and engine is running
            self.rpm += int((1 / self.rpm) * 1000 * 504)  # increase rpm
            # high rpm leads to slower rate of growth and the opposite

            if self.rpm > MAX_RPM:
                self.rpm = MAX_RPM

        elif key_pressed[pygame.K_DOWN] or self.hand_break:  # if pressed break pedal or hand break
            if abs(self.v) < 2 * MAX_ACC:
                self.v = 0

            elif self.v > 0:
                self.v -= MAX_ACC * 2

            else:
                self.v += MAX_ACC * 2

            # get the speed always towards 0

        # check for mode change
        if key_pressed[pygame.K_d]:
            self.set_mode("D")

        elif key_pressed[pygame.K_p]:
            self.set_mode("P")

        elif key_pressed[pygame.K_r]:
            self.set_mode("R")

        elif key_pressed[pygame.K_n]:
            self.set_mode("N")

    def move_car(self, key_pressed):
        if not self.gear_box.is_neutral():  # if wheels are connected to engine
            self.rpm -= GEAR_FRICTION  # gear friction

            if self.rpm < MIN_RPM:
                self.rpm = MIN_RPM

            suppose_to_be = int((self.rpm * self.gear_box.get_gear()) / 160) + FRICTION  # calculate the speed that the car should be in based on the rpm and gear

            if abs(self.v - suppose_to_be) < MAX_ACC:
                self.v = suppose_to_be

            elif self.v <= suppose_to_be:
                self.v += MAX_ACC

            else:
                self.v -= MAX_ACC

        self.pedals_and_engine(key_pressed)
        self.v = int(self.v)

        self.gear_box.shift(self.v, self.rpm)

        return (self.v / 10) * math.sin(math.radians(self.angle)), (self.v / 10) * math.cos(math.radians(self.angle))

    def lost(self):
        self.set_mode("P")

        self.car_running = False
