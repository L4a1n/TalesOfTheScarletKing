import sys
from os import path
from settings import *
from sprites import *
from tilemap import *
from animations import Animation


class New_level:
    def __init__(self, game, screen, level, time_counter, player_location):
        self.screen = screen
        self.game = game
        self.current_level = level
        self.next_level = ""
        self.player_location = player_location
        self.clock = pg.time.Clock()
        self.time = self.game.time
        self.time_counter = time_counter[0]
        self.night_brightnes = time_counter[1]
        self.load_data(self.current_level)
        self.stats = PLAYER_HEALTH, PLAYER_CURRENT_LEVEL
           ### Muss in der Safe-Datei gespeichert werden

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

    def load_data(self, map):
        self.player_spritesheet = self.game.player_spritesheet
        self.spritesheet = self.game.spritesheet
        self.spritesheet2 = self.game.spritesheet2
        self.spritesheet3 = self.game.spritesheet3
        self.spritesheet4 = self.game.spritesheet4
        self.spritesheet6 = self.game.spritesheet6
        self.title_font = self.game.title_font
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((8, 0, 0, 180))
        self.map = TiledMap(path.join(self.game.map_folder, map))
        self.map_image = self.map.make_map()
        self.map_rect = self.map_image.get_rect()

        self.night = pg.Surface(self.screen.get_size()).convert_alpha()
        self.night.fill((10, 10, 10, self.night_brightnes))

        # Sound loading

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.player_list = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.npcs = pg.sprite.Group()
        self.animation_list = pg.sprite.Group()
        self.spike_list = pg.sprite.Group()
        self.portal_list = pg.sprite.Group()
        self.npc_animations_list = pg.sprite.Group()
        self.effects_list = pg.sprite.Group()

        for group in self.map.tmxdata.objectgroups:

            if group.name == "Obstacles":
                for tile_object in self.map.tmxdata.objects:
                    if tile_object.name == 'wall':
                        Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height,
                                 tile_object.type)

            if group.name == "Portals":
                for tile_object in self.map.tmxdata.objects:
                    if tile_object.name == 'a':
                        Portal(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height,
                                 tile_object.type, tile_object.name)
                    if tile_object.name == 'b':
                        Portal(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height,
                                 tile_object.type, tile_object.name)
                    if tile_object.name == 'c':
                        Portal(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height,
                                 tile_object.type, tile_object.name)

            if group.name == "Entitys":
                for tile_object in self.map.tmxdata.objects:
                    obj_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)
                    if tile_object.name == 'player':
                        if self.player_location == tile_object.type:
                            self.player = Player(self, obj_center.x, obj_center.y)
                    if tile_object.name == 'NPC':
                        NPC(self, obj_center.x, obj_center.y, tile_object.type)

            if group.name == "Animations":
                for tile_object in self.map.tmxdata.objects:
                    if tile_object.name == 'animation':
                        Animation(self, tile_object.x, tile_object.y, tile_object.type)
                    if tile_object.name == 'effect':
                        Effect(self, tile_object.x, tile_object.y, tile_object.type)

        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False
        print(self.player_location)
        # self.effects_sounds['level_start'].play()

    def load_next_level(self):
        return self.next_level

    def load_next_level_time(self):
        return self.time_counter, self.night_brightnes

    def load_next_player_location(self):
        return self.player_location

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        # pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0
            print(self.time_counter)
            print(self.night_brightnes)
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.npc_animations_list.update()
        self.portal_list.update()
        self.camera.update(self.player)

        ##### DAY AND NIGHT
        if self.time_counter < self.time:
            raw = (self.dt / 10) * FPS
            self.time_counter += raw
        else:
            self.time_counter = 0

        if self.time_counter < 303:
            if 302 >= self.time_counter >= 206:
                self.night_brightnes -= 0.2

        if self.time_counter > 790:
            if 890 >= self.time_counter >= 790:
                self.night_brightnes += 0.2

    def draw(self):
        self.screen.fill(RED)
        self.screen.blit(self.map_image, self.camera.apply_rect(self.map_rect))

        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

            if self.draw_debug:
                pg.draw.rect(self.screen, RED, self.camera.apply_rect(sprite.hit_rect), 1)# .convert_alpha()

        for sprite in self.npc_animations_list:
            if sprite.visible == 1:
                self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.night.fill((10, 10, 30, int(self.night_brightnes)))
        self.screen.blit(self.night, (0, 0))

        for effect in self.effects_list:
            effect.update()

        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, RED, self.camera.apply_rect(wall.rect), 1)
            for spike in self.spike_list:
                pg.draw.rect(self.screen, BLUE, self.camera.apply_rect(spike.rect), 1)
            for portal in self.portal_list:
                pg.draw.rect(self.screen, BLUE, self.camera.apply_rect(portal.rect), 1)

        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.title_font, 60, WHITE, (WIDTH/2), (HEIGHT/2), 'center')
        self.draw_text("{:.2f}".format((self.clock.get_fps())), self.title_font, 20, GREEN, 0, 0)
        pg.display.flip()

    def events(self):
        # catch all in-game events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.paused = not self.paused
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_p:
                    self.quit()

                if self.player.on_ground and event.key == pg.K_w:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_w:
                    self.player.jump_cut()
                    self.player.jumping = False
