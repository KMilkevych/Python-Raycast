import numpy as np
from core.level import Level

# Technical details for levels
tile_size = np.array([32, 32, 64])
ceiling_height = 96

# Each wall is defined by a tag / wall type, a texture and height
# type 0 == empty space / not wall
# textures are described by the indices in texture_helper.py
AIR = (0, 0, 0)

W_0 = (1, 1, tile_size[2])    # dark gray

W_1 = (1, 8, tile_size[2])    # blue_stone
W_2 = (1, 9, tile_size[2])    # color_stone
W_3 = (1, 10, tile_size[2])   # grey_stone 
W_4 = (1, 11, tile_size[2])   # mossy_stone
W_5 = (1, 12, tile_size[2])   # purple_stone
W_6 = (1, 13, tile_size[2])   # red_brick
W_7 = (1, 14, tile_size[2])   # eagle_brick
W_8 = (1, 15, tile_size[2])   # wood

W_9 = (1, 5, tile_size[2])    # brick_texture_01
W10 = (1, 6, tile_size[2])    # brick_texture_02
W11 = (1, 7, tile_size[2])    # brick_texture_03


# Each floor/ceiling is defined by texture id
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

# Each sprite is defined by a sprite object (tag/type, texture, height/z-pos) and a position in the game world (x, y)
BARREL = [1, 0, tile_size[2]]
PILLAR = [1, 1, tile_size[2]]
LAMP = [0, 2, ceiling_height]

#############################################################################

class Level0(Level):

    def __init__(self):

        # Draw walls
        walls = np.array([
            # 00   01   02   03   04   05   06   07   08   09   10   11   12   13   14   15
            [W_8, W_8, W_8, W_8, W_8, W_0, W_0, W_0, W_0, W_0, W_0, W_0, W_0, W_0, W_0, W_0],   # 00
            [W_8, AIR, AIR, AIR, AIR, W_8, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, W_0],   # 01
            [W_8, AIR, AIR, AIR, AIR, AIR, W_8, W_9, W_9, W_9, AIR, W_9, W_9, W_9, W_9, W_0],   # 02
            [W_8, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, W_9, AIR, AIR, AIR, W_0],   # 03
            [W_8, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, W_9, W_9, AIR, AIR, AIR, W_0],   # 04
            [W_8, AIR, AIR, AIR, AIR, W_8, AIR, AIR, W_5, W_5, AIR, AIR, AIR, AIR, AIR, W_0],   # 05
            [W_6, W_8, W_8, W_8, W_8, W_5, W_5, AIR, W_5, W_5, AIR, AIR, AIR, AIR, AIR, W_0],   # 06
            [W_6, W_6, W_6, W_6, W_6, AIR, AIR, AIR, AIR, AIR, W_6, AIR, AIR, AIR, AIR, W_0],   # 07
            [W_7, AIR, AIR, AIR, W_7, AIR, AIR, AIR, AIR, AIR, W_6, AIR, AIR, AIR, AIR, W_0],   # 08
            [W_6, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, W_7, AIR, AIR, AIR, AIR, W_0],   # 09
            [W_7, AIR, AIR, AIR, W_7, AIR, AIR, AIR, AIR, AIR, W_8, AIR, AIR, AIR, AIR, W_0],   # 10
            [W_6, W_6, AIR, W_6, W_6, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, W_0],   # 11
            [W_0, W_6, AIR, W_6, AIR, AIR, AIR, AIR, AIR, AIR, W_8, AIR, AIR, AIR, AIR, W_0],   # 12
            [W_0, W_6, AIR, W_6, AIR, AIR, AIR, AIR, AIR, AIR, W_7, AIR, AIR, AIR, AIR, W_0],   # 13
            [W_0, W_6, W_6, W_6, AIR, AIR, AIR, AIR, AIR, AIR, W_6, AIR, AIR, AIR, AIR, W_0],   # 14
            [W_0, W_0, W_0, W_0, W_6, W_6, W_6, W_6, W_6, W_6, W_6, W_0, W_0, W_0, W_0, W_0],   # 15
        ])

        # Draw floors
        floors = np.array([
            # 00   01   02   03   04   05   06   07   08   09   10   11   12   13   14   15
            [F_8, F_8, F_8, F_8, F_8, F_8, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3],   # 00
            [F_8, F_8, F_8, F_8, F_8, F_8, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3],   # 01
            [F_8, F_8, F_3, F_4, F_3, F_8, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3],   # 02
            [F_8, F_8, F_4, F_4, F_4, F_8, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3],   # 03
            [F_8, F_8, F_3, F_4, F_3, F_8, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3],   # 04
            [F_8, F_8, F_8, F_8, F_8, F_8, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3],   # 05
            [F_8, F_8, F_8, F_8, F_8, F_8, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3],   # 06
            [F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3],   # 07
            [F_3, F_3, F_3, F_3, F_3, F_3, F_4, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3],   # 08
            [F_3, F_3, F_3, F_3, F_3, F_3, F_4, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3],   # 09
            [F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3],   # 10
            [F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_4, F_3, F_3, F_3, F_3, F_3, F_3, F_3],   # 11
            [F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3],   # 12
            [F_3, F_3, F_3, F_3, F_3, F_4, F_3, F_4, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3],   # 13
            [F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_4, F_3, F_3, F_3, F_3, F_3, F_3, F_3],   # 14
            [F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3, F_3],   # 15
        ])

        # Draw ceilings
        ceilings = np.array([
            # 00   01   02   03   04   05   06   07   08   09   10   11   12   13   14   15
            [F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8],   # 00
            [F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8],   # 01
            [F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8],   # 02
            [F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8],   # 03
            [F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8],   # 04
            [F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8],   # 05
            [F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8],   # 06
            [F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8],   # 07
            [F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8],   # 08
            [F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8],   # 09
            [F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, TRN, TRN, TRN, F_8, F_8, F_8],   # 10
            [F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, TRN, TRN, TRN, F_8, F_8, F_8],   # 11
            [F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, TRN, TRN, TRN, F_8, F_8, F_8],   # 12
            [F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8],   # 13
            [F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8],   # 14
            [F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8, F_8],   # 15
        ])

        # Draw static objects
        static_objects = np.array([
            [*BARREL, 2.5, 8.5],
            [*PILLAR, 7.5, 9.5],
            [*PILLAR, 7.5, 11.5],
            [*PILLAR, 7.5, 13.5],
            [*LAMP, 2.5, 3.5],
            [*BARREL, 1.5, 1.5],
            [*BARREL, 1.5, 5.5],
            [*BARREL, 4.5, 13.0],
            [*BARREL, 4.5, 13.5],
            [*BARREL, 4.5, 14.0],
            [*LAMP, 1.5, 9.5],
            [*LAMP, 3.5, 9.5],
        ])
        #print(static_objects.shape)
        #print(static_objects)

        # Call level init
        Level.__init__(self,
                       tile_size,
                       ceiling_height,
                       np.array([2.5 * tile_size[0], 13.5 * tile_size[1]]),
                       np.pi * (3/2),
                       (160, 230, 230),
                       (60, 20, 0))

        # Set walls, floors, ceilings and add static objects
        self.set_walls(walls)
        self.set_floors(floors)
        self.set_ceilings(ceilings)
        self.set_static_drawables(static_objects)
