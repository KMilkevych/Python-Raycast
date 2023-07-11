import numpy as np

WINDOW_SIZE = (1280, 800)
WINDOW_SIZE = (1280, 720)
WORKING_SIZE = (320, 200)
WORKING_SIZE = (320, 400)

GROUND_COLOR = (60, 20, 0)
#SKY_COLOR = (160, 230, 230)
SKY_COLOR = (0, 0, 0)

PLAYER_FOV = np.math.pi / 2

PLAYER_SPEED = 32
PLAYER_TURN_SPEED = 2

COLUMN_WIDTH = PLAYER_FOV / WORKING_SIZE[0]

DISTANCE_TO_PROJECTION_PLANE = (WORKING_SIZE[0] / 2) / np.math.tan(PLAYER_FOV / 2)

INTENSITY = 1.0
INTENSITY_MULTIPLIER = 128 * INTENSITY