from constants import *


class GearBox:
    def __init__(self):
        self.gear = NEUTRAL_GEAR
        self.clutch = False

    @staticmethod
    def extract_gear(key_pressed):
        lst_of_gears_pressed = [i - pygame.K_0 for i in range(pygame.K_0, pygame.K_6 + 1) if key_pressed[i]]  # get the gear keys that have been pressed (0-6)

        if len(lst_of_gears_pressed) > 1:  # if more than one gear
            raise MoreThanOneGear

        if len(lst_of_gears_pressed) == 1:
            return lst_of_gears_pressed[0]

        if key_pressed[pygame.K_r]:
            return REVERSE_GEAR

        return None

    def get_gear(self):
        return self.gear

    def set_neutral(self):
        self.gear = NEUTRAL_GEAR

    def set_reverse(self):
        self.gear = REVERSE_GEAR

    def engage_clutch(self):
        self.clutch = True

    def release_clutch(self):
        self.clutch = False

    def is_neutral(self):
        return self.gear == NEUTRAL_GEAR or self.clutch

    def shift(self, v, rpm, gear_to_shift_to=None):
        if gear_to_shift_to is None:
            return

        if not self.clutch:  # if clutch is not engaged
            raise ClutchNotIn

        self.gear = gear_to_shift_to


class AutoGearBox(GearBox):
    def __init__(self):
        super().__init__()
        self.cooldown = 0

    def on_cooldown(self):
        return self.cooldown > 0

    def shift(self, v, rpm, gear_to_shift_to=None):
        if gear_to_shift_to is not None:
            self.gear = gear_to_shift_to
            self.release_clutch()
            return

        if self.gear == REVERSE_GEAR:  # can't shift if in reverse (the mode drive will shift to first gear)
            return

        self.cooldown -= 1

        if self.cooldown <= 45:
            self.release_clutch()

        if self.on_cooldown():
            return

        if not self.is_neutral():  # if wheels are connected to engine
            if rpm > 3500 and self.gear != 6 and v >= self.gear * 20 - 10:  # condition for up shifting
                self.engage_clutch()
                self.gear += 1
                self.cooldown = 50

            elif self.gear != 1:
                min_speed = self.gear * 20 - 25

                if v < min_speed:  # condition for down shifting
                    self.engage_clutch()
                    self.gear -= 1
                    self.cooldown = 10
