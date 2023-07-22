# Import packages
import pygame
from pygame.locals import *

import numpy as np

from constants import *
import camera

from texture_helper import *

from level import *

# Font for writing text
pygame.font.init()
main_font = pygame.font.SysFont("Dejavu Sans", 16)

# Level
level = Level()

# Game active objects
player = camera.Camera(position=(level.player_start[0] * level.tile_size[0], level.player_start[1] * level.tile_size[1]), angle=level.player_start[2])

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

# Mark debug info as not shown
show_debug = False

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
            
            # If X toggle debug info
            if event.key == pygame.K_x:
                show_debug = not(show_debug)

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
    if keys[pygame.K_LEFT] or keys[pygame.K_KP_4]:
        player.turn(-1., dt)
    if keys[pygame.K_RIGHT] or keys[pygame.K_KP_6]:
        player.turn(1., dt)
    if keys[pygame.K_LSHIFT]:
        player.height += 32 * dt
    if keys[pygame.K_LCTRL]:
        player.height -= 32 * dt
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
    middle = max(0, int(WORKING_SIZE[1]/2 + player.tilt_offset))
    pygame.draw.rect(screen, SKY_COLOR, pygame.Rect((0, 0), (WORKING_SIZE[0], middle)))
    pygame.draw.rect(screen, GROUND_COLOR, pygame.Rect((0, middle), (WORKING_SIZE[0], WORKING_SIZE[1] - middle)))

    # Compute floors and ceilings
    floors_and_ceilings_surface = player.do_floorcast_to_surface(level, textures)
    floors_and_ceilings_surface.set_colorkey((0, 0, 0))
    screen.blit(floors_and_ceilings_surface, (0, 0))

    # Get raycast distances
    distances = player.do_raycast(level)

    # Create pygame surface for a line
    column = pygame.Surface((1, TEXTURE_SIZE[1]))

    # Print columns
    for col in range(WORKING_SIZE[0]):

        # Extract data from dda
        distance, (mapX, mapY), face, offset = distances[col]

        # Extract wall data from walls
        wall_tag, texture_id, wall_height = level.walls[mapY][mapX]

        # Compute height of wall, and space/offset at top based on player height
        height, height_offset = player.height_and_offset_from_distance(wall_height, distance)

        # Compute modifiers
        shade_factor = 1.0 - 0.2 * (face % 2)

        intensify_factor = min(1.0, (INTENSITY_MULTIPLIER * INTENSITY_MULTIPLIER) / (distance * distance))
        final_factor = min(shade_factor * intensify_factor * 255, 255)

        # Apply texture to column
        column.blit(textures[texture_id], ((-1) * (offset), 0))

        # Apply effects
        column.fill((final_factor, final_factor, final_factor), special_flags=BLEND_MULT)

        # Blit column
        screen.blit(pygame.transform.scale(column, (1, height)), (col, height_offset + player.tilt_offset))

    # Compute sprites
    sprite_data = player.compute_sprite_data(level)

    # Iterate over each sprite in sprite_data
    for s in range(sprite_data.shape[0]):

        # Extract data
        texture_id, sprite_distance, sprite_size_x, sprite_size_y, draw_start_x, draw_start_y = sprite_data[s, :]

        texture_id = int(texture_id)
        sprite_size = ((sprite_size_x), (sprite_size_y))
        draw_start = (int(draw_start_x), int(draw_start_y))
        draw_end = (int(draw_start_x + sprite_size_x), int(draw_start_y + sprite_size_y))

        # Compute intensity
        final_factor = min(1.0, (INTENSITY_MULTIPLIER * INTENSITY_MULTIPLIER) / (sprite_distance * sprite_distance)) * 255

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

                # Apply effects
                column.fill((final_factor, final_factor, final_factor), special_flags=BLEND_MULT)

                # Blit to screen
                screen.blit(column, (col, draw_start[1]))

    
    # Draw debug information to screen
    if show_debug:
        debug_text = "pos: {0}\ndir: {1}\nang: {2}".format(np.around(np.hstack([player.position, player.height]), 2), np.around(player.direction, 2), np.around(player.angle, 2))
        debug_info = [main_font.render(line, False, (255, 255, 255)) for line in debug_text.split("\n")]
        heightsum = 0
        for info in debug_info:
            screen.blit(info, (2, heightsum))
            heightsum += info.get_height()

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