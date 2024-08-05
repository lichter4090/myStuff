from constants import *
import math
from random import choice
from car import Car


ROAD_OPTIONS = extract_files_from_folder("Assets", "road", ROAD_WIDTH, ROAD_HEIGHT, key_word_for_opposite="horizontal")


class Road(pygame.Rect):
    def __init__(self, x, y, w=ROAD_WIDTH, h=ROAD_HEIGHT, left_turn=None):
        super().__init__(x, y, w, h)
        self.vertical = h > w
        self.left_turn = None

        if not self.vertical:
            self.left_turn = left_turn

    def get_coordinates(self):
        return self.x, self.y


class Track:
    def __init__(self, car):
        self.roads = [Road(ROAD_MIDDLE, 0)]
        self.last_road = self.roads[-1]
        self.car = car

    def get_v(self):
        return self.car.get_v()

    def update_last(self):
        self.last_road = self.roads[-1]

    def draw_track(self, window):
        last_one = None
        for road in self.roads:
            if road.vertical:
                if last_one is not None and not last_one.vertical:  # if the last one was a vertical road
                    if last_one.left_turn:
                        window.blit(ROAD_OPTIONS["vertical-left"], road.get_coordinates())

                    else:
                        window.blit(ROAD_OPTIONS["vertical-right"], road.get_coordinates())

                else:
                    window.blit(ROAD_OPTIONS["vertical"], road.get_coordinates())

            else:
                if last_one is not None and last_one.left_turn == road.left_turn:
                    window.blit(ROAD_OPTIONS["horizontal"], road.get_coordinates())

                elif road.left_turn:
                    window.blit(ROAD_OPTIONS["horizontal-left"], road.get_coordinates())

                else:
                    window.blit(ROAD_OPTIONS["horizontal-right"], road.get_coordinates())

            #  pygame.draw.rect(window, GREY, road)

            last_one = road

    def get_new_road(self):
        options = list()

        if self.last_road.vertical:
            options.append(Road(self.last_road.x, self.last_road.y - ROAD_HEIGHT))  # straight
            options.append(Road(self.last_road.x + ROAD_WIDTH - ROAD_HEIGHT, self.last_road.y - ROAD_WIDTH, w=ROAD_HEIGHT, h=ROAD_WIDTH, left_turn=True))  # left turn
            options.append(Road(self.last_road.x, self.last_road.y - ROAD_WIDTH, w=ROAD_HEIGHT, h=ROAD_WIDTH, left_turn=False))  # right turn

        else:
            if self.last_road.left_turn:  # last one was a left turn
                options.append(Road(self.last_road.x, self.last_road.y + self.last_road.height - ROAD_HEIGHT))  # up
                options.append(Road(self.last_road.x - self.last_road.width, self.last_road.y, w=ROAD_HEIGHT, h=ROAD_WIDTH, left_turn=True))  # straight

            else:  # last one was a right turn
                options.append(Road(self.last_road.x + self.last_road.width - self.last_road.height, self.last_road.y + self.last_road.height - ROAD_HEIGHT))  # up
                options.append(Road(self.last_road.x + self.last_road.width, self.last_road.y, w=ROAD_HEIGHT, h=ROAD_WIDTH, left_turn=False))  # straight

        return choice(options)

    def is_track_moving(self):
        return self.car.get_v() != 0

    def can_move_track(self):
        for road in self.roads:
            if road.colliderect(self.car):
                return True

        return False

    def move_track(self, key_pressed):
        change_x, change_y = self.car.move_car(key_pressed)

        for idx, road in enumerate(self.roads):
            road.x += change_x
            road.y += change_y

            if road.y > HEIGHT:
                self.roads.remove(road)

        if len(self.roads) < 10:
            new_road = self.get_new_road()

            self.roads.append(new_road)
            self.update_last()
