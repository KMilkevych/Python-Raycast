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
sprite_textures = load_sprite_textures()

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

    # Compute sprites
    sprite_data = player.compute_sprite_data(level)

    # Create pygame surface for a line
    column = pygame.Surface((1, TEXTURE_SIZE[1]))

    # Print columns
    for col in range(WORKING_SIZE[0]):

        # Extract data from dda
        distance, cell, face, offset = distances[col]

        # Compute height of wall, and space/offset at top based on player height
        height, height_offset = player.column_height_from_distance(level, distance)

        # Compute modifiers
        shade_factor = 1.0 - 0.2 * (face % 2)

        intensify_factor = min(1.0, (INTENSITY_MULTIPLIER * INTENSITY_MULTIPLIER) / (distance * distance))
        final_factor = min(shade_factor * intensify_factor * 255, 255)

        # Apply texture to column
        column.blit(textures[cell], ((-1) * (offset % TEXTURE_SIZE[0]), 0))

        # Apply effects
        column.fill((final_factor, final_factor, final_factor), special_flags=BLEND_MULT)

        # Blit column
        screen.blit(pygame.transform.scale(column, (1, height)), (col, height_offset + player.tilt_offset))


    #print(sprite_data.shape)
    #print(sprite_data)

    # Iterate over each sprite in sprite_data
    for s in range(sprite_data.shape[0]):

        #print(sprite_data[s, :].shape)
        #print(sprite_data[s, :])

        # Extract data
        texture_id, sprite_distance, sprite_size_x, sprite_size_y, draw_start_x, draw_start_y, draw_end_x, draw_end_y, y_depth = sprite_data[s, :]

        texture_id = int(texture_id)
        sprite_size = ((sprite_size_x), (sprite_size_y))
        draw_start = (int(draw_start_x), int(draw_start_y))
        draw_end = (int(draw_end_x), int(draw_end_y))

        # Compute surface to draw from
        sprite = pygame.transform.scale(sprite_textures[texture_id], sprite_size)
        
        # Create column surface
        column = pygame.Surface((1, sprite_size[1]))
        column.set_colorkey((0,0,0))


        # Iterate and blit each column of the sprite
        for col in range(draw_start[0], draw_end[0]):
            if col > 0 and col < WORKING_SIZE[0] and sprite_distance < distances[col][0]:
                # Blit to column
                column.blit(sprite, (-(col - draw_start[0]), 0))

                # Blit to screen
                screen.blit(column, (col, draw_start[1]))

    '''
    # Iterate over each sprite and draw as needed
    for sprite_datum in sprite_data:
        
        # Extract data
        texture_id, sprite_distance, sprite_size, draw_start, draw_end = sprite_datum

        # Compute surface to draw from
        sprite = pygame.transform.scale(sprite_textures[texture_id], sprite_size)
        
        # Create column surface
        column = pygame.Surface((1, sprite_size[1]))
        column.set_colorkey((0,0,0))


        # Iterate and blit each column of the sprite
        for col in range(draw_start[0], draw_end[0]):
            if col > 0 and col < WORKING_SIZE[0] and sprite_distance < distances[col][0]:
                # Blit to column
                column.blit(sprite, (-(col - draw_start[0]), 0))

                # Blit to screen
                screen.blit(column, (col, draw_start[1]))

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