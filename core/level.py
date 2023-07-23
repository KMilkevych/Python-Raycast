import numpy as np
from typing import Tuple

from core.staticobject import StaticObject

class Level:

    def __init__(
            self,
            tile_size: np.ndarray = np.array([32, 32, 64]),
            ceiling_height: int = 64,
            player_start: np.ndarray = np.array([0., 0.]),
            player_start_angle: float = 0,
            sky_color: Tuple[int, int, int] = (160, 230, 230),
            ground_color: Tuple[int, int, int] = (60, 20, 0)
            ):

        self.tile_size = tile_size
        self.ceiling_height = ceiling_height

        self.player_start = player_start
        self.player_start_angle = player_start_angle
        
        self.ground_color = ground_color
        self.sky_color = sky_color

        # Static objects registered
        self.static_objects = []    # regular list
        self.__static_objects = np.array([])  # numpy array
    
    def get_tile_size(self):
        return self.tile_size

    def set_tile_size(self, tile_size):
        self.tile_size = tile_size
    
    def get_ceiling_height(self):
        return self.ceiling_height
    
    def set_ceiling_height(self, ceiling_height):
        self.ceiling_height = ceiling_height
    
    def get_player_start(self):
        return self.player_start
    
    def set_player_start(self, player_start):
        self.player_start = player_start
    
    def get_player_start_angle(self):
        return self.player_start_angle
    
    def set_player_start_angle(self, player_start_angle):
        self.player_start_angle = player_start_angle
    
    def get_sky_color(self):
        return self.sky_color

    def set_sky_color(self, sky_color):
        self.sky_color = sky_color

    def get_ground_color(self):
        return self.ground_color

    def set_ground_color(self, ground_color):
        self.ground_color = ground_color

    def get_walls(self):
        return self.walls
    
    def set_walls(self, walls):
        self.walls = walls
    
    def get_floors(self):
        return self.floors
    
    def set_floors(self, floors):
        self.floors = floors
    
    def get_ceilings(self):
        return self.ceilings
    
    def set_ceilings(self, ceilings):
        self.ceilings = ceilings
    
    def get_static_objects(self) -> np.ndarray:
        return self.__static_objects
    
    def set_static_objects(self, static_objects: np.ndarray):
        self.__static_objects = static_objects
        
    def add_static_object(self, staticobject: StaticObject):
        self.static_objects.append(staticobject)
        self.__recompute_static_objects()
    
    def remove_static_object(self, staticobject: StaticObject):
        self.static_objects.remove(staticobject)
        self.__recompute_static_objects()

    def __recompute_static_objects(self):
        
        # Mapped staticobjects
        mapped_static_objects = list(map(lambda s: s.get_ndarray(), self.static_objects))

        # Set numpy array
        self.static_objects = np.array(mapped_static_objects)
