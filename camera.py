# https://lodev.org/cgtutor/raycasting.html
# https://permadi.com/1996/05/ray-casting-tutorial-table-of-contents/

import numpy as np
from constants import *

import math

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
    
    def move_collide(self, direction, deltaTime, level):

        # Define wall margin
        margin = 4
        
        # Compute new position
        pos_change = direction * self.direction * self.speed * deltaTime
        new_pos = self.position + pos_change

        # Get current cell position
        cellX = math.floor(self.position[0] / level.tile_size[0])
        cellY = math.floor(self.position[1] / level.tile_size[1])

        # Get would-be cell position
        ncellX = math.floor((new_pos[0] + np.sign(pos_change[0]) * margin) / level.tile_size[0])
        ncellY = math.floor((new_pos[1] + np.sign(pos_change[1]) * margin) / level.tile_size[1])

        # Check for both x movement and y movement
        if level.walls[cellY][ncellX] != 0:
            
            # Go to the edge of that cell
            new_pos[0] = ncellX * level.tile_size[0] - np.sign(pos_change[0]) * margin + (np.sign(pos_change[0]) - 1) * level.tile_size[0] / (-2)

        if level.walls[ncellY][cellX] != 0:
            
            # Go to the edge of that cell
            new_pos[1] = ncellY * level.tile_size[1] - np.sign(pos_change[1]) * margin + (np.sign(pos_change[1]) - 1) * level.tile_size[1] / (-2)
            
        # Update own position
        self.position = new_pos
        
    def do_raycast(self, level):

        # For each column / working x cast a ray using dda
        distances = [0 for col in range(WORKING_SIZE[0])]

        # Perform dda for each ray
        for col in range(WORKING_SIZE[0]):
            angle_mod = (col - WORKING_SIZE[0] / 2) * COLUMN_WIDTH
            rayDirection = compute_direction(self.angle + angle_mod)

            distance, cell, face, offset = self.do_dda(level, rayDirection)
            distances[col] = (distance * np.math.cos(angle_mod), cell, face, offset)
        
        # Return distances
        return distances
    
    def do_dda(self, level, rayDirection):

        posX = self.position[0] / level.tile_size[0]
        posY = self.position[1] / level.tile_size[1]

        mapX = int(posX)
        mapY = int(posY)

        sideDistX = 0
        sideDistY = 0

        deltaDistX = 1e30 if (rayDirection[0] == 0) else np.abs(1 / rayDirection[0])
        deltaDistY = 1e30 if (rayDirection[1] == 0) else np.abs(1 / rayDirection[1])

        perpWallDist = 1e30

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
        face = 0
        offset = 0
        cell = 0
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
            
            if mapY >= len(level.walls) or mapX >= len(level.walls[mapY]):
                break

            # Check if we hit a wall on mapX mapY
            cell = level.walls[mapY][mapX]
            if cell != 0:
                hit = True

                if (side == 0):
                    perpWallDist = (sideDistX - deltaDistX) * level.tile_size[0]
                    face = 0 if stepX == -1 else 1
                    
                    offset = math.floor(self.position[1] + perpWallDist * rayDirection[1]) % level.tile_size[1]
                else:
                    perpWallDist = (sideDistY - deltaDistY) * level.tile_size[1]
                    face = 2 if stepY == -1 else 3

                    offset = math.floor(self.position[0] + perpWallDist * rayDirection[0]) % level.tile_size[0]
                    

        return (perpWallDist, cell, face, offset)
    
    def do_modified_dda(self, level, rayDirection):

        posX = self.position[0] / level.tile_size[0]
        posY = self.position[1] / level.tile_size[1]

        mapX = int(posX)
        mapY = int(posY)

        sideDistX = 0
        sideDistY = 0

        deltaDistX = 1e30 if (rayDirection[0] == 0) else np.abs(1 / rayDirection[0])
        deltaDistY = 1e30 if (rayDirection[1] == 0) else np.abs(1 / rayDirection[1])

        perpWallDist = 1e30

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
        #face = 0
        #offset = 0
        cell = 0
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
            
            if mapY >= len(level.walls) or mapX >= len(level.walls[mapY]):
                break

            # Check if we hit a wall on mapX mapY
            cell = level.walls[mapY][mapX]
            if cell != 0:
                hit = True

                if (side == 0):
                    perpWallDist = (sideDistX - deltaDistX) * level.tile_size[0]
                    #face = 0 if stepX == -1 else 1
                    
                    #offset = math.floor(self.position[1] + perpWallDist * rayDirection[1]) % level.tile_size[1]
                else:
                    perpWallDist = (sideDistY - deltaDistY) * level.tile_size[1]
                    #face = 2 if stepY == -1 else 3

                    #offset = math.floor(self.position[0] + perpWallDist * rayDirection[0]) % level.tile_size[0]
                    

        return (perpWallDist, side, mapX, mapY)