import numpy as np

WINDOW_SIZE = (1280, 800)
WINDOW_SIZE = (1920, 1200)
WORKING_SIZE = (320, 200)
WORKING_SIZE = (640, 800)


COLORS = {
        "#": (50., 50., 50.),
        "A": (150., 0., 0.),
        "B": (0., 150., 0.),
        "C": (0., 0., 150.),
        "0": (255., 0., 0.),
        "1": (0., 255., 0.),
        "2": (0., 0., 255.),
        " ": (255., 255., 255.),
        "D": (50., 50., 50.),
        "E": (50., 50., 50.),
        "F": (50., 50., 50.),
        "G": (50., 50., 50.),
        "H": (50., 50., 50.),
        "I": (50., 50., 50.),
        "J": (50., 50., 50.),
        "K": (50., 50., 50.),
        }



GROUND_COLOR = (60, 20, 0)
#SKY_COLOR = (160, 230, 230)
SKY_COLOR = (0, 0, 0)

PLAYER_HEIGHT = 32

PLAYER_FOV = np.math.pi / 2.5

PLAYER_SPEED = 32
PLAYER_TURN_SPEED = 2

COLUMN_WIDTH = PLAYER_FOV / WORKING_SIZE[0]

DISTANCE_TO_PROJECTION_PLANE = (WORKING_SIZE[0] / 2) / np.math.tan(PLAYER_FOV / 2)