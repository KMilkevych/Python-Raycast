import numpy as np

class Drawable:

    def __init__(self, tag: int, texture_id: int, x_pos: float, y_pos: float, z_pos: float):
        
        self.tag = tag
        self.texture_id = texture_id
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.z_pos = z_pos
    
    def get_ndarray(self) -> np.ndarray:
        return np.array([self.tag, self.texture_id, self.z_pos, self.x_pos, self.y_pos])
