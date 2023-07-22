# Import packages
import pygame
from pygame.locals import *

import numpy as np

from constants import *
import camera

from texture_helper import *

from level import *

class Game:

    def __init__(self, window_size = (1280, 800), frame_size = (320, 400), framerate_limit = 60, level=None, camera=None):

        self.WINDOW_SIZE = window_size
        self.WORKING_SIZE = frame_size
        self.FRAMERATE = framerate_limit
        self.dt = 0

        self.level = level
        self.camera = camera

        self.mouse_grab = False
        self.debug = False

        self.running = True

        self.on_key_down = {}
        self.on_key_up = {}
        self.while_key_pressed = {}
        self.on_mouse_move = []

    def set_level(self, level):
        self.level = level

    def get_level(self):
        return self.level
    
    def set_camera(self, camera):
        self.camera = camera
    
    def get_camera(self):
        return self.camera

    def bind_key_down(self, key, action):
        self.on_key_down[key] = action

    def bind_key_up(self, key, action):
        self.on_key_up[key] = action
    
    def bind_key_pressed(self, key, action):
        self.while_key_pressed[key] = action
    
    def bind_mouse_move(self, action):
        self.on_mouse_move.append(action)
    
    def get_mouse(self):
        return self.mouse_grab
    
    def set_mouse(self, mouse_grab):
        self.mouse_grab = mouse_grab

        pygame.mouse.set_visible(not(self.mouse_grab))
        pygame.event.set_grab(self.mouse_grab)
        pygame.mouse.set_pos(self.WINDOW_SIZE[0]/2, self.WINDOW_SIZE[1]/2)
        
    def get_debug(self):
        return self.debug
    
    def set_debug(self, debug):
        self.debug = debug
    
    def get_dt(self):
        return self.dt

    def quit(self):
        self.running = False

    def setup(self):

        # Instantiate font
        pygame.font.init()
        self.main_font = pygame.font.SysFont("Dejavu Sans", 16)

        # Initialize pygame window
        pygame.init()
        self.window = pygame.display.set_mode(self.WINDOW_SIZE, flags=DOUBLEBUF | RESIZABLE, depth=16, vsync=True)
        self.screen = pygame.Surface(self.WORKING_SIZE)

        # Load textures
        self.textures = load_textures()
        self.sprite_textures = load_sprite_textures()


    def run(self):

        # Make clock
        clock = pygame.time.Clock()

        # Start game loop
        while (self.running):

            # Fetch events
            for event in pygame.event.get():

                # Check if user has quit
                if event.type == pygame.QUIT:
                    self.running = False

                # If its a resize event
                if event.type == pygame.VIDEORESIZE:
                    self.WINDOW_SIZE = event.dict['size']

                # Keypress events
                if event.type == pygame.KEYDOWN:

                    # If the key is bound, then execute it
                    if event.key in self.on_key_down.keys():
                        self.on_key_down[event.key]()
                
                if event.type == pygame.KEYUP:

                    # If the key is bound, then execute it
                    if event.key in self.on_key_up.keys():
                        self.on_key_up[event.key]()

            # Update position based on inputs   
            keys = pygame.key.get_pressed()

            # Iterate over each bound key
            for key in self.while_key_pressed.keys():
                
                # If its pressed, do the action
                if keys[key]:
                    self.while_key_pressed[key]()

            
            # Update based on mouse movement
            mouse_xy = pygame.mouse.get_rel()
            if self.mouse_grab:
                for mouse_action in self.on_mouse_move:
                    mouse_action(mouse_xy[0], mouse_xy[1])

            # Clear the screen
            self.screen.fill(pygame.Color(0, 0, 0))

            # Draw sky and ground
            self.__draw_sky_and_ground()

            # Draw floors and ceilings
            self.__draw_floors_and_ceilings()

            # Draw walls
            raycast_data = self.__compute_raycast_data()
            self.__draw_walls(raycast_data)

            # Draw sprites
            sprite_data = self.__compute_sprite_data()
            self.__draw_sprites(sprite_data, raycast_data)

            # Draw debug info
            if self.debug:
                pass
                #self.__draw_debug()

            # Paste self.screen frame
            frame = pygame.transform.scale(self.screen, self.WINDOW_SIZE)
            self.window.blit(frame, frame.get_rect())

            # Update display
            pygame.display.flip()

            # Limit fps
            self.dt = clock.tick(self.FRAMERATE) / 1000
            pygame.display.set_caption("Raycasting " + str(np.round(1. / self.dt, 1)))

        # Quit application
        pygame.quit()


    def __draw_sky_and_ground(self):
        middle = max(0, int(self.WORKING_SIZE[1]/2 + self.camera.tilt_offset))
        pygame.draw.rect(self.screen, SKY_COLOR, pygame.Rect((0, 0), (self.WORKING_SIZE[0], middle)))
        pygame.draw.rect(self.screen, GROUND_COLOR, pygame.Rect((0, middle), (self.WORKING_SIZE[0], self.WORKING_SIZE[1] - middle)))


    def __draw_floors_and_ceilings(self):

        # Compute floorcast surface
        floors_and_ceilings_surface = self.camera.do_floorcast_to_surface(self.level, self.textures)
        floors_and_ceilings_surface.set_colorkey((0, 0, 0))

        # Draw floorcast surface to screen
        self.screen.blit(floors_and_ceilings_surface, (0, 0))
    
    def __compute_raycast_data(self):
        return self.camera.do_raycast(self.level)

    def __draw_walls(self, raycast_data):

        # Create pygame surface for a line
        column = pygame.Surface((1, TEXTURE_SIZE[1]))

        # Draw columns to screen
        for col in range(self.WORKING_SIZE[0]):

            # Extract data from dda
            distance, (mapX, mapY), face, offset = raycast_data[col]

            # Extract wall data from walls
            wall_tag, texture_id, wall_height = self.level.walls[mapY][mapX]

            # Compute height of wall, and space/offset at top based on self.camera height
            height, height_offset = self.camera.height_and_offset_from_distance(wall_height, distance)

            # Compute modifiers
            shade_factor = 1.0 - 0.2 * (face % 2)

            intensify_factor = min(1.0, (INTENSITY_MULTIPLIER * INTENSITY_MULTIPLIER) / (distance * distance))
            final_factor = min(shade_factor * intensify_factor * 255, 255)

            # Apply texture to column
            column.blit(self.textures[texture_id], ((-1) * (offset), 0))

            # Apply effects
            column.fill((final_factor, final_factor, final_factor), special_flags=BLEND_MULT)

            # Blit column
            self.screen.blit(pygame.transform.scale(column, (1, height)), (col, height_offset + self.camera.tilt_offset))

    def __compute_sprite_data(self):
        return self.camera.compute_sprite_data(self.level)

    def __draw_sprites(self, sprite_data, raycast_data):

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
            sprite = pygame.transform.scale(self.sprite_textures[texture_id], sprite_size)
            
            # Create column surface
            column = pygame.Surface((1, sprite_size[1]))
            column.set_colorkey((0,0,0))


            # Iterate and blit each column of the sprite
            for col in range(draw_start[0], draw_end[0]):
                if col > 0 and col < WORKING_SIZE[0] and sprite_distance < raycast_data[col][0]:
                    
                    # Blit to column
                    column.blit(sprite, (-(col - draw_start[0]), 0))

                    # Apply effects
                    column.fill((final_factor, final_factor, final_factor), special_flags=BLEND_MULT)

                    # Blit to self.screen
                    self.screen.blit(column, (col, draw_start[1]))