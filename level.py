import numpy as np

class Level:

    def __init__(self):

        self.tile_size = np.array([32, 32, 64])
        self.ceiling_height = 128

        # Each wall is defined by a tag / wall type, a texture and height
        # type 0 == empty space / not wall
        # textures are described by the indices in texture_helper.py

        AIR = (0, 0, 0)

        W_0 = (1, 1, 64)    # dark gray

        W_1 = (1, 8, 64)    # blue_stone
        W_2 = (1, 9, 64)    # color_stone
        W_3 = (1, 10, 64)   # grey_stone 
        W_4 = (1, 11, 64)   # mossy_stone
        W_5 = (1, 12, 64)   # purple_stone
        W_6 = (1, 13, 64)   # red_brick
        W_7 = (1, 14, 64)   # eagle_brick
        W_8 = (1, 15, 64)   # wood

        W_9 = (1, 5, 64)    # brick_texture_01
        W10 = (1, 6, 64)    # brick_texture_02
        W11 = (1, 7, 64)    # brick_texture_03

        self.walls = np.array([
            [W_0, W_0, W_0, W_0, W_0, W_0, W_0, W_0, W_0, W_0, W_0, W_0, W_0, W_0, W_0, W_0],
            [W_0, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, W_0],
            [W_0, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, W_0],
            [W_0, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, W_0],
            [W_0, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, W_0],
            [W_0, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, W_0],
            [W_0, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, W_0],
            [W_0, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, W_0],
            [W_0, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, W_0],
            [W_0, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, W_0],
            [W_0, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, W_0],
            [W_0, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, W_0],
            [W_0, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, W_0],
            [W_0, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, W_0],
            [W_0, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, W_0],
            [W_0, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, W_0],
            [W_0, W_0, W_0, W_0, W_0, W_0, W_0, W_0, W_0, W_0, W_0, W_0, W_0, W_0, W_0, W_0],
        ])


        # Each floor/ceiling is defined by texture id
        # TODO: allow a "transparent" texture to make holes in floors and ceilings

        TRN = (16)  # Transparent
        F_0 = (1)   # Dark gray

        F_1 = (8)    # blue_stone
        F_2 = (9)    # color_stone
        F_3 = (10)   # grey_stone 
        F_4 = (11)   # mossy_stone
        F_5 = (12)   # purple_stone
        F_6 = (13)   # red_brick
        F_7 = (14)   # eagle_brick
        F_8 = (15)   # wood

        F_9 = (5)    # brick_texture_01
        F10 = (6)    # brick_texture_02
        F11 = (7)    # brick_texture_03
        

        self.floors = np.array([
            [F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3],
            [F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3],
            [F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3],
            [F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3],
            [F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3],
            [F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3],
            [F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3],
            [F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3],
            [F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3],
            [F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3],
            [F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3],
            [F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3],
            [F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3],
            [F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3],
            [F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3],
            [F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3],
            [F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3],
        ])

        self.ceilings = np.array([
            [F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8],
            [F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8],
            [F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8],
            [F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8],
            [F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8],
            [F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8],
            [F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8],
            [F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8],
            [F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8],
            [F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8],
            [F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8],
            [F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8],
            [F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8],
            [F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8],
            [F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8],
            [F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8],
            [F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8],
        ])

        # Each sprite is defined by a sprite object (tag/type, texture, height/z-pos) and a position in the game world (x, y)
        BARREL = [1, 0, 32]
        PILLAR = [1, 1, 32]
        LAMP = [0, 2, 64]

        sprite_positions = np.array([
            [6.5, 5.5],
            [6.5, 6.5],
            [7.5, 10.5],
            [8., 10.],
            [9.5, 10.5],
            [10.5, 10.5]
        ])

        sprite_types = np.vstack([
            BARREL,
            BARREL,
            PILLAR,
            PILLAR,
            LAMP,
            LAMP
        ])


        self.sprites = np.hstack([
            sprite_types, sprite_positions
        ])
