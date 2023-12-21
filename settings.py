import pygame as pg
import time
from os import path
vec = pg.math.Vector2
import screeninfo

pg.init()

# some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
NIGHT = (15, 15, 30, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BROWN = (106, 55, 5)

# game settings
main_monitor = None
try:
    monitors = screeninfo.get_monitors()
    if monitors:
        main_monitor = next((e for e in monitors if e.is_primary), monitors[0])
        if main_monitor.is_primary:
            print(f'Using primary monitor: {main_monitor}')
        else:
            print('No primary monitor found, using first monitor instead')
except:
    print('No monitors found')
WIDTH, HEIGHT = main_monitor.x, main_monitor.y

FPS = 60
GAME_PLAYER_LOC = "a"
TITLE = "Tales of the Scarlet King"
BGCOLOR = (0, 0, 120)
FIRST_LEVEL = 'lvl_1.tmx'
game_folder = path.dirname(__file__)
font_folder = path.join(game_folder, 'fonts')
TITLE_FONT = path.join(font_folder, 'Boldhead.otf')
TITLE_FONT2 = path.join(font_folder, 'ka1.ttf')
TITLE_FONT3 = path.join(font_folder, 'origa___.ttf')
TITLE_FONT4 = path.join(font_folder, 'origap__.ttf')
rec_folder = path.join(game_folder, 'rec')
START_VID = path.join(rec_folder, 'start_vid.mp4')


# player settings
PLAYER_HIT_RECT = pg.Rect(0, 0, 60, 150)
PLAYER_HIT_RECT_CROUCH = pg.Rect(0, 0, 60, 60)
PLAYER_HIT_RECT_SLIDE = pg.Rect(0, 0, 60, 45)
ANIMATION_HIT_RECT = pg.Rect(0, 0, 32, 32)
PLAYER_ACC = 0.9
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 28
PLAYER_HEALTH = 100
PLAYER_CURRENT_LEVEL = 'lvl_1.tmx'

# NPC settings
NPC_ACC = 0.9
NPC_FRICTION = -0.12
NPC_GRAV = 0.8
NPC_JUMP = 20

# ANIMATION_CONFIGURATION
ANIMATION_CONFIG_1 = 50, 50

# Layer sorting
WALL_LAYER = 1
PLAYER_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# Spritesheets
SPRITE_SCALE = 4.5
PLAYER_SPRITESHEET = "Player_sheet_1.png"

# Spritesheet xml

PLAYER_SPRITES = [0, 0, 50, 37, 50, 0, 50, 37, 0, 37, 50, 37, 50, 37, 50, 37, 0, 74, 50, 37, 50, 74, 50, 37, 0, 111, 50,
                  37, 50, 111, 50, 37, 0, 148, 50, 37, 50, 148, 50, 37, 0, 185, 50, 37, 50, 185, 50, 37, 0, 222, 50, 37,
                  50, 222, 50, 37, 0, 259, 50, 37, 50, 259, 50, 37, 0, 296, 50, 37, 50, 296, 50, 37, 0, 333, 50, 37, 50,
                  333, 50, 37, 0, 370, 50, 37, 50, 370, 50, 37, 0, 407, 50, 37, 50, 407, 50, 37, 0, 444, 50, 37, 50, 444,
                  50, 37, 0, 481, 50, 37, 50, 481, 50, 37, 0, 518, 50, 37, 50, 518, 50, 37, 0, 555, 50, 37, 50, 555, 50,
                  37, 0, 592, 50, 37, 50, 592, 50, 37, 0, 629, 50, 37, 50, 629, 50, 37, 0, 666, 50, 37, 50, 666, 50, 37,
                  0, 703, 50, 37, 50, 703, 50, 37, 0, 740, 50, 37, 50, 740, 50, 37, 0, 777, 50, 37, 50, 777, 50, 37, 0,
                  814, 50, 37, 50, 814, 50, 37, 0, 851, 50, 37, 50, 851, 50, 37, 0, 888, 50, 37, 50, 888, 50, 37, 0, 925,
                  50, 37, 50, 925, 50, 37, 0, 962, 50, 37, 50, 962, 50, 37, 0, 999, 50, 37, 50, 999, 50, 37, 0, 1036, 50,
                  37, 50, 1036, 50, 37, 0, 1073, 50, 37, 50, 1073, 50, 37, 0, 1110, 50, 37, 50, 1110, 50, 37, 0, 1147, 50,
                  37, 50, 1147, 50, 37, 0, 1184, 50, 37, 50, 1184, 50, 37, 0, 1221, 50, 37, 50, 1221, 50, 37, 0, 1258, 50,
                  37, 50, 1258, 50, 37, 0, 1295, 50, 37, 50, 1295, 50, 37, 0, 1332, 50, 37, 50, 1332, 50, 37, 0, 1369, 50,
                  37, 50, 1369, 50, 37, 0, 1406, 50, 37, 50, 1406, 50, 37, 0, 1443, 50, 37, 50, 1443, 50, 37, 0, 1480, 50,
                  37, 50, 1480, 50, 37, 0, 1517, 50, 37, 50, 1517, 50, 37, 0, 1554, 50, 37, 50, 1554, 50, 37, 0, 1591, 50,
                  37, 50, 1591, 50, 37, 0, 1628, 50, 37, 50, 1628, 50, 37, 0, 1665, 50, 37, 50, 1665, 50, 37, 0, 1702, 50,
                  37, 50, 1702, 50, 37, 0, 1739, 50, 37, 50, 1739, 50, 37, 0, 1776, 50, 37, 50, 1776, 50, 37, 0, 1813, 50,
                  37]

