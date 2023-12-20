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
        if self.type == "grass":
            self.package = GRASS_ANIMATION
            self.standing_frames = [
                self.game.spritesheet2.get_image(self.package[0], self.package[1], self.package[2], self.package[3]),
                self.game.spritesheet2.get_image(self.package[4], self.package[5], self.package[6], self.package[7]),
                self.game.spritesheet2.get_image(self.package[8], self.package[9], self.package[10], self.package[11])]
            for frame in self.standing_frames:
                frame.set_colorkey(BLACK)
        if self.type == "crystal":
            self.package = CRYSTAL_ANIM
            self.standing_frames = [
                self.game.spritesheet4.get_image(self.package[0], self.package[1], self.package[2], self.package[3]),
                self.game.spritesheet4.get_image(self.package[4], self.package[5], self.package[6], self.package[7]),
                self.game.spritesheet4.get_image(self.package[8], self.package[9], self.package[10], self.package[11]),
                self.game.spritesheet4.get_image(self.package[12], self.package[13], self.package[14], self.package[15]),
                self.game.spritesheet4.get_image(self.package[16], self.package[17], self.package[18], self.package[19]),
                self.game.spritesheet4.get_image(self.package[20], self.package[21], self.package[22], self.package[23])]
            for frame in self.standing_frames:
                frame.set_colorkey(BLACK)
        if self.type == "mg_shield":
            self.speed = 50
            self.package = MAGIC_SHIELD_ANIM
            self.standing_frames = [
                self.game.spritesheet4.get_image(self.package[0], self.package[1], self.package[2], self.package[3]),
                self.game.spritesheet4.get_image(self.package[4], self.package[5], self.package[6], self.package[7]),
                self.game.spritesheet4.get_image(self.package[8], self.package[9], self.package[10], self.package[11]),
                self.game.spritesheet4.get_image(self.package[12], self.package[13], self.package[14],self.package[15]),
                self.game.spritesheet4.get_image(self.package[16], self.package[17], self.package[18],self.package[19])]
            for frame in self.standing_frames:
                frame.set_colorkey(BLACK)
        if self.type == "ene_ball":
            self.speed = 70
            self.package = ENERGY_BALL_ANIM
            self.standing_frames = [
                self.game.spritesheet4.get_image(self.package[0], self.package[1], self.package[2], self.package[3]),
                self.game.spritesheet4.get_image(self.package[4], self.package[5], self.package[6], self.package[7]),
                self.game.spritesheet4.get_image(self.package[8], self.package[9], self.package[10], self.package[11]),
                self.game.spritesheet4.get_image(self.package[12], self.package[13], self.package[14], self.package[15]),
                self.game.spritesheet4.get_image(self.package[16], self.package[17], self.package[18], self.package[19]),
                self.game.spritesheet4.get_image(self.package[20], self.package[21], self.package[22], self.package[23]),
                self.game.spritesheet4.get_image(self.package[24], self.package[25], self.package[26], self.package[27]),
                self.game.spritesheet4.get_image(self.package[28], self.package[29], self.package[30], self.package[31]),
                self.game.spritesheet4.get_image(self.package[32], self.package[33], self.package[34], self.package[35])]
            for frame in self.standing_frames:
                frame.set_colorkey(BLACK)
        if self.type == "loading_bat":
            self.speed = 85
            self.package = LOADING_ANIM
            self.standing_frames = [
                self.game.spritesheet5.get_image(self.package[0], self.package[1], self.package[2], self.package[3]),
                self.game.spritesheet5.get_image(self.package[4], self.package[5], self.package[6], self.package[7]),
                self.game.spritesheet5.get_image(self.package[8], self.package[9], self.package[10], self.package[11]),
                self.game.spritesheet5.get_image(self.package[12], self.package[13], self.package[14], self.package[15]),
                self.game.spritesheet5.get_image(self.package[16], self.package[17], self.package[18], self.package[19]),
                self.game.spritesheet5.get_image(self.package[20], self.package[21], self.package[22], self.package[23]),
                self.game.spritesheet5.get_image(self.package[24], self.package[25], self.package[26], self.package[27]),
                self.game.spritesheet5.get_image(self.package[28], self.package[29], self.package[30], self.package[31]),
                self.game.spritesheet5.get_image(self.package[32], self.package[33], self.package[34], self.package[35]),
                self.game.spritesheet5.get_image(self.package[36], self.package[37], self.package[38], self.package[39]),
                self.game.spritesheet5.get_image(self.package[40], self.package[41], self.package[42], self.package[43]),
                self.game.spritesheet5.get_image(self.package[44], self.package[45], self.package[46], self.package[47]),
                self.game.spritesheet5.get_image(self.package[48], self.package[49], self.package[50],self.package[51]),
                self.game.spritesheet5.get_image(self.package[52], self.package[53], self.package[54], self.package[55]),
                self.game.spritesheet5.get_image(self.package[56], self.package[57], self.package[58],self.package[59]),
                self.game.spritesheet5.get_image(self.package[60], self.package[61], self.package[62],self.package[63]),
                self.game.spritesheet5.get_image(self.package[64], self.package[65], self.package[66],self.package[67]),
                self.game.spritesheet5.get_image(self.package[68], self.package[69], self.package[70], self.package[71]),
                self.game.spritesheet5.get_image(self.package[72], self.package[73], self.package[74], self.package[75]),
                self.game.spritesheet5.get_image(self.package[76], self.package[77], self.package[78], self.package[79]),
                self.game.spritesheet5.get_image(self.package[80], self.package[81], self.package[82], self.package[83]),
                self.game.spritesheet5.get_image(self.package[84], self.package[85], self.package[86],self.package[87]),
                self.game.spritesheet5.get_image(self.package[88], self.package[89], self.package[90],self.package[91]),
                self.game.spritesheet5.get_image(self.package[92], self.package[93], self.package[94],self.package[95]),
                self.game.spritesheet5.get_image(self.package[96], self.package[97], self.package[98],self.package[99]),
                self.game.spritesheet5.get_image(self.package[100], self.package[101], self.package[102],self.package[103]),
                self.game.spritesheet5.get_image(self.package[104], self.package[105], self.package[106], self.package[107]),
                self.game.spritesheet5.get_image(self.package[108], self.package[109], self.package[110], self.package[111]),
                self.game.spritesheet5.get_image(self.package[112], self.package[113], self.package[114], self.package[115]),
                self.game.spritesheet5.get_image(self.package[116], self.package[117], self.package[118], self.package[119]),
                self.game.spritesheet5.get_image(self.package[120], self.package[121], self.package[122], self.package[123]),
                self.game.spritesheet5.get_image(self.package[124], self.package[125], self.package[126], self.package[127])]
            for frame in self.standing_frames:
                frame.set_colorkey(BLACK)

        if self.type == "flame_anim":
            self.speed = 70
            self.package = FLAMES_ANIM
            self.standing_frames = [
                self.game.spritesheet6.get_image(self.package[0], self.package[1], self.package[2],self.package[3]),
                self.game.spritesheet6.get_image(self.package[4], self.package[5], self.package[6],self.package[7]),
                self.game.spritesheet6.get_image(self.package[8], self.package[9], self.package[10],self.package[11]),
                self.game.spritesheet6.get_image(self.package[12], self.package[13], self.package[14],self.package[15]),
                self.game.spritesheet6.get_image(self.package[16], self.package[17], self.package[18],self.package[19]),
                self.game.spritesheet6.get_image(self.package[20], self.package[21], self.package[22],self.package[23]),
                self.game.spritesheet6.get_image(self.package[24], self.package[25], self.package[26],self.package[27]),
                self.game.spritesheet6.get_image(self.package[28], self.package[29], self.package[30],self.package[31]),
                self.game.spritesheet6.get_image(self.package[32], self.package[33], self.package[34],self.package[35]),
                self.game.spritesheet6.get_image(self.package[36], self.package[37], self.package[38],self.package[39]),
                self.game.spritesheet6.get_image(self.package[40], self.package[41], self.package[42],self.package[43]),
                self.game.spritesheet6.get_image(self.package[44], self.package[45], self.package[46],self.package[47]),
                self.game.spritesheet6.get_image(self.package[48], self.package[49], self.package[50],self.package[51]),
                self.game.spritesheet6.get_image(self.package[52], self.package[53], self.package[54],self.package[55]),
                self.game.spritesheet6.get_image(self.package[56], self.package[57], self.package[58],self.package[59]),
                self.game.spritesheet6.get_image(self.package[60], self.package[61], self.package[62],self.package[63]),
                self.game.spritesheet6.get_image(self.package[64], self.package[65], self.package[66],self.package[67]),
                self.game.spritesheet6.get_image(self.package[68], self.package[69], self.package[70],self.package[71])]
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

