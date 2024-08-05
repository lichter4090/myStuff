from constants import *


class GearBox:
    def __init__(self):
        self.gear = NEUTRAL_GEAR
        self.clutch = True
        self.cooldown = 0

    def get_gear(self):
        return self.gear

    def set_neutral(self):
        self.gear = NEUTRAL_GEAR

    def is_neutral(self):
        return self.gear == NEUTRAL_GEAR or self.clutch

    def shift(self, v, rpm, gear_to_shift_to=None):
        raise NotImplementedError("Abstract class!")

    def on_cooldown(self):
        return self.cooldown > 0


class AutoGearBox(GearBox):
    def __init__(self):
        super().__init__()

    def shift(self, v, rpm, gear_to_shift_to=None):
        if gear_to_shift_to is not None:
            self.gear = gear_to_shift_to
            self.clutch = False
            return

        self.cooldown -= 1

        if self.on_cooldown():
            return

        self.clutch = False

        if not self.is_neutral():
            if rpm > 3500 and self.gear != 6:
                #self.clutch = True
                self.gear += 1
                self.cooldown = 20

            elif self.gear != 1:
                min_speed = self.gear * 20 - 30

                if v < min_speed:
                    #self.clutch = True
                    self.gear -= 1
                    #self.cooldown = 20
