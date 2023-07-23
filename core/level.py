import numpy as np
from typing import Tuple

from core.drawable import Drawable

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

        # Basic level defining variables
        self.tile_size = tile_size
        self.ceiling_height = ceiling_height

        self.player_start = player_start
        self.player_start_angle = player_start_angle
        
        self.ground_color = ground_color
        self.sky_color = sky_color
        
        # Walls registered
        self.__walls = np.array([])

        # Floors and ceilings registered
        #self.floors = []
        self.__floors = np.array([])

        #self.ceilings = []
        self.__ceilings = np.array([])

        # Static objects registered
        self.__static_drawables_list = []    # regular list
        self.__static_drawables = np.array([])  # numpy array
    
    def get_tile_size(self) -> np.ndarray:
        return self.tile_size

    def set_tile_size(self, tile_size: np.ndarray):
        self.tile_size = tile_size
    
    def get_ceiling_height(self) -> float:
        return self.ceiling_height
    
    def set_ceiling_height(self, ceiling_height: float):
        self.ceiling_height = ceiling_height
    
    def get_player_start(self) -> np.ndarray:
        return self.player_start
    
    def set_player_start(self, player_start: np.ndarray):
        self.player_start = player_start
    
    def get_player_start_angle(self) -> float:
        return self.player_start_angle
    
    def set_player_start_angle(self, player_start_angle: float):
        self.player_start_angle = player_start_angle
    
    def get_sky_color(self) -> Tuple[int, int, int]:
        return self.sky_color

    def set_sky_color(self, sky_color: Tuple[int, int, int]):
        self.sky_color = sky_color

    def get_ground_color(self) -> Tuple[int, int, int]:
        return self.ground_color

    def set_ground_color(self, ground_color: Tuple[int, int, int]):
        self.ground_color = ground_color

    def get_walls(self) -> np.ndarray:
        return self.walls
    
    def set_walls(self, walls: np.ndarray):
        self.walls = walls
    
    def get_floors(self) -> np.ndarray:
        return self.floors
    
    def set_floors(self, floors: np.ndarray):
        self.floors = floors
    
    def get_ceilings(self) -> np.ndarray:
        return self.ceilings
    
    def set_ceilings(self, ceilings: np.ndarray):
        self.ceilings = ceilings
    
    def get_static_drawables(self) -> np.ndarray:
        return self.__static_drawables
    
    def set_static_drawables(self, static_drawables: np.ndarray):
        self.__static_drawables = static_drawables
        
    def add_static_drawable(self, static_drawable: Drawable):
        self.__static_drawables_list.append(static_drawable)
        self.__recompute_static_drawables()
    
    def remove_static_drawable(self, static_drawable: Drawable):
        self.__static_drawables_list.remove(static_drawable)
        self.__recompute_static_drawables()

    def __recompute_static_drawables(self):
        
        # Mapped staticobjects
        mapped_static_drawables = list(map(lambda s: s.get_ndarray(), self.__static_drawables_list))

        # Set numpy array
        self.__static_drawables_list = np.array(mapped_static_drawables)