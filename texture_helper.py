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

    err = pygame.Surface(TEXTURE_SIZE)
    err.fill((255, 0, 255))

    '''
    return {
        1: dark_gray,
        2: brick_texture_01,
        3: brick_texture_02,
        4: brick_texture_03,
        5: red,
        6: green,
        7: blue,
        8: blue_stone,
        9: color_stone,
        10: grey_stone,
        11: mossy_stone,
        12: purple_stone,
        13: red_brick,
        14: eagle_brick,
        15: wood,
        0: err
    }
    '''

    return [
        err,
        dark_gray,
        red,
        green,
        blue,
        brick_texture_01,
        brick_texture_02,
        brick_texture_03,
        blue_stone,
        color_stone,
        grey_stone,
        mossy_stone,
        purple_stone,
        red_brick,
        eagle_brick,
        wood
    ]

def load_texture(filename):
    tex = pygame.image.load(filename).convert()
    return pygame.transform.scale(tex, TEXTURE_SIZE)