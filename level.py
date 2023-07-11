
class Level:

    def __init__(self):

        self.tile_size = (32, 32, 64)

        self.walls = [
            [ 1, 1, 1, 1, 1, 1, 5, 5, 6, 6, 7, 7, 8, 8, 9, 1],
            [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
            [ 1, 0,12,12,12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
            [ 1, 0,12, 0,12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
            [ 1, 0,12,12,12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,10],
            [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,10],
            [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,11],
            [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,11],
            [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,14,14, 0,14, 1],
            [ 1, 0, 9, 9, 9, 9, 9, 0, 0, 0, 0,14,14, 0,14, 1],
            [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,14,14, 0, 0, 1],
            [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,14,14,14,14, 1],
            [ 1, 0, 0, 0, 0, 0, 0, 2, 3, 4, 0, 0,14,14,14, 1],
            [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [ 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

        self.floors = [
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 15, 15, 15, 15, 15, 15, 15],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 15, 15, 15, 15, 15, 15, 15],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 15, 15, 15, 15, 15, 15, 15],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 15, 15, 15, 15, 15, 15, 15],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 15, 15, 15, 15, 15, 15, 15],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 15, 15, 15, 15, 15, 15, 15],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 15, 15, 15, 15, 15, 15, 15],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 15, 15, 15, 15, 15, 15, 15],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 15, 15, 15, 15, 15, 15, 15],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 15, 15, 15, 15, 15, 15, 15],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 15, 15, 15, 15, 15, 15, 15],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 15, 15, 15, 15, 15, 15, 15],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 15, 15, 15, 15, 15, 15, 15]
        ]

        self.ceilings = [
            [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15],
            [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15],
            [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15],
            [15, 15, 15, 15, 15, 15, 15, 15, 15,  9,  9,  9,  9,  9,  9,  9],
            [15, 15, 15, 11, 11, 10, 10, 15, 15,  9,  9,  9,  9,  9,  9,  9],
            [15, 15, 15, 11, 11, 11, 10, 15, 15,  9,  9,  9,  9,  9,  9,  9],
            [15, 15, 15, 11, 11, 11, 10, 15, 15,  9,  9,  9,  9,  9,  9,  9],
            [15, 15, 15, 11, 11, 11, 10, 15, 15,  9,  9,  9,  9,  9,  9,  9],
            [15, 15, 15, 11, 11, 11, 10, 15, 15,  9,  9,  9,  9,  9,  9,  9],
            [15, 15, 15, 11, 11, 11, 10, 15, 15,  9,  9,  7,  7,  7,  7,  7],
            [15, 15, 15, 15, 15, 15, 15, 15, 15,  9,  9,  7,  7,  7,  7,  7],
            [15, 15, 15, 15, 15, 15, 15, 15, 15,  9,  9,  7,  9,  9,  9,  7],
            [15, 15, 15, 15, 15, 15, 15, 15, 15,  9,  9,  7,  9,  7,  9,  7],
            [15, 15, 15, 15, 15, 15, 15, 15, 15,  7,  7,  7,  9,  7,  7,  7],
            [15, 15, 15, 15, 15, 15, 15, 15, 15,  9,  9,  9,  9,  7,  7,  9],
            [15, 15, 15, 15, 15, 15, 15, 15, 15,  7,  7,  7,  9,  9,  9,  9]
        ]

