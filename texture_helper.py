import pygame

TEXTURE_SIZE = (32, 32)

def load_textures():

    brick_texture_01 = pygame.image.load("textures/brick_texture_01.png").convert()
    brick_texture_02 = pygame.image.load("textures/brick_texture_02.png").convert()
    brick_texture_03 = pygame.image.load("textures/brick_texture_03.png").convert()

    black = pygame.Surface(TEXTURE_SIZE)
    black.fill((0, 0, 0))

    red = pygame.Surface(TEXTURE_SIZE)
    red.fill((255, 0, 0))

    green = pygame.Surface(TEXTURE_SIZE)
    green.fill((0, 255, 0))

    blue = pygame.Surface(TEXTURE_SIZE)
    blue.fill((0, 0, 255))

    dark_gray = pygame.Surface(TEXTURE_SIZE)
    dark_gray.fill((50, 50, 50))

    return {
        "#": dark_gray,
        "A": brick_texture_01,
        "B": brick_texture_02,
        "C": brick_texture_03,
        "0": red,
        "1": green,
        "2": blue
    }