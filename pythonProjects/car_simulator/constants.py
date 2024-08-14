import os
import pygame
from pydub import AudioSegment
from tkinter import messagebox


pygame.init()
pygame.font.init()
pygame.mixer.init()

# fonts
little_font = pygame.font.Font('freesansbold.ttf', 20)
mid_font = pygame.font.Font('freesansbold.ttf', 40)
big_font = pygame.font.Font('freesansbold.ttf', 60)

# window constants
WIDTH, HEIGHT = 600, 600
BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load("Assets/background.jpg"), (WIDTH, HEIGHT))
FPS = 60

# car
CAR_WIDTH = 75
CAR_HEIGHT = 165
CAR_MIDDLE = WIDTH // 2 - CAR_WIDTH // 2

# road
ROAD_WIDTH = 200
ROAD_HEIGHT = HEIGHT
ROAD_MIDDLE = WIDTH // 2 - ROAD_WIDTH // 2

# speed constants
MAX_ACC = 2
FRICTION = 0.05
GEAR_FRICTION = 5
MAX_RPM = 8000
MIN_RPM = 1000

# gearbox constants
NEUTRAL_GEAR = 0
REVERSE_GEAR = -1

# colors
GREY = 75, 75, 75
BLACK = 0, 0, 0
RED = 240, 20, 20
LIGHT_GRAY = 200, 200, 200
WHITE = 255, 255, 255

# settings and icons size
SETTINGS_SIZE = 40
SETTINGS_COORDINATES = 5
SPEEDOMETER_SIZE = 100

# wheel
ROTATION = 4


def extract_files_from_folder(folder_name, key_name, w, h, key_word_for_opposite="aaaaaaaaa"):
    files = {}
    for filename in os.listdir(folder_name):
        if key_name in filename:
            image = pygame.image.load(os.path.join(folder_name, filename))

            if key_word_for_opposite in filename:
                scaled_image = pygame.transform.scale(image, (h, w))

            else:
                scaled_image = pygame.transform.scale(image, (w, h))

            files[filename.split("_")[0]] = scaled_image

    return files


def draw_text(window, text, center_coordinates, font, color):
    label = font.render(text, True, color)
    text_rect = label.get_rect()
    text_rect.center = center_coordinates
    window.blit(label, text_rect)


# my exceptions
class ClutchNotIn(Exception):
    def __str__(self):
        return "Shifted Without Engaging Clutch"


class MoreThanOneGear(Exception):
    def __str__(self):
        return "Shifted To More Than One Gear"


class StopWithoutClutch(Exception):
    def __str__(self):
        return "Stopped Without Engaging Clutch"


class DidNotStartInFirstGear(Exception):
    def __str__(self):
        return "Start Driving Only In First Gear"


# icons and meters on screen
SETTINGS_RECT = pygame.Rect(SETTINGS_COORDINATES, SETTINGS_COORDINATES, SETTINGS_SIZE, SETTINGS_SIZE)
SETTINGS_OPTIONS = extract_files_from_folder("Assets", "settings", SETTINGS_SIZE, SETTINGS_SIZE)

SPEEDOMETER = pygame.Rect(SETTINGS_COORDINATES * 3, HEIGHT - SPEEDOMETER_SIZE - SETTINGS_COORDINATES, SPEEDOMETER_SIZE, SPEEDOMETER_SIZE)
RPM_METER = pygame.Rect(WIDTH - SETTINGS_COORDINATES * 30, HEIGHT - SPEEDOMETER_SIZE - SETTINGS_COORDINATES, SPEEDOMETER_SIZE, SPEEDOMETER_SIZE)
GEAR_METER = pygame.Rect(WIDTH - SETTINGS_COORDINATES * 30, HEIGHT - SPEEDOMETER_SIZE * 2 - SETTINGS_COORDINATES, SPEEDOMETER_SIZE, SPEEDOMETER_SIZE)
MANUAL_INDICATOR = pygame.Rect(SETTINGS_COORDINATES, SETTINGS_COORDINATES * 10, SETTINGS_SIZE, SETTINGS_SIZE)

# info button
INFO_RECT = pygame.Rect(WIDTH - SETTINGS_SIZE - SETTINGS_COORDINATES, SETTINGS_COORDINATES, SETTINGS_SIZE, SETTINGS_SIZE)
INFO_TEXT = mid_font.render("i", True, BLACK)


# sound functions:
ENGINE_SOUND = AudioSegment.from_file("Assets/sound.wav")


def change_pitch(audio_segment: AudioSegment, semitones):
    """ Change the pitch of the audio segment by a number of semitones. """
    new_sample_rate = int(audio_segment.frame_rate * (2.0 ** (semitones / 12.0)))
    pitched_audio = audio_segment._spawn(audio_segment.raw_data, overrides={'frame_rate': new_sample_rate})
    return pitched_audio.set_frame_rate(audio_segment.frame_rate)


def get_rpm_semitones(rpm, max_rpm):
    return (rpm / max_rpm) * 20 - 5


def pop_msg(title, text):
    messagebox.showinfo(title, text)


def info():
    message = """Hi! This is my car simulator.
Use the up arrow for gas and down arrow for break.

There are two kinds of simulators: Auto transmission gear and manual one.
For the auto one, you can switch between the driving modes, D (drive), R (reverse), P (parking), N (neutral) By pressing their key on the keyboard.
For the manual one, you can switch the gear by engaging the clutch (Left ctrl button) and clicking on the number of the gear you want.
In manual mode, the key p raises the hand break, 0 is neutral gear and the key r is reverse gear.
The meter in the bottom left is your speed and the meter in bottom right is the rpm, on top of the rpm meter there is the gear you in and mode you are if you are in auto transmission car.
If you got out of the track press Space key to restart."""

    pop_msg("hello", message)

