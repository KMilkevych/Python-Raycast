# https://lodev.org/cgtutor/raycasting.html
# https://permadi.com/1996/05/ray-casting-tutorial-table-of-contents/

import pygame
import pygame.surfarray as surfarray

from pygame.locals import *

import numpy as np

import math

from core.level import Level

from core.texture_helper import TEXTURE_SIZE

from typing import Tuple

def compute_direction(angle: float) -> np.ndarray:
    return np.array([np.math.cos(angle), np.math.sin(angle)])

class Camera:

    def __init__(self, position: np.ndarray, angle: float, view_width: int, view_height: int):

        self.height = 32.
        
        self.fov = np.math.pi / 2
        self.view_width = view_width
        self.view_height = view_height
        self.DISTANCE_TO_PROJECTION_PLANE = (self.view_width / 2) / np.math.tan(self.fov / 2)

        self.speed = 32
        self.turn_speed = 2
        self.tilt_speed = 2

        #self.COLUMN_WIDTH = PLAYER_FOV / WORKING_SIZE[0]

        self.position = np.array([position[0], position[1]])
        self.angle = angle
        self.vangle = 0.
        self.tilt_offset = 0
        self.direction = compute_direction(self.angle)

        self.INTENSITY = 6.0
        self.INTENSITY_MULTIPLIER = 32 * self.INTENSITY
    
    def turn(self, direction: float, deltaTime: float):

        # Change angle
        self.angle += direction * deltaTime * self.turn_speed

        # Recompute direction
        self.direction = compute_direction(self.angle)
    
    def tilt(self, direction: float, deltaTime: float):

        # Change vangle
        self.vangle += direction * deltaTime * self.tilt_speed
        self.vangle = np.clip(self.vangle, -np.pi/2.5, np.pi/2.5)

        # Update tilt offset
        self.tilt_offset = (np.tan(self.vangle) * self.DISTANCE_TO_PROJECTION_PLANE).astype(int)
    
    def move(self, direction: float, deltaTime: float):

        # Change position
        self.position += direction * self.direction * self.speed * deltaTime
    
    def strafe(self, direction: float, deltaTime: float):

        # Change position
        self.position += direction * np.array([-self.direction[1], self.direction[0]]) * self.speed * deltaTime
    
    def strafe_collide(self, direction: float, deltaTime: float, level: Level):

        # Define wall margin
        margin = 2
        
        # Compute new position
        pos_change = direction * np.array([-self.direction[1], self.direction[0]]) * self.speed * deltaTime
        new_pos = self.position + pos_change

        # Get current cell position
        cellX = math.floor(self.position[0] / level.tile_size[0])
        cellY = math.floor(self.position[1] / level.tile_size[1])

        # Get would-be cell position
        ncellX = math.floor((new_pos[0] + np.sign(pos_change[0]) * margin) / level.tile_size[0])
        ncellY = math.floor((new_pos[1] + np.sign(pos_change[1]) * margin) / level.tile_size[1])

        # Check for both x movement and y movement
        if level.walls[cellY][ncellX][0] != 0:
            
            # Go to the edge of that cell
            new_pos[0] = ncellX * level.tile_size[0] - np.sign(pos_change[0]) * margin + (np.sign(pos_change[0]) - 1) * level.tile_size[0] / (-2)

        if level.walls[ncellY][cellX][0] != 0:
            
            # Go to the edge of that cell
            new_pos[1] = ncellY * level.tile_size[1] - np.sign(pos_change[1]) * margin + (np.sign(pos_change[1]) - 1) * level.tile_size[1] / (-2)
            
        # Update own position
        self.position = new_pos
    
    def move_collide(self, direction: float, deltaTime: float, level: Level):

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
        if level.walls[cellY][ncellX][0] != 0:
            
            # Go to the edge of that cell
            new_pos[0] = ncellX * level.tile_size[0] - np.sign(pos_change[0]) * margin + (np.sign(pos_change[0]) - 1) * level.tile_size[0] / (-2)

        if level.walls[ncellY][cellX][0] != 0:
            
            # Go to the edge of that cell
            new_pos[1] = ncellY * level.tile_size[1] - np.sign(pos_change[1]) * margin + (np.sign(pos_change[1]) - 1) * level.tile_size[1] / (-2)
            
        # Update own position
        self.position = new_pos
    
    def compute_sprite_data(self, level: Level, drawables: np.ndarray) -> np.ndarray:

        # Sprite positions relative to camera
        sprite_positions = drawables[:, [3, 4]]
        sprite_positions -= (self.position / np.array([level.tile_size[0], level.tile_size[1]]))[:, np.newaxis].T

        # Camera plane
        camera_plane_length = np.math.tan(self.fov / 2)
        camera_plane = np.array([-self.direction[1], self.direction[0]])[:, np.newaxis]
        camera_plane = (camera_plane) * camera_plane_length

        camera_view_inv = np.linalg.inv(np.hstack([camera_plane, self.direction[:, np.newaxis]]))

        # Compute sprite positions in camera view
        sprite_positions = (camera_view_inv @ sprite_positions.T).T
        sprite_distances = sprite_positions[:, [1]] * level.tile_size[0]

        # Compute horisontal offsets when drawing sprites on screen
        sprite_screen_xs = ((self.view_width/2) * (1 + sprite_positions[:, [0]] / sprite_positions[:, [1]])).astype(int)

        # Compute vertical offset when drawing sprite based on sprites desired height/z-pos, player height, player tilt and distance
        sprite_heights, sprite_offsets = self.height_and_offset_from_distance(drawables[:, [2]], sprite_distances[:])
        sprite_heights = np.clip(sprite_heights, 0, 2*self.view_height)
        sprite_offsets += self.tilt_offset

        # Compute sprite dimensions. Reduce width by 2x to acommodate for 320x400 resolution which "fattens" sprites
        sprite_sizes = np.hstack([sprite_heights/2, sprite_heights])
        
        # Compute draw_start and draw_end
        sprite_draw_start = np.hstack([sprite_screen_xs - (sprite_sizes[:, [0]]/2), sprite_offsets])
        sprite_draw_end = sprite_draw_start + sprite_sizes

        # Build sprite data: (height, distance, size, draw_start)
        sprite_data = np.hstack([drawables[:, [1]], sprite_distances[:], sprite_sizes, sprite_draw_start])

        # Remove inappropriate sprite data using row mask
        rows_mask = (sprite_draw_end[:, 0] > 0) & (sprite_draw_start[:, 0] < self.view_width) & (sprite_positions[:, 1] > 0)
        sprite_data = sprite_data[rows_mask, :]

        # Lastly, sort by distance
        sprite_data = np.flip(sprite_data[sprite_data[:, 1].argsort()], axis=0)

        # return sprite data
        return sprite_data

    def do_floorcast_to_surface(self, level: Level, textures) -> pygame.Surface:

        # Load textures as numpy array
        tile_textures = np.array(list(map(surfarray.array2d, textures)))
        
        # Create a surface
        surface = pygame.Surface((self.view_width, self.view_height))
        surface_array = surfarray.pixels2d(surface)

        # Compute angle mod
        angle_mod = np.math.atan2((self.view_width / 2), self.DISTANCE_TO_PROJECTION_PLANE)

        # Compute the left-most ray and right-most ray
        left_ray = compute_direction(self.angle - angle_mod)
        right_ray = compute_direction(self.angle + angle_mod)

        # Generate rows
        middle = max(0, int(self.view_height/2 + self.tilt_offset))
        look_offsets = (np.arange(self.view_height) - self.view_height/2)[:, np.newaxis]
        np.subtract(look_offsets, self.tilt_offset, look_offsets) # Apply look_offsets
        

        # Compute h_distances
        h_distances = np.empty_like(look_offsets)
        h_distances[:middle, 0] = (level.ceiling_height - self.height) * self.DISTANCE_TO_PROJECTION_PLANE / (-look_offsets[:middle,0] * np.math.cos(angle_mod))
        h_distances[middle+1:, 0] = (self.height) * self.DISTANCE_TO_PROJECTION_PLANE / (look_offsets[middle+1:,0] * np.math.cos(angle_mod))

        # Compute ray hits
        ray_hit_left = (left_ray * h_distances)
        np.add(ray_hit_left, self.position, ray_hit_left)
        np.multiply(ray_hit_left, np.array([TEXTURE_SIZE[0] / level.tile_size[0], TEXTURE_SIZE[1] / level.tile_size[1]]), ray_hit_left)

        ray_hit_right = (right_ray * h_distances)
        np.add(ray_hit_right, self.position, ray_hit_right)
        np.multiply(ray_hit_right, np.array([TEXTURE_SIZE[0] / level.tile_size[0], TEXTURE_SIZE[1] / level.tile_size[1]]), ray_hit_right)

        # Do linear interpolation for ray hits
        ray_hits_x = np.linspace(ray_hit_left[:, 0], ray_hit_right[:, 0], self.view_width, axis=1)
        ray_hits_y = np.linspace(ray_hit_left[:, 1], ray_hit_right[:, 1], self.view_width, axis=1)

        # Merge into x, y coordinate pairs for each row, column
        ray_hits = np.dstack([ray_hits_x, ray_hits_y]) # row, column, (x, y)

        # Fetch floor and ceiling as numpy arrays
        floor = np.array(level.floors)
        ceiling = np.array(level.ceilings)

        # Compute which cells on the floor we hit and get the right textures and clip to size
        cells = (ray_hits / np.array([TEXTURE_SIZE[0], TEXTURE_SIZE[1]])).astype(int)
        np.clip(cells[:,:,0], 0, floor.shape[0]-1, cells[:,:,0])
        np.clip(cells[:,:,1], 0, floor.shape[1]-1, cells[:,:,1])        

        # Compute which texture ids the cells hit by rays correspond to
        cell_texture_ids = np.empty((self.view_height, self.view_width)).astype(int)
        cell_texture_ids[:middle] = ceiling[cells[:middle,:,1], cells[:middle,:,0]]
        cell_texture_ids[middle:] = floor[cells[middle:,:,1], cells[middle:,:,0]]

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
        blend_surface = pygame.Surface((self.view_width, self.view_height))

        # Compute intensities distances from h_distances
        intensities = np.empty_like(h_distances)

        np.square(h_distances, h_distances)
        np.divide(self.INTENSITY_MULTIPLIER*self.INTENSITY_MULTIPLIER, h_distances, intensities)
        np.clip(intensities, 0.0, 1.0, intensities)
        np.multiply(intensities, 255.0, intensities)

        intensities = np.tile(intensities, (1, self.view_width)).T

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
    
    def do_wallcast_to_surface(self, level: Level, raycast_data, textures) -> pygame.Surface:

        # Create a surface
        surface = pygame.Surface((self.view_width, self.view_height))

        # Create pygame surface for a line
        column = pygame.Surface((1, TEXTURE_SIZE[1]))

        # Draw columns to screen
        for col in range(self.view_width):

            # Extract data from dda
            distance, (mapX, mapY), face, offset = raycast_data[col]

            # Extract wall data from walls
            wall_tag, texture_id, wall_height = level.walls[mapY][mapX]

            # Compute height of wall, and space/offset at top based on self.camera height
            height, height_offset = self.height_and_offset_from_distance(wall_height, distance)

            # Compute modifiers
            shade_factor = 1.0 - 0.2 * (face % 2)

            intensify_factor = min(1.0, (self.INTENSITY_MULTIPLIER * self.INTENSITY_MULTIPLIER) / (distance * distance))
            final_factor = min(shade_factor * intensify_factor * 255, 255)

            # Apply texture to column
            column.blit(textures[texture_id], ((-1) * (offset), 0))

            # Apply effects
            column.fill((final_factor, final_factor, final_factor), special_flags=BLEND_MULT)

            # Blit column
            surface.blit(pygame.transform.scale(column, (1, height)), (col, height_offset + self.tilt_offset))
        
        # Return surface
        return surface

    def do_spritecast_to_surface(self, sprite_data, raycast_data, sprite_textures):

        # Create surface
        surface = pygame.Surface((self.view_width, self.view_height))

        # Iterate over each sprite in sprite_data
        for s in range(sprite_data.shape[0]):

            # Extract data
            texture_id, sprite_distance, sprite_size_x, sprite_size_y, draw_start_x, draw_start_y = sprite_data[s, :]

            texture_id = int(texture_id)
            sprite_size = ((sprite_size_x), (sprite_size_y))
            draw_start = (int(draw_start_x), int(draw_start_y))
            draw_end = (int(draw_start_x + sprite_size_x), int(draw_start_y + sprite_size_y))

            # Compute intensity
            final_factor = min(1.0, (self.INTENSITY_MULTIPLIER * self.INTENSITY_MULTIPLIER) / (sprite_distance * sprite_distance)) * 255

            # Compute surface to draw from
            sprite = pygame.transform.scale(sprite_textures[texture_id], sprite_size)
            
            # Create column surface
            column = pygame.Surface((1, sprite_size[1]))
            column.set_colorkey((0,0,0))

            # Iterate and blit each column of the sprite
            for col in range(draw_start[0], draw_end[0]):
                if col > 0 and col < self.view_width and sprite_distance < raycast_data[col][0]:
                    
                    # Blit to column
                    column.blit(sprite, (-(col - draw_start[0]), 0))

                    # Apply effects
                    column.fill((final_factor, final_factor, final_factor), special_flags=BLEND_MULT)

                    # Blit to self.screen
                    surface.blit(column, (col, draw_start[1]))
        
        # Return surface
        return surface

    def do_skycast_to_surface(self, sky_color, ground_color):

        # Make surface
        surface = pygame.Surface((self.view_width, self.view_height))

        # Draw sky and ground
        middle = max(0, int(self.view_height/2 + self.tilt_offset))
        pygame.draw.rect(surface, sky_color, pygame.Rect((0, 0), (self.view_width, middle)))
        pygame.draw.rect(surface, ground_color, pygame.Rect((0, middle), (self.view_width, self.view_height - middle)))

        # Return surface
        return surface

    def do_raycast(self, level: Level) -> list:

        # For each column / working x cast a ray using dda
        distances = [0 for col in range(self.view_width)]

        # Perform dda for each ray
        for col in range(self.view_width):
            
            angle_mod =  np.math.atan2((col - self.view_width / 2), self.DISTANCE_TO_PROJECTION_PLANE) # Slower but no curved edges

            rayDirection = compute_direction(self.angle + angle_mod)

            distance, (mapX, mapY), face, offset = self.do_dda(level, rayDirection)
            distances[col] = (distance * np.math.cos(angle_mod), (mapX, mapY), face, offset)
        
        # Return distances
        return distances
    
    def do_dda(self, level: Level, rayDirection: np.ndarray) -> Tuple[float, Tuple[int, int], int, int]:

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
            wall_tag = level.walls[mapY][mapX][0]
            if wall_tag != 0:
                hit = True

                if (side == 0):
                    perpWallDist = (sideDistX - deltaDistX) * level.tile_size[0]
                    face = 0 if stepX == -1 else 1
                    
                    #offset = math.floor(self.position[1] + perpWallDist * rayDirection[1]) % level.tile_size[1]
                    #offset = math.floor((self.position[1] + perpWallDist * rayDirection[1]) * (TEXTURE_SIZE[0] / level.tile_size[1]) ) % TEXTURE_SIZE[0]
                    offset = (posY + (sideDistX - deltaDistX) * rayDirection[1]) * TEXTURE_SIZE[0] % TEXTURE_SIZE[0]
                else:
                    perpWallDist = (sideDistY - deltaDistY) * level.tile_size[1]
                    face = 2 if stepY == -1 else 3

                    #offset = math.floor(self.position[0] + perpWallDist * rayDirection[0]) % level.tile_size[0]
                    #offset = math.floor((self.position[0] + perpWallDist * rayDirection[0])  * (TEXTURE_SIZE[0] / level.tile_size[0]) ) % TEXTURE_SIZE[0]
                    offset = (posX + (sideDistY - deltaDistY) * rayDirection[0]) * TEXTURE_SIZE[0] % TEXTURE_SIZE[0]


        return (perpWallDist, (mapX, mapY), face, offset)

    def height_and_offset_from_distance(self, true_height: float, distance: float) -> Tuple[float, float]:
        height = (true_height / distance) * self.DISTANCE_TO_PROJECTION_PLANE
        offset =  self.view_height/2 - height + ((self.height / distance) * self.DISTANCE_TO_PROJECTION_PLANE)
        return (height, offset)