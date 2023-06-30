# Import packages
import pygame
from pygame.locals import *

import numpy as np

from constants import *
import camera

# Game active objects
player = camera.Camera(position=(3. * TILE_SIZE[0], 3. * TILE_SIZE[1]), angle=np.math.pi)

# Initialize pygame window
pygame.init()
window = pygame.display.set_mode(WINDOW_SIZE, DOUBLEBUF, 16)
screen = pygame.Surface(WORKING_SIZE)

pygame.display.set_caption("Raycasting")

# Make clock
clock = pygame.time.Clock()

# Start game loop
running = True
dt = 0
while (running):

    # Fetch events
    for event in pygame.event.get():

        # Check if user has quit
        if event.type == pygame.QUIT:
            running = False

    # Update position based on inputs
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player.move(1., dt)
        print(player.position / TILE_SIZE[0])
    if keys[pygame.K_DOWN]:
        player.move(-1., dt)
        print(player.position / TILE_SIZE[0])
    if keys[pygame.K_LEFT]:
        player.turn(-1., dt)
    if keys[pygame.K_RIGHT]:
        player.turn(1., dt)
    
    # Print everything
    #print("Position: ", player.position)
    #print("Direction: ", player.direction)


    # Clear the screen
    screen.fill(pygame.Color(255, 255, 255))

    # Rendering code goes here
    # ...

    
    # Get raycast distances
    distances = player.do_raycast(LEVEL)
    
    # Print lines
    for col in range(WORKING_SIZE[0]):
        height = WORKING_SIZE[1] / distances[col][0]
        space = (WORKING_SIZE[1] - height) / 2

        type = distances[col][1]
        color = COLORS[type]

        pygame.draw.line(screen, color, (col, space), (col, WORKING_SIZE[1] - space))
    

    # Debugging draw
    scale = 4.0
    for y in range(len(LEVEL)):
        for x in range(len(LEVEL[y])):
            pygame.draw.rect(screen, COLORS[LEVEL[y][x]], pygame.Rect((x * scale, y * scale), (scale, scale)))

    pygame.draw.circle(screen, "black", player.position*scale/ TILE_SIZE[0], 4, 1)
    pygame.draw.line(screen, "green", player.position*scale / TILE_SIZE[0], player.position*scale/ TILE_SIZE[0] + player.direction * DISTANCE_TO_PROJECTION_PLANE * scale / (TILE_SIZE[0]**2), 1)


    # Paste screen frame
    frame = pygame.transform.scale(screen, WINDOW_SIZE)
    window.blit(frame, frame.get_rect())

    # Update display
    pygame.display.flip()

    # Limit fps
    dt = clock.tick(30) / 1000

# Quit application
pygame.quit()