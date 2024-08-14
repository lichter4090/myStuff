from constants import *
from random import choice
from car import ManualCar


ROAD_OPTIONS = extract_files_from_folder("Assets", "road", ROAD_WIDTH, ROAD_HEIGHT, key_word_for_opposite="horizontal")


class Road(pygame.Rect):
    def __init__(self, x, y, image, w=ROAD_WIDTH, h=ROAD_HEIGHT, left_turn=None):
        super().__init__(x, y, w, h)
        self.vertical = h > w
        self.left_turn = None
        self.image = image

        if not self.vertical:  # if not a vertical road
            self.left_turn = left_turn

    def get_coordinates(self):
        return self.x, self.y

    def get_image(self):
        return self.image


class Track:
    def __init__(self, car: ManualCar):
        self.roads = [Road(ROAD_MIDDLE, 0, ROAD_OPTIONS["vertical"])]
        self.last_road = self.roads[-1]
        self.car = car

    def get_v(self):
        return self.car.get_v()

    def update_last(self):
        self.last_road = self.roads[-1]

    def draw_track(self, window):
        for road in self.roads:
            window.blit(road.get_image(), road.get_coordinates())

    def get_new_road(self):
        options = list()

        if self.last_road.vertical:
            options.append(Road(self.last_road.x, self.last_road.y - ROAD_HEIGHT, ROAD_OPTIONS["vertical"]))  # straight
            options.append(Road(self.last_road.x + ROAD_WIDTH - ROAD_HEIGHT, self.last_road.y - ROAD_WIDTH, ROAD_OPTIONS["horizontal-left"], w=ROAD_HEIGHT, h=ROAD_WIDTH, left_turn=True))  # left horizontal turn
            options.append(Road(self.last_road.x, self.last_road.y - ROAD_WIDTH, ROAD_OPTIONS["horizontal-right"], w=ROAD_HEIGHT, h=ROAD_WIDTH, left_turn=False))  # right horizontal turn

        else:  # last road was a horizontal road
            if self.last_road.left_turn:  # if last one was a horizontal left turn
                options.append(Road(self.last_road.x - ROAD_WIDTH, self.last_road.y + self.last_road.height - ROAD_HEIGHT, ROAD_OPTIONS["vertical-left"]))  # up vertical road
                options.append(Road(self.last_road.x - self.last_road.width, self.last_road.y, ROAD_OPTIONS["horizontal"], w=ROAD_HEIGHT, h=ROAD_WIDTH, left_turn=True))  # continue going horizontal

            else:  # last one was a right turn
                options.append(Road(self.last_road.x + self.last_road.width, self.last_road.y + self.last_road.height - ROAD_HEIGHT, ROAD_OPTIONS["vertical-right"]))  # up vertical road
                options.append(Road(self.last_road.x + self.last_road.width, self.last_road.y, ROAD_OPTIONS["horizontal"], w=ROAD_HEIGHT, h=ROAD_WIDTH, left_turn=False))  # continue going horizontal

        return choice(options)  # pick random option

    def is_track_moving(self):
        return self.car.get_v() != 0

    def can_move_track(self):
        for road in self.roads:
            if road.colliderect(self.car):
                return True  # if at least one road collides with the car then the track can move

        self.car.lost()
        return False

    def move_track(self, change_x, change_y):
        for idx, road in enumerate(self.roads):
            road.x += change_x
            road.y += change_y

            if road.y > HEIGHT:
                self.roads.remove(road)

        if len(self.roads) < 10:  # if there are less than 10 roads
            new_road = self.get_new_road()

            self.roads.append(new_road)
            self.update_last()
