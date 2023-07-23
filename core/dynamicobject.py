from core.staticobject import StaticObject

class DynamicObject(StaticObject):

    def __init__(self, tag: int, texture_id: int, x_pos: float, y_pos: float, z_pos: float):
        StaticObject.__init__(self, tag, texture_id, x_pos, y_pos, z_pos)

