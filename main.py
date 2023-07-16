# Import packages
import pygame
from pygame.locals import *

import numpy as np

from constants import *
import camera

from texture_helper import *

from level import *

# Level
level = Level()

# Game active objects
player = camera.Camera(position=(8. * level.tile_size[0], 7. * level.tile_size[1]), angle=np.math.pi)

# Initialize pygame window
pygame.init()
window = pygame.display.set_mode(WINDOW_SIZE, flags=DOUBLEBUF | RESIZABLE, depth=16, vsync=True)
screen = pygame.Surface(WORKING_SIZE)

pygame.display.set_caption("Raycasting")

# Load textures
textures = load_textures()

# Make clock
clock = pygame.time.Clock()

# Mark mouse as not grabbed
mouse_grabbed = False

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

            # If TAB then toggle mouse cursor and "grab" window
            if event.key == pygame.K_TAB:
                pygame.mouse.set_visible(not(pygame.mouse.get_visible()))
                pygame.event.set_grab(not(pygame.event.get_grab()))
                pygame.mouse.set_pos(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2)
                mouse_grabbed = not(mouse_grabbed)

        if event.type == pygame.KEYUP:

            # If CTRL then un-crouch
            #if event.key == pygame.K_LCTRL:
            #    player.height *= 2

            pass


    # Update position based on inputs   
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.move_collide(1., dt, level)
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.move_collide(-1., dt, level)
    if keys[pygame.K_a]:
        player.strafe_collide(-1., dt, level)
    if keys[pygame.K_d]:
        player.strafe_collide(1., dt, level)
    if keys[pygame.K_LEFT]:
        player.turn(-1., dt)
    if keys[pygame.K_RIGHT]:
        player.turn(1., dt)
    if keys[pygame.K_LSHIFT]:
        player.height += 32 * dt
    if keys[pygame.K_LCTRL]:
        player.height -= 32 * dt
    if keys[pygame.K_KP_4]:
        player.turn(-1., dt)
    if keys[pygame.K_KP_6]:
        player.turn(1., dt)
    if keys[pygame.K_KP_8]:
        player.tilt(1., dt)
    if keys[pygame.K_KP_2]:
        player.tilt(-1., dt)
    
    # Update based on mouse movement
    mouse_xy = pygame.mouse.get_rel()
    if mouse_grabbed:
        player.turn(mouse_xy[0] / (2*WORKING_SIZE[0]), 1)
        player.tilt(-mouse_xy[1] / WORKING_SIZE[1], 1)

    # Clear the screen
    screen.fill(pygame.Color(0, 0, 0))

    # Draw sky and ground
    pygame.draw.rect(screen, SKY_COLOR, pygame.Rect((0, 0), (WORKING_SIZE[0], WORKING_SIZE[1]/2 )))
    pygame.draw.rect(screen, GROUND_COLOR, pygame.Rect((0, WORKING_SIZE[1]/2), (WORKING_SIZE[0], WORKING_SIZE[1]/2)))


    # Get raycast distances
    distances = player.do_raycast(level)

    # Compute floors and ceilings
    floors_and_ceilings_surface = player.do_floorcast_to_surface(level, textures)
    screen.blit(floors_and_ceilings_surface, (0, 0))

    # Create pygame surface for a line
    column = pygame.Surface((1, TEXTURE_SIZE[1]))

    # Print columns
    for col in range(WORKING_SIZE[0]):

        previous_height_offset = WORKING_SIZE[1]

        for d_col in reversed(range(0, len(distances[col]), 1)):

            # Extract data from dda
            distance, cell, face, offset, backside_distance, backside_offset = distances[col][d_col]

            # Compute height of wall, and space/offset at top based on player height
            height, height_offset = player.column_height_from_distance_with_modifier(level, distance, cell/10)
            height_offset += player.tilt_offset

            if height_offset >= previous_height_offset:
                continue

            height_b, height_offset_b = player.column_height_from_distance_with_modifier(level, backside_distance, cell/10)
            height_offset_b += player.tilt_offset

            # If front face is shorter than back face
            if height_offset > height_offset_b:

                # Draw a green line
                pygame.draw.line(screen, (50, 50, 50), (col, height_offset_b), (col, height_offset))

            # Compute modifiers
            shade_factor = 1.0 - 0.2 * (face % 2)

            intensify_factor = min(1.0, (INTENSITY_MULTIPLIER * INTENSITY_MULTIPLIER) / (distance * distance))
            final_factor = min(shade_factor * intensify_factor * 255, 255)

            # Apply texture to column
            column.blit(textures[cell], ((-1) * (offset % TEXTURE_SIZE[0]), 0))

            # Apply effects
            column.fill((final_factor, final_factor, final_factor), special_flags=BLEND_MULT)

            # Blit column
            screen.blit(pygame.transform.scale(column, (1, height)), (col,height_offset ))

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