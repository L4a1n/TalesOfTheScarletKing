from settings import *


class Animation(pg.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = type
        self.current_frame = 0
        self.last_update = 0
        self.speed = 350
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = ANIMATION_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)

    def load_images(self):
        if self.type == "player":
            self.package = PLAYER_SPRITES
            self.speed = 300
            self.standing_frames = [
                self.game.player_spritesheet.get_image(self.package[4], self.package[277], self.package[2],self.package[3]),
                self.game.player_spritesheet.get_image(self.package[0], self.package[281], self.package[2],self.package[3]),
                self.game.player_spritesheet.get_image(self.package[0], self.package[285], self.package[2],self.package[3]),
                self.game.player_spritesheet.get_image(self.package[0], self.package[289], self.package[2],self.package[3])]
            for frame in self.standing_frames:
                frame.set_colorkey(BLACK)

        if self.type == "bubbles":
            self.package = SPEECH_BUBLES
            self.standing_frames = [
                self.game.spritesheet3.get_image(self.package[0], self.package[1], self.package[2], self.package[3]),
                self.game.spritesheet3.get_image(self.package[4], self.package[5], self.package[6], self.package[7]),
                self.game.spritesheet3.get_image(self.package[8], self.package[9], self.package[10], self.package[11])]
            for frame in self.standing_frames:
                frame.set_colorkey(BLACK)

    def update(self):
        self.animate()
        self.rect.center = self.hit_rect.center
        self.rect.midtop = self.pos

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.speed:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            self.image = self.standing_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
        self.mask = pg.mask.from_surface(self.image)

    def kill(self):
        return True


class Active_Animation(pg.sprite.DirtySprite):
    def __init__(self, game, x, y, type):
        self._layer = EFFECTS_LAYER
        self.groups = game.npc_animations_list
        pg.sprite.DirtySprite.__init__(self, self.groups)
        self.dirty = 2
        self.visible = 0
        self.game = game
        self.type = type
        self.current_frame = 0
        self.last_update = 0
        self.true = False
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = ANIMATION_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)

    def load_images(self):
        if self.type == "bubbles":
            self.package = SPEECH_BUBLES
            self.standing_frames = [
                self.game.spritesheet3.get_image(self.package[0], self.package[1], self.package[2], self.package[3]),
                self.game.spritesheet3.get_image(self.package[4], self.package[5], self.package[6], self.package[7]),
                self.game.spritesheet3.get_image(self.package[8], self.package[9], self.package[10], self.package[11])]
            for frame in self.standing_frames:
                frame.set_colorkey(BLACK)

    def update(self):
        #if self.true:
        self.animate()
        self.rect.center = self.hit_rect.center
        self.rect.midtop = self.pos

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            self.image = self.standing_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
        self.mask = pg.mask.from_surface(self.image)

    def active(self, test):
        self.true = test
        if self.true == True:
            self.visible = 1
        else:
            self.visible = 0
        return self.true

