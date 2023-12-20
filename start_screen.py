from settings import *
from classes import *
from tilemap import *
from sprites import Player
from animations import *


class Start_screen:
    def __init__(self, game, screen):
        self.screen = screen
        self.game = game
        self.running = True
        self.closing = 0
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        self.camera = Camera(WIDTH, HEIGHT)
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.player_list = pg.sprite.Group()
        self.player_spritesheet = self.game.player_spritesheet
        self.spritesheet3 = self.game.spritesheet3
        self.bg_color = (17, 17, 17)
        self.bg_img = pg.image.load("img/bg_img_1.png").convert_alpha()
        self.bg_img = pg.transform.scale(self.bg_img, (1100, 1100))
        self.start_button = Button("Start", 250, 400, 150, 70, (17, 17, 17))
        self.quit_button = Button("Quit", 250, 540, 150, 70, (17, 17, 17))
        self.anim = Animation(self, 1160, 310, "player")

    def close(self):
        if self.closing == 1:
            self.running = False
            return self.closing

    def events(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.running = False

                if event.key == pg.K_ESCAPE:
                    self.closing = 1
                    self.running = False

        self.mouse = pg.mouse.get_pos()
        self.click = pg.mouse.get_pressed()
        self.start = self.start_button.click((self.mouse[0], self.mouse[1]))
        self.quit = self.quit_button.click((self.mouse[0], self.mouse[1]))

    def update(self):
        self.all_sprites.update()
        if self.start and self.click[0] >= 1:
            self.running = False
        if self.quit and self.click[0] >= 1:
            self.closing = 1
            self.running = False

    def draw(self):
        self.screen.fill(self.bg_color)
        self.screen.blit(self.bg_img, (600, 0))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.start_button.draw(self.screen)
        self.quit_button.draw(self.screen)

        pg.display.update()

    def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.events()
            self.update()
            self.draw()