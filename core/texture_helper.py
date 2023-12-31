import pygame

TEXTURE_SIZE = (64, 64)

def load_sprite_textures():
    barrel_texture = load_texture("textures/wolfenstein_textures/barrel.png")
    #barrel_texture.set_colorkey((0, 0, 0))

    pillar_texture = load_texture("textures/wolfenstein_textures/pillar.png")
    #pillar_texture.set_colorkey((0, 0, 0))

    greenlight_texture = load_texture("textures/wolfenstein_textures/greenlight.png")
    #greenlight_texture.set_colorkey((0, 0, 0))

    return [
        barrel_texture,     # 0
        pillar_texture,     # 1
        greenlight_texture  # 2
    ]

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

    transparent = pygame.Surface(TEXTURE_SIZE)#.convert_alpha()
    transparent.set_colorkey((0, 0, 0))

    err = pygame.Surface(TEXTURE_SIZE)
    err.fill((255, 0, 255))

    return [
        err,                # 0
        dark_gray,          # 1
        red,                # 2
        green,              # 3
        blue,               # 4
        brick_texture_01,   # 5
        brick_texture_02,   # 6
        brick_texture_03,   # 7
        blue_stone,         # 8
        color_stone,        # 9
        grey_stone,         # 10
        mossy_stone,        # 11
        purple_stone,       # 12
        red_brick,          # 13
        eagle_brick,        # 14
        wood,               # 15
        transparent         # 16
    ]

def load_texture(filename):
    tex = pygame.image.load(filename).convert()
    return pygame.transform.scale(tex, TEXTURE_SIZE)