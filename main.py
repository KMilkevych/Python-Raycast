# Import packages
import pygame
from pygame.locals import *

import numpy as np

# Program constants
WINDOW_SIZE = (1280, 800)
WORKING_SIZE = (320, 200)

TILE_SIZE = (64, 64)

LEVEL = [
    ["#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#"],
    ["#"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","#"],
    ["#"," ","#","#","#"," "," "," "," "," "," "," "," "," "," ","#"],
    ["#"," ","#"," ","#"," "," "," "," "," "," "," "," "," "," ","#"],
    ["#"," ","#","#","#"," "," "," "," "," "," "," "," "," "," ","#"],
    ["#"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","#"],
    ["#"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","#"],
    ["#"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","#"],
    ["#"," "," "," "," "," "," "," "," "," "," ","#","#"," ","#","#"],
    ["#"," ","#","#","#","#","#"," "," "," "," ","#","#"," ","#","#"],
    ["#"," "," "," "," "," "," "," "," "," "," ","#","#"," "," ","#"],
    ["#"," "," "," "," "," "," "," "," "," "," ","#","#","#","#","#"],
    ["#"," "," "," "," "," "," "," "," "," "," "," ","#","#","#","#"],
    ["#"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","#"],
    ["#"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","#"],
    ["#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#"],
]

PLAYER_HEIGHT = 32
# PLAYER_FOV = 60
PLAYER_FOV = np.math.pi / 3.

COLUMN_WIDTH = WORKING_SIZE[0] / PLAYER_FOV

DISTANCE_TO_PROJECTION_PLANE = (WORKING_SIZE[0] / 2.) / np.math.tan(PLAYER_FOV / 2)

# Game active objects
player_pos = np.array([5., 8.]).reshape((-1, 1))
player_dir = np.math.pi

# Initialize pygame window
pygame.init()
window = pygame.display.set_mode(WINDOW_SIZE, DOUBLEBUF, 16)
screen = pygame.Surface(WORKING_SIZE)

pygame.display.set_caption("Raycasting")

# Make clock
clock = pygame.time.Clock()

# Start game loop
running = True
while (running):

    # Fetch events
    for event in pygame.event.get():

        # Check if user has quit
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(pygame.Color(255, 255, 255))

    # Rendering code goes here
    # ...
    pygame.draw.circle(screen, pygame.Color(0, 0, 0), (170, 100), 20, 4)

    # Paste screen frame
    frame = pygame.transform.scale(screen, WINDOW_SIZE)
    window.blit(frame, frame.get_rect())

    # Update display
    pygame.display.flip()

    # Limit fps
    clock.tick(60)

# Quit application
pygame.quit()