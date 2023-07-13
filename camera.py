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
        self.tilt_speed = PLAYER_TILT_SPEED

        self.position = np.array([position[0], position[1]])
        self.angle = angle
        self.vangle = 0.
        self.tilt_offset = 0
        self.direction = compute_direction(self.angle)
    
    def turn(self, direction, deltaTime):

        # Change angle
        self.angle += direction * deltaTime * self.turn_speed

        # Recompute direction
        self.direction = compute_direction(self.angle)
    
    def tilt(self, direction, deltaTime):

        # Change vangle
        self.vangle += direction * deltaTime * self.tilt_speed
        self.vangle = np.clip(self.vangle, -np.pi/3, np.pi/3)

        # Update tilt offset
        self.tilt_offset = (np.tan(self.vangle) * DISTANCE_TO_PROJECTION_PLANE).astype(int)
    
    def move(self, direction, deltaTime):

        # Change position
        self.position += direction * self.direction * self.speed * deltaTime
    
    def move_collide(self, direction, deltaTime, level):

        # Define wall margin
        margin = 2
        
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
    
    def do_floorcast_to_surface(self, level, textures):

        # Load textures as numpy array
        tile_textures = np.array(list(map(surfarray.array2d, textures)))
        
        # Create a surface
        surface = pygame.Surface(WORKING_SIZE)
        surface_array = surfarray.pixels2d(surface)

        # Compute angle mod
        angle_mod = np.math.atan2((WORKING_SIZE[0] / 2), DISTANCE_TO_PROJECTION_PLANE)

        # Compute the left-most ray and right-most ray
        left_ray = compute_direction(self.angle - angle_mod)
        right_ray = compute_direction(self.angle + angle_mod)

        # Generate rows
        middle = max(0, int(WORKING_SIZE[1]/2 + self.tilt_offset))
        look_offsets = (np.arange(WORKING_SIZE[1]) - WORKING_SIZE[1]/2)[:, np.newaxis]
        np.subtract(look_offsets, self.tilt_offset, look_offsets) # Apply look_offsets
        

        # Compute h_distances
        h_distances = np.empty_like(look_offsets)
        h_distances[:middle, 0] = (level.ceiling_height - self.height) * DISTANCE_TO_PROJECTION_PLANE / (-look_offsets[:middle,0] * np.math.cos(angle_mod))
        h_distances[middle+1:, 0] = (self.height) * DISTANCE_TO_PROJECTION_PLANE / (look_offsets[middle+1:,0] * np.math.cos(angle_mod))

        # Compute ray hits
        ray_hit_left = (left_ray * h_distances)
        np.add(ray_hit_left, self.position, ray_hit_left)

        ray_hit_right = (right_ray * h_distances)
        np.add(ray_hit_right, self.position, ray_hit_right)

        # Do linear interpolation for ray hits
        ray_hits_x = np.linspace(ray_hit_left[:, 0], ray_hit_right[:, 0], WORKING_SIZE[0], axis=1)
        ray_hits_y = np.linspace(ray_hit_left[:, 1], ray_hit_right[:, 1], WORKING_SIZE[0], axis=1)

        # Merge into x, y coordinate pairs for each row, column
        ray_hits = np.dstack([ray_hits_x, ray_hits_y]) # row, column, (x, y)

        # Fetch floor and ceiling as numpy arrays
        floor = np.array(level.floors)
        ceiling = np.array(level.ceilings)

        # Compute which cells on the floor we hit and get the right textures and clip to size
        cells = (ray_hits / np.array([level.tile_size[0], level.tile_size[1]])).astype(int)
        np.clip(cells[:,:,0], 0, floor.shape[0]-1, cells[:,:,0])
        np.clip(cells[:,:,1], 0, floor.shape[1]-1, cells[:,:,1])        

        # Compute which texture ids the cells hit by rays correspond to
        cell_texture_ids = np.empty((WORKING_SIZE[1], WORKING_SIZE[0])).astype(int)
        cell_texture_ids[:middle] = ceiling[cells[:middle,:,0], cells[:middle,:,1]]
        cell_texture_ids[middle:] = floor[cells[middle:,:,0], cells[middle:,:,1]]

        # Compute coordinates on texture for each ray
        tex_size = np.array([TEXTURE_SIZE[0], TEXTURE_SIZE[1]])[np.newaxis, np.newaxis, :]

        texture_xys = ray_hits.astype(int)
        np.mod(texture_xys, tex_size, texture_xys)

        # Compute scanlines
        scanlines = tile_textures[cell_texture_ids, texture_xys[:,:,0], texture_xys[:,:,1]]

        # Write scanlines to surface
        surface_array[:, :] = scanlines.T

        # Delete surface array
        del surface_array

        # Create a blend surface
        blend_surface = pygame.Surface(WORKING_SIZE)

        # Compute intensities distances from h_distances
        intensities = np.empty_like(h_distances)

        np.square(h_distances, h_distances)
        np.divide(INTENSITY_MULTIPLIER*INTENSITY_MULTIPLIER, h_distances, intensities)
        np.clip(intensities, 0.0, 1.0, intensities)
        np.multiply(intensities, 255.0, intensities)

        intensities = np.tile(intensities, (1, WORKING_SIZE[0])).T

        # Create a blend surface array
        blend_surface_array = surfarray.pixels3d(blend_surface)

        # Apply intensities to blend_surface
        blend_surface_array[:] = np.dstack([intensities, intensities, intensities])[:]
        
        # Dispose blend_surface_array
        del blend_surface_array

        # Apply blend surface
        surface.blit(blend_surface, (0, 0), special_flags=pygame.BLEND_MULT)

        # Return surface
        return surface
        
        
    def do_raycast(self, level):

        # For each column / working x cast a ray using dda
        distances = [0 for col in range(WORKING_SIZE[0])]

        # Perform dda for each ray
        for col in range(WORKING_SIZE[0]):
            
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
    '''
    def column_height_from_distance_with_modifier(self, level, distance, modifier):
        height = (level.tile_size[2] / distance) * DISTANCE_TO_PROJECTION_PLANE * modifier
        offset =  WORKING_SIZE[1]/2 - height + ((self.height / distance) * DISTANCE_TO_PROJECTION_PLANE)
        return (height, offset)
    '''