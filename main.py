from game import Game
from level import Level, level0
from camera import Camera

import pygame

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

# Create a level
#level = Level()
level = level0

# Create a camera
camera = Camera(position=level.player_start, angle=level.player_start_angle, view_width=VIEW_SIZE[0], view_height=VIEW_SIZE[1])

# Create a game object
game = Game(window_size=WINDOW_SIZE, frame_size=VIEW_SIZE)

# Set level and camera
game.set_level(level)
game.set_camera(camera)

# Bind keys
bind_keys(game, camera)

# Run game loop
game.run()