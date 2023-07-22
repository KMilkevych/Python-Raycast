# Import packages
import pygame
from pygame.locals import *

import numpy as np

from texture_helper import load_textures, load_sprite_textures, TEXTURE_SIZE

from level import Level
from camera import Camera
from typing import Tuple, Callable

class Game:

    def __init__(
                self,
                window_size: Tuple[int, int] = (1280, 800),
                frame_size: Tuple[int, int] = (320, 400),
                framerate_limit: int = 60,
                level: Level = None,
                camera: Camera = None
            ):

        # Setup window-related members
        self.__window_size = window_size
        self.__frame_size = frame_size
        self.__framerate = framerate_limit
        self.__dt = 0

        # Initialize pygame window
        pygame.init()
        self.window = pygame.display.set_mode(self.__window_size, flags=DOUBLEBUF | RESIZABLE, depth=16, vsync=True)
        self.screen = pygame.Surface(self.__frame_size)

        # Set level and camera objects
        self.__level = level
        self.__camera = camera

        # Initialize without mouse and debug enabled
        self.__mouse_enabled = False
        self.__debug_enabled = False
        
        # Start game as running
        self.__running = True

        # Initialize empty keymaps
        self.__on_key_down = {}
        self.__on_key_up = {}
        self.__while_key_pressed = {}
        self.__on_mouse_move = []

        # Custom objects / variables dictionary
        self.custom_variables = {}

        # Instantiate font for text writing
        pygame.font.init()
        self.main_font = pygame.font.SysFont("Dejavu Sans", 16)

        # Load textures
        self.textures = load_textures()
        self.sprite_textures = load_sprite_textures()

    def set_level(self, level: Level):
        self.__level = level

    def get_level(self) -> Level:
        return self.__level
    
    def set_camera(self, camera: Camera):
        self.__camera = camera
    
    def get_camera(self) -> Camera:
        return self.__camera

    def bind_key_down(self, key: int, action: Callable):
        self.__on_key_down[key] = action

    def bind_key_up(self, key: int, action: Callable):
        self.__on_key_up[key] = action
    
    def bind_key_pressed(self, key: int, action: Callable):
        self.__while_key_pressed[key] = action
    
    def bind_mouse_move(self, action: Callable):
        self.__on_mouse_move.append(action)
    
    def get_mouse_enabled(self) -> bool:
        return self.__mouse_enabled
    
    def set_mouse_enabled(self, mouse_enabled: bool):
        self.__mouse_enabled = mouse_enabled

        pygame.mouse.set_visible(not(self.__mouse_enabled))
        pygame.event.set_grab(self.__mouse_enabled)
        pygame.mouse.set_pos(self.__window_size[0]/2, self.__window_size[1]/2)
        
    def get_debug_enabled(self) -> bool:
        return self.__debug_enabled
    
    def set_debug_enabled(self, debug_enabled: bool):
        self.__debug_enabled = debug_enabled
    
    def get_dt(self) -> int:
        return self.__dt

    def get_frame_size(self) -> Tuple[int, int]:
        return self.__frame_size
        
    def quit(self):
        self.__running = False

    def get_custom_variable(self, key):
        return self.custom_variables[key]
    
    def set_custom_variable(self, key, value):
        self.custom_variables[key] = value
    
    def get_custom_variables(self) -> dict:
        return self.custom_variables

    def set_custom_variables(self, custom_variables: dict):
        self.custom_variables = custom_variables

    def run(self):

        # Make clock
        clock = pygame.time.Clock()

        # Start game loop
        while (self.__running):

            # Fetch events
            for event in pygame.event.get():

                # Check if user has quit
                if event.type == pygame.QUIT:
                    self.__running = False

                # If its a resize event
                if event.type == pygame.VIDEORESIZE:
                    self.__window_size = event.dict['size']

                # Keypress events
                if event.type == pygame.KEYDOWN:

                    # If the key is bound, then execute it
                    if event.key in self.__on_key_down.keys():
                        self.__on_key_down[event.key]()
                
                if event.type == pygame.KEYUP:

                    # If the key is bound, then execute it
                    if event.key in self.__on_key_up.keys():
                        self.__on_key_up[event.key]()

            # Update position based on inputs   
            keys = pygame.key.get_pressed()

            # Iterate over each bound key
            for key in self.__while_key_pressed.keys():
                
                # If its pressed, do the action
                if keys[key]:
                    self.__while_key_pressed[key]()

            
            # Update based on mouse movement
            mouse_xy = pygame.mouse.get_rel()
            if self.__mouse_enabled:
                for mouse_action in self.__on_mouse_move:
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
            # TODO: Make debug info
            if self.__debug_enabled:
                pass

            # Paste self.screen frame
            frame = pygame.transform.scale(self.screen, self.__window_size)
            self.window.blit(frame, frame.get_rect())

            # Update display
            pygame.display.flip()

            # Limit fps
            self.__dt = clock.tick(self.__framerate) / 1000
            pygame.display.set_caption("Raycasting " + str(np.round(1. / self.__dt, 1)))

        # Quit application
        pygame.quit()


    def __draw_sky_and_ground(self):
        middle = max(0, int(self.__frame_size[1]/2 + self.__camera.tilt_offset))
        pygame.draw.rect(self.screen, self.__level.sky_color, pygame.Rect((0, 0), (self.__frame_size[0], middle)))
        pygame.draw.rect(self.screen, self.__level.ground_color, pygame.Rect((0, middle), (self.__frame_size[0], self.__frame_size[1] - middle)))


    def __draw_floors_and_ceilings(self):

        # Compute floorcast surface
        floors_and_ceilings_surface = self.__camera.do_floorcast_to_surface(self.__level, self.textures)
        floors_and_ceilings_surface.set_colorkey((0, 0, 0))

        # Draw floorcast surface to screen
        self.screen.blit(floors_and_ceilings_surface, (0, 0))
    
    def __compute_raycast_data(self):
        return self.__camera.do_raycast(self.__level)

    def __draw_walls(self, raycast_data):

        # Create pygame surface for a line
        column = pygame.Surface((1, TEXTURE_SIZE[1]))

        # Draw columns to screen
        for col in range(self.__frame_size[0]):

            # Extract data from dda
            distance, (mapX, mapY), face, offset = raycast_data[col]

            # Extract wall data from walls
            wall_tag, texture_id, wall_height = self.__level.walls[mapY][mapX]

            # Compute height of wall, and space/offset at top based on self.camera height
            height, height_offset = self.__camera.height_and_offset_from_distance(wall_height, distance)

            # Compute modifiers
            shade_factor = 1.0 - 0.2 * (face % 2)

            intensify_factor = min(1.0, (self.__camera.INTENSITY_MULTIPLIER * self.__camera.INTENSITY_MULTIPLIER) / (distance * distance))
            final_factor = min(shade_factor * intensify_factor * 255, 255)

            # Apply texture to column
            column.blit(self.textures[texture_id], ((-1) * (offset), 0))

            # Apply effects
            column.fill((final_factor, final_factor, final_factor), special_flags=BLEND_MULT)

            # Blit column
            self.screen.blit(pygame.transform.scale(column, (1, height)), (col, height_offset + self.__camera.tilt_offset))

    def __compute_sprite_data(self):
        return self.__camera.compute_sprite_data(self.__level)

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
            final_factor = min(1.0, (self.__camera.INTENSITY_MULTIPLIER * self.__camera.INTENSITY_MULTIPLIER) / (sprite_distance * sprite_distance)) * 255

            # Compute surface to draw from
            sprite = pygame.transform.scale(self.sprite_textures[texture_id], sprite_size)
            
            # Create column surface
            column = pygame.Surface((1, sprite_size[1]))
            column.set_colorkey((0,0,0))


            # Iterate and blit each column of the sprite
            for col in range(draw_start[0], draw_end[0]):
                if col > 0 and col < self.__frame_size[0] and sprite_distance < raycast_data[col][0]:
                    
                    # Blit to column
                    column.blit(sprite, (-(col - draw_start[0]), 0))

                    # Apply effects
                    column.fill((final_factor, final_factor, final_factor), special_flags=BLEND_MULT)

                    # Blit to self.screen
                    self.screen.blit(column, (col, draw_start[1]))