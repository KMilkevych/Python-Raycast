# Import packages
import pygame
from pygame.locals import *

import numpy as np

from core.texture_helper import load_textures, load_sprite_textures, TEXTURE_SIZE

from core.level import Level
from core.camera import Camera
from core.drawable import Drawable
from typing import Tuple, Callable, List

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

        # Set update function
        self.__update = None

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

        # Drawables
        self.drawables = []

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

    def get_drawables(self) -> List[Drawable]:
        return self.drawables

    def set_drawables(self, drawables: List[Drawable]):
        self.drawables = drawables
    
    def add_drawable(self, drawable: Drawable):
        self.drawables.append(drawable)
    
    def remove_drawable(self, drawable: Drawable):
        self.drawables.remove(drawable)

    def __get_drawables_ndarray(self) -> np.ndarray:
        
        # Map to list of ndarrays
        ndarray_list = list(map(lambda d: d.get_ndarray(), self.drawables))

        # Return numpy ndarray
        return np.array(ndarray_list).reshape(len(self.drawables), 5)

    def set_update(self, update: Callable[['Game', float], None]):
        self.__update = update

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

            # Now call the update function
            self.__update(self, self.__dt)

            # Clear the screen
            self.screen.fill(pygame.Color(0, 0, 0))

            # Draw sky and ground
            sky_and_ground_surface = self.__camera.do_skycast_to_surface(self.__level.sky_color, self.__level.ground_color)
            self.screen.blit(sky_and_ground_surface, (0, 0))

            # Draw floors and ceilings
            floors_and_ceilings_surface = self.__camera.do_floorcast_to_surface(self.__level, self.textures)
            floors_and_ceilings_surface.set_colorkey((0, 0, 0))
            self.screen.blit(floors_and_ceilings_surface, (0, 0))

            # Compute raycast data
            raycast_data = self.__camera.do_raycast(self.__level)

            # Draw walls
            walls_surface = self.__camera.do_wallcast_to_surface(self.__level, raycast_data, self.textures)
            walls_surface.set_colorkey((0, 0, 0))
            self.screen.blit(walls_surface, (0, 0))

            # Compute sprite data
            drawable_sprites = np.vstack([self.__level.get_static_drawables(), self.__get_drawables_ndarray()])
            sprite_data = self.__camera.compute_sprite_data(self.__level, drawable_sprites)

            # Draw sprites
            sprite_surface = self.__camera.do_spritecast_to_surface(sprite_data, raycast_data, self.sprite_textures)
            sprite_surface.set_colorkey((0, 0, 0))
            self.screen.blit(sprite_surface, (0, 0))

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