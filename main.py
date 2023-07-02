# Import packages
import pygame
from pygame.locals import *

import numpy as np

from constants import *
import camera

from texture_helper import *

# Game active objects
player = camera.Camera(position=(8. * TILE_SIZE[0], 7. * TILE_SIZE[1]), angle=np.math.pi)

# Initialize pygame window
pygame.init()
window = pygame.display.set_mode(WINDOW_SIZE, flags=DOUBLEBUF | RESIZABLE, depth=16, vsync=True)
screen = pygame.Surface(WORKING_SIZE)

pygame.display.set_caption("Raycasting")

# Load textures
textures = load_textures()

# Make clock
clock = pygame.time.Clock()

# Start game loop
running = True
dt = 0
while (running):

    # Fetch events
    for event in pygame.event.get():

        # Check if user has quit
        if event.type == pygame.QUIT:
            running = False

        # If its a resize event
        if event.type == pygame.VIDEORESIZE:
            WINDOW_SIZE = event.dict['size']

        # Keypress events
        if event.type == pygame.KEYDOWN:

            # If ESCAPE then quit
            if event.key == pygame.K_ESCAPE:
                running = False

            # If CTRL the crouch
            if event.key == pygame.K_LCTRL:
                PLAYER_HEIGHT /= 2

        if event.type == pygame.KEYUP:

            # If CTRL then un-crouch
            if event.key == pygame.K_LCTRL:
                PLAYER_HEIGHT *= 2


    # Update position based on inputs   
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player.move(1., dt)
        #print(player.position / TILE_SIZE[0])
    if keys[pygame.K_DOWN]:
        player.move(-1., dt)
        #print(player.position / TILE_SIZE[0])
    if keys[pygame.K_LEFT]:
        player.turn(-1., dt)
    if keys[pygame.K_RIGHT]:
        player.turn(1., dt)

    # Clear the screen
    screen.fill(pygame.Color(0, 0, 0))

    # Draw sky and ground
    pygame.draw.rect(screen, SKY_COLOR, pygame.Rect((0, 0), (WORKING_SIZE[0], WORKING_SIZE[1]/2 )))
    pygame.draw.rect(screen, GROUND_COLOR, pygame.Rect((0, WORKING_SIZE[1]/2), (WORKING_SIZE[0], WORKING_SIZE[1]/2)))

    
    # Get raycast distances
    distances = player.do_raycast(WALLS)

    # Create pygame surface for a line
    column = pygame.Surface((1, TILE_SIZE[1]))
    
    # Print lines
    for col in range(WORKING_SIZE[0]):

        # Extract data from dda
        distance, cell, face, offset = distances[col]

        # Compute height of wall, and space/offset at top based on player height
        height = (TILE_SIZE[2] / distance) * DISTANCE_TO_PROJECTION_PLANE
        height_offset = (PLAYER_HEIGHT / distance) * DISTANCE_TO_PROJECTION_PLANE

        # Get column from texture
        texture_column = textures[cell].subsurface((offset % TEXTURE_SIZE[0], 0), (1, TEXTURE_SIZE[1]))

        # Compute modifiers
        shade_factor = 1.0 - 0.2 * (face % 2)

        intensity = 1.0
        intensity_multiplier = 128

        intensify_factor = min(1.0, (intensity / distance) * intensity_multiplier)

        final_factor = shade_factor * intensify_factor * 255

        # Apply texture to column
        column.blit(texture_column, (0, 0))

        # Apply effects
        column.fill((final_factor, final_factor, final_factor), special_flags=BLEND_MULT)

        # Blit column
        screen.blit(pygame.transform.scale(column, (1, height)), (col, WORKING_SIZE[1]/2 - height + height_offset))

    '''
    # Debugging draw
    scale = 4.0
    for y in range(len(WALLS)):
        for x in range(len(WALLS[y])):
            pygame.draw.rect(screen, COLORS[WALLS[y][x]], pygame.Rect((x * scale, y * scale), (scale, scale)))

    pygame.draw.circle(screen, "black", player.position*scale/ TILE_SIZE[0], 4, 1)
    pygame.draw.line(screen, "green", player.position*scale / TILE_SIZE[0], player.position*scale/ TILE_SIZE[0] + player.direction * DISTANCE_TO_PROJECTION_PLANE * scale / (TILE_SIZE[0]**2), 1)
    '''

    # Paste screen frame
    frame = pygame.transform.scale(screen, WINDOW_SIZE)
    window.blit(frame, frame.get_rect())

    # Update display
    pygame.display.flip()

    # Limit fps
    dt = clock.tick(60) / 1000
    pygame.display.set_caption("Raycasting " + str(np.round(1. / dt, 1)))

# Quit application
pygame.quit()