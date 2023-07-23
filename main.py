from core.game import Game
#from core.level import Level
from core.camera import Camera
from core.drawable import Drawable

from levels import Level0

import pygame
import numpy as np

import random

# Define constants
WINDOW_SIZE = (1280, 800)
VIEW_SIZE = (320, 400)

# Define helpers
def bind_keys(game: Game, camera: Camera):
    
    # Create actions for key_presses
    def player_move_forward():
        camera.move_collide(1., game.get_dt(), level)

    def player_move_backwards():
        camera.move_collide(-1., game.get_dt(), level)

    def player_move_left():
        camera.strafe_collide(-1., game.get_dt(), level)

    def player_move_right():
        camera.strafe_collide(1., game.get_dt(), level)

    def player_turn_left():
        camera.turn(-1., game.get_dt())

    def player_turn_right():
        camera.turn(1., game.get_dt())

    def player_turn_up():
        camera.tilt(1., game.get_dt())

    def player_turn_down():
        camera.tilt(-1., game.get_dt())

    def player_increase_height():
        camera.height += 32 * game.get_dt()

    def player_decrease_height():
        camera.height -= 32 * game.get_dt()

    # Bind actions to keys
    game.bind_key_pressed(pygame.K_w, player_move_forward)
    game.bind_key_pressed(pygame.K_s, player_move_backwards)
    game.bind_key_pressed(pygame.K_a, player_move_left)
    game.bind_key_pressed(pygame.K_d, player_move_right)
    game.bind_key_pressed(pygame.K_LEFT, player_turn_left)
    game.bind_key_pressed(pygame.K_RIGHT, player_turn_right)
    game.bind_key_pressed(pygame.K_UP, player_turn_up)
    game.bind_key_pressed(pygame.K_DOWN, player_turn_down)
    game.bind_key_pressed(pygame.K_LSHIFT, player_increase_height)
    game.bind_key_pressed(pygame.K_LCTRL, player_decrease_height)

    # Bind mouse look
    def game_toggle_enable_mouse():
        game.set_mouse_enabled(not(game.get_mouse_enabled()))

    game.bind_key_down(pygame.K_TAB, game_toggle_enable_mouse)

    def player_look(deltaMouseX, deltaMouseY):
        camera.turn(deltaMouseX / (2*game.get_frame_size()[0]), 1.)
        camera.tilt(-deltaMouseY / game.get_frame_size()[1], 1.)

    game.bind_mouse_move(player_look)

    # Bind misc keys
    def game_toggle_debug_info():
        game.set_debug_enabled(not(game.get_debug_enabled()))

    def game_quit():
        game.quit()

    game.bind_key_down(pygame.K_x, game_toggle_debug_info)
    game.bind_key_down(pygame.K_ESCAPE, game_quit)

# Load a level from the levels folder
level = Level0()

# Create a camera
camera = Camera(position=level.player_start, angle=level.player_start_angle, view_width=VIEW_SIZE[0], view_height=VIEW_SIZE[1])

# Create a game object
game = Game(window_size=WINDOW_SIZE, frame_size=VIEW_SIZE)

# Set level and camera
game.set_level(level)
game.set_camera(camera)

# Bind keys
bind_keys(game, camera)

# Define update function for game
def update(game: Game, dt: float):

    # Do nothing for now
    pass

game.set_update(update)

# Add a custom drawable (a magic lamp that moves to a random place when pressing x)
magic_lamp = Drawable(0, 2, 2.5, 11.5, 32)
game.add_drawable(magic_lamp)
game.set_custom_variable("magic_lamp", magic_lamp)

# Define a function to move magic lamp
def move_magic_lamp():
    # Move magic lamp to a random spot on the level that is not a wall
    while True:
        magic_lamp.x_pos = random.randint(0, game.get_level().get_walls().shape[1] - 1) + 0.5
        magic_lamp.y_pos = random.randint(0, game.get_level().get_walls().shape[0] - 1) + 0.5

        if game.get_level().get_walls()[int(magic_lamp.y_pos - 0.5), int(magic_lamp.x_pos - 0.5), 0] == 0:
            break

# Bind key to move magic lamp
game.bind_key_down(pygame.K_x, move_magic_lamp)

# Run game loop
game.run()