import pygame

TEXTURE_SIZE = (32, 32)

def load_textures():

    brick_texture_01 = load_texture("textures/brick_texture_01.png")
    brick_texture_02 = load_texture("textures/brick_texture_02.png")
    brick_texture_03 = load_texture("textures/brick_texture_03.png")

    blue_stone = load_texture("textures/wolfenstein_textures/bluestone.png")
    color_stone = load_texture("textures/wolfenstein_textures/colorstone.png")
    grey_stone = load_texture("textures/wolfenstein_textures/greystone.png")
    mossy_stone = load_texture("textures/wolfenstein_textures/mossy.png")
    purple_stone = load_texture("textures/wolfenstein_textures/purplestone.png")
    red_brick = load_texture("textures/wolfenstein_textures/redbrick.png")
    eagle_brick = load_texture("textures/wolfenstein_textures/eagle.png")
    wood = load_texture("textures/wolfenstein_textures/wood.png")

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
        "2": blue,
        "D": blue_stone,
        "E": color_stone,
        "F": grey_stone,
        "G": mossy_stone,
        "H": purple_stone,
        "I": red_brick,
        "J": eagle_brick,
        "K": wood
    }

def load_texture(filename):
    tex = pygame.image.load(filename).convert()
    return pygame.transform.scale(tex, TEXTURE_SIZE)