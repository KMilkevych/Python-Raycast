# Import packages
import pygame
from pygame.locals import *

import numpy as np

from constants import *
import camera

# Game active objects
player = camera.Camera(position=(8. * TILE_SIZE[0], 7. * TILE_SIZE[1]), angle=np.math.pi)

# Initialize pygame window
pygame.init()
window = pygame.display.set_mode(WINDOW_SIZE, DOUBLEBUF, 16)
screen = pygame.Surface(WORKING_SIZE)

pygame.display.set_caption("Raycasting")

# Load textures
TEXTURES = {
    "A": pygame.image.load("textures/brick_texture_01.png").convert(),
    "B": pygame.image.load("textures/brick_texture_01.png").convert(),
    "C": pygame.image.load("textures/brick_texture_01.png").convert()
}

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

    # Update position based on inputs
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player.move(1., dt)
        print(player.position / TILE_SIZE[0])
    if keys[pygame.K_DOWN]:
        player.move(-1., dt)
        print(player.position / TILE_SIZE[0])
    if keys[pygame.K_LEFT]:
        player.turn(-1., dt)
    if keys[pygame.K_RIGHT]:
        player.turn(1., dt)
    
    # Print everything
    #print("Position: ", player.position)
    #print("Direction: ", player.direction)


    # Clear the screen
    screen.fill(pygame.Color(0, 0, 0))

    # Rendering code goes here
    # ...

    # Draw sky and ground
    pygame.draw.rect(screen, SKY_COLOR, pygame.Rect((0, 0), (WORKING_SIZE[0], WORKING_SIZE[1]/2)))
    pygame.draw.rect(screen, GROUND_COLOR, pygame.Rect((0, WORKING_SIZE[1]/2), (WORKING_SIZE[0], WORKING_SIZE[1]/2)))

    
    # Get raycast distances
    distances = player.do_raycast(LEVEL)

    # Create pygame surface for a line
    column = pygame.Surface((1, TILE_SIZE[1]))
    
    # Print lines
    for col in range(WORKING_SIZE[0]):

        distance, cell, face, offset = distances[col]

        height = max(0, (WORKING_SIZE[1] / distance) * (DISTANCE_TO_PROJECTION_PLANE / TILE_SIZE[0]) * 2.0)
        space = (WORKING_SIZE[1] - height) / 2

        if cell == "#":
            base_color = COLORS[cell]

            if (offset == 0) or (offset == TILE_SIZE[0] - 1):
                base_color = (0., 0., 0.)

            shade_factor = 0.25 if face == 0 else (0.50 if face == 2 else 0.0)
            shaded_color = (base_color[0] * (1.0 - shade_factor), base_color[1] * (1.0 - shade_factor), base_color[2] * (1.0 - shade_factor))

            intensity = 1.0
            intensity_multiplier = 64.0
            detensify_scale = min(1.0, (intensity / distance) * intensity_multiplier)

            detensified_color = (base_color[0] * detensify_scale, base_color[1] * detensify_scale, base_color[2] * detensify_scale)

            # Fill column
            column.fill(detensified_color)
        elif cell in ("A", "B", "C"):

            # Get column from texture
            texture_column = TEXTURES[cell].copy().subsurface((offset, 0), (1, TILE_SIZE[1]))

            # Compute modifiers
            shade_factor = 0.25 if face == 0 else (0.50 if face == 2 else 0.0)
            shade_factor = 1.0 - shade_factor

            intensity = 1.0
            intensity_multiplier = 64.0
            detensify_scale = min(1.0, (intensity / distance) * intensity_multiplier)

            # Apply texture to column
            column.blit(texture_column, (0, 0))

            # Apply effects
            column.fill((255 * shade_factor, 255 * shade_factor, 255 * shade_factor), special_flags=BLEND_MULT)
            column.fill((255 * detensify_scale, 255 * detensify_scale, 255 *detensify_scale), special_flags=BLEND_MULT)
            


        # Blit column
        screen.blit(pygame.transform.scale(column, (1, height)), (col, space))

        #pygame.draw.line(screen, detensified_color, (col, space), (col, WORKING_SIZE[1] - space))
    

    # Debugging draw
    scale = 4.0
    for y in range(len(LEVEL)):
        for x in range(len(LEVEL[y])):
            pygame.draw.rect(screen, COLORS[LEVEL[y][x]], pygame.Rect((x * scale, y * scale), (scale, scale)))

    pygame.draw.circle(screen, "black", player.position*scale/ TILE_SIZE[0], 4, 1)
    pygame.draw.line(screen, "green", player.position*scale / TILE_SIZE[0], player.position*scale/ TILE_SIZE[0] + player.direction * DISTANCE_TO_PROJECTION_PLANE * scale / (TILE_SIZE[0]**2), 1)


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