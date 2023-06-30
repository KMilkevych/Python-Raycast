# https://lodev.org/cgtutor/raycasting.html
# https://permadi.com/1996/05/ray-casting-tutorial-table-of-contents/

import numpy as np
from constants import *

def compute_direction(angle):
    return np.array([np.math.cos(angle), np.math.sin(angle)])

class Camera:

    def __init__(self, position, angle):
        self.height = 32.
        self.fov = PLAYER_FOV
        self.speed = PLAYER_SPEED
        self.turn_speed = PLAYER_TURN_SPEED

        self.position = np.array([position[0], position[1]])
        self.angle = angle
        self.direction = compute_direction(self.angle)
    
    def turn(self, direction, deltaTime):

        # Change angle
        self.angle += direction * deltaTime * self.turn_speed

        # Recompute direction
        self.direction = compute_direction(self.angle)
    
    def move(self, direction, deltaTime):

        # Change position
        self.position += direction * self.direction * self.speed * deltaTime
    
    def do_raycast(self, level):

        # For each column / working x cast a ray using dda
        distances = [(0., "") for col in range(WORKING_SIZE[0])]

        # Perform dda for each ray
        for col in range(WORKING_SIZE[0]):

            rayDirection = compute_direction(self.angle + (col - WORKING_SIZE[0] / 2.) * COLUMN_WIDTH)
            distances[col] = self.do_dda(level, rayDirection)
        
        # Return distances
        return distances
    
    def do_dda(self, level, rayDirection):

        posX = self.position[0] / TILE_SIZE[0]
        posY = self.position[1] / TILE_SIZE[1]

        mapX = int(posX)
        mapY = int(posY)

        sideDistX = 0
        sideDistY = 0

        deltaDistX = 1e30 if (rayDirection[0] == 0) else np.abs(1 / rayDirection[0])
        deltaDistY = 1e30 if (rayDirection[1] == 0) else np.abs(1 / rayDirection[1])

        perpWallDist = 0

        stepX = 0
        stepY = 0

        if rayDirection[0] < 0:
            stepX = -1
            sideDistX = (posX - mapX) * deltaDistX
        else:
            stepX = 1
            sideDistX = (mapX + 1.0 - posX) * deltaDistX
        
        if rayDirection[1] < 0:
            stepY = -1
            sideDistY = (posY - mapY) * deltaDistY
        else:
            stepY = 1
            sideDistY = (mapY + 1.0 - posY) * deltaDistY

        hit = False
        side = 0
        while not(hit):

            # Jump in x-direction or y-direction to next grid cell
            if (sideDistX < sideDistY):
                sideDistX += deltaDistX
                mapX += stepX
                side = 0
            else:
                sideDistY += deltaDistY
                mapY += stepY
                side = 1

            # Check if we hit a wall on mapX mapY
            if level[mapY][mapX] in WALLS:
                hit = True

                if (side == 0):
                    perpWallDist = (sideDistX - deltaDistX) * TILE_SIZE[0]
                else:
                    perpWallDist = (sideDistY - deltaDistY) * TILE_SIZE[1]

        return (perpWallDist, level[mapY][mapX])