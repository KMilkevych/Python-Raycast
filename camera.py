# https://lodev.org/cgtutor/raycasting.html
# https://permadi.com/1996/05/ray-casting-tutorial-table-of-contents/

import pygame
import pygame.surfarray as surfarray

import numpy as np
from constants import *

import math

from texture_helper import *

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
    
    def do_floorcast_to_surface(self, distances, level, textures):

        # Downscale
        step = 1
        
        # Create a surface
        surface = pygame.Surface(WORKING_SIZE)
        surface_array = surfarray.pixels2d(surface)

        # Compute angle mod
        angle_mod = np.math.atan2((WORKING_SIZE[0] / 2), DISTANCE_TO_PROJECTION_PLANE)

        # Iterate over each horisontal row
        for row in range(0, WORKING_SIZE[1]):

            # Compute the left-most ray and right-most ray
            left_ray = compute_direction(self.angle - angle_mod)
            right_ray = compute_direction(self.angle + angle_mod)

            # Compute how many ray "extensions" for the ray to hit the ground
            look_offset = row - WORKING_SIZE[1]/2
            
            if look_offset == 0:
                continue
            
            # WORKS FOR FLOORS
            h_distance =  np.abs((self.height * DISTANCE_TO_PROJECTION_PLANE) / (look_offset * np.math.cos(angle_mod)))

            # WORKS FOR CEILINGS
            #h_distance =  np.abs(((level.tile_size[2] - self.height) * DISTANCE_TO_PROJECTION_PLANE) / (look_offset * np.math.cos(angle_mod)))

            # Now compute, where each ray hits the ground
            floor_left_xy = left_ray * h_distance + self.position
            floor_right_xy = right_ray * h_distance + self.position

            # Now linearly interpolate between these
            map_xs = np.linspace(floor_left_xy[0], floor_right_xy[0], WORKING_SIZE[0])
            map_ys = np.linspace(floor_left_xy[1], floor_right_xy[1], WORKING_SIZE[0])

            map_xys = np.vstack([map_xs, map_ys]).T
            
            # Compute which cells on the floor map we hit
            cell_xys = np.floor(map_xys / np.array([level.tile_size[0], level.tile_size[1]])[:, np.newaxis].T).astype(int)

            # Compute texture coordinates for each of those hits
            texture_xys = (np.floor(map_xys) % np.array([TEXTURE_SIZE[0], TEXTURE_SIZE[1]])[:, np.newaxis].T).astype(int)

            # Compute which cells on the floor we hit and get the right textures
            # ...

            # Now compute scanline pixels
            texture_ceiling_floor = [surfarray.array2d(textures[15]), surfarray.array2d(textures[10])]
            scanline = texture_ceiling_floor[int((np.sign(look_offset)+1)/2)][texture_xys[:,0], texture_xys[:,1]]


            # Place into surface array
            surface_array[:, row] = scanline

        # Return surface
        return surface
            
        '''
        # Iterate over each vertical column
        for col in range(0, WORKING_SIZE[0], 1):

            # Compute relative angle based on column
            angle_mod =  np.math.atan2((col - WORKING_SIZE[0] / 2), DISTANCE_TO_PROJECTION_PLANE) # Slower but no curved edges
            rayDirection = compute_direction(self.angle + angle_mod).reshape((1, -1))

            # Extract the distance to the thingy from the thiny
            distance = distances[col][0]

            # Compute the height and height_offset
            column_height, column_offset = self.column_height_from_distance(level, distance)

            # Generate numpy array of certain size to contain row counts
            nrows = WORKING_SIZE[1] - math.floor(column_height + column_offset)
            rowarray = np.arange(math.floor(column_height + column_offset), WORKING_SIZE[1], 1)

            # Now compute the look offsets
            look_offsets = rowarray - WORKING_SIZE[1]/2

            # Now compute horisontal distances
            h_distances = (1/look_offsets) * ((self.height * DISTANCE_TO_PROJECTION_PLANE) / np.math.cos(angle_mod))
            h_distances = h_distances.reshape((-1, 1))

            # Now compute the xy_distances
            xy_distances = h_distances @ rayDirection

            # Compute level_xy
            level_xy = (xy_distances + np.tile(self.position, (xy_distances.shape[0], 1)))
            level_xy = np.transpose(level_xy) / np.array([level.tile_size[0], level.tile_size[1]])[:, np.newaxis]

            # Compute cell_xy
            cell_xy = np.floor(level_xy).T.astype(int)

            # Compute texture_xy
            texture_xy = (level_xy * np.array([level.tile_size[0], level.tile_size[1]])[:, np.newaxis]) % np.array([TEXTURE_SIZE[0], TEXTURE_SIZE[1]])[:, np.newaxis]
            texture_xy = np.floor(texture_xy).T.astype(int)

            # Compute the textures array
            floor = np.array(level.floors) # REFACTOR THIS

            floor_texture_ids = floor[cell_xy[:,[0]], cell_xy[:,[1]]] # NOT USED YET

            texture = surfarray.array2d(textures[14])
            floor_pixels = texture[texture_xy[:,[0]], texture_xy[:,[1]]]

            # Draw using pixel references
            surface_array[col, math.floor(column_height + column_offset):WORKING_SIZE[1]] = floor_pixels[:,0]

        del surface_array

        # Return surface
        return surface        

    # Now draw everything
    '''
    '''
    for row in range(nrows):

        # Extract cell_xy and texture_xy
        cell = cell_xy[row, :]
        texture = texture_xy[row, :]

        # Now we feast, get texture
        cellx = cell[0].astype(int)
        celly = cell[1].astype(int)

        texture_id = 0
        if not(cellx < 0 or celly < 0 or celly >= len(level.floors) or cellx >= len(level.floors[celly])):
            texture_id = level.floors[celly][cellx]
        
        # Now draw that to the pixel on the screen
        pixel.blit(textures[texture_id], (-texture[0], -texture[1]))

        # Draw pixel to surface
        surface.blit(pygame.transform.scale(pixel, (step, step)), (col, row + math.floor(column_height + column_offset)))
    '''

    '''
    # Now work for each floor pixel
    for row in range(math.floor(column_height + column_offset), WORKING_SIZE[1], step):

        # Compute the horisontal distance on the floor/horisontal distance to where intersection with floor occurs
        look_offset = (row - WORKING_SIZE[1]/2)

        if look_offset == 0:
            continue

        h_distance = (self.height * DISTANCE_TO_PROJECTION_PLANE) / (look_offset * np.math.cos(angle_mod))

        # Now we part this into x and y distances using player angle
        # xy_distance = self.direction * h_distance
        xy_distance = rayDirection * h_distance


        # Now compute the exact cell
        levelX = (xy_distance[0] + self.position[0]) / level.tile_size[0]
        levelY = (xy_distance[1] + self.position[1]) / level.tile_size[1]

        cellX = math.floor(levelX)
        cellY = math.floor(levelY)

        texture_id = 0
        if not(cellX < 0 or cellY < 0 or cellY >= len(level.floors) or cellX >= len(level.floors[cellY])):
            texture_id = level.floors[cellY][cellX]

        # Now compute the texture x and y
        textureX = levelX * level.tile_size[0] / step % TEXTURE_SIZE[0]
        textureY = levelY * level.tile_size[1] / step % TEXTURE_SIZE[1]


        # Now draw that to the pixel on the screen
        pixel.blit(textures[texture_id], (-textureX, -textureY))

        # Draw pixel to surface
        surface.blit(pygame.transform.scale(pixel, (step, step)), (col, row))

    # We have our own direction vector, now compute the look angle
    '''
        
        
    def do_raycast(self, level):

        # For each column / working x cast a ray using dda
        distances = [0 for col in range(WORKING_SIZE[0])]

        # Perform dda for each ray
        for col in range(WORKING_SIZE[0]):
            
            #angle_mod = (col - WORKING_SIZE[0] / 2) * COLUMN_WIDTH # This is faster, but gives curved edges effect
            angle_mod =  np.math.atan2((col - WORKING_SIZE[0] / 2), DISTANCE_TO_PROJECTION_PLANE) # Slower but no curved edges

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

    def column_height_from_distance(self, level, distance):
        height = (level.tile_size[2] / distance) * DISTANCE_TO_PROJECTION_PLANE
        offset =  WORKING_SIZE[1]/2 - height + ((self.height / distance) * DISTANCE_TO_PROJECTION_PLANE)
        return (height, offset)