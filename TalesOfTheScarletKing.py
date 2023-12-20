import sys
import threading
from os import path
from settings import *
from sprites import *
from tilemap import *
from start_screen import Start_screen
from animations import Animation
from load_level import New_level


class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 1, 2048)
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        self.player_location = GAME_PLAYER_LOC
        self.current_level = FIRST_LEVEL
        self.time = GAME_TIME
        self.time_counter = GAME_TIME_COUNTER, GAME_NIGHT_BRIGHTNES
        self.new_time_counter = self.time_counter

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        font_folder = path.join(game_folder, 'fonts')
        self.map_folder = path.join(game_folder, 'maps')
        self.player_spritesheet = Spritesheet(path.join(img_folder, PLAYER_SPRITESHEET))
        self.title_font = path.join(font_folder, 'Boldhead.otf')

    def loading(self):
        self.load_level = New_level(self, self.screen, self.current_level, self.new_time_counter, self.player_location)
        self.load_level.new()
        self.load_level.run()
        self.current_level = self.load_level.load_next_level()
        self.new_time_counter = self.load_level.load_next_level_time()
        self.player_location = self.load_level.load_next_player_location()

    def run(self):
        self.playing = True
        while self.playing:
            self.loading()
            self.load_level = None

    def show_start_screen(self):
        self.start_screen = Start_screen(self, self.screen)
        self.start_screen.run()
        if self.start_screen.close():
            self.test = False
        else:
            self.test = True


# create the game object
g = Game()
g.show_start_screen()
if g.test:
    run = True
    while run:
        g.run()
