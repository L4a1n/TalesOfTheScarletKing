from settings import *
import random
from tilemap import collide_hit_rect
from animations import Active_Animation
vec = pg.math.Vector2
all_animations = []


class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
        self.scale = SPRITE_SCALE

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (int(width * self.scale), int(height * self.scale)))
        return image


class collide_walls:
    def __init__(self, sprite, group):
        self.X = False
        self.Y = False
        self.sprite = sprite
        self.group = group

    def collide(self, dir):
        self.dir = dir
        if self.dir == 'x':
            hits = pg.sprite.spritecollide(self.sprite, self.group, False, collide_hit_rect)
            if hits:
                if hits[0].rect.centerx > self.sprite.hit_rect.centerx:
                    self.sprite.pos.x = hits[0].rect.left - self.sprite.hit_rect.width / 2.0
                if hits[0].rect.centerx < self.sprite.hit_rect.centerx:
                    self.sprite.pos.x = hits[0].rect.right + self.sprite.hit_rect.width / 2.0
                self.sprite.vel.x = 0
                self.sprite.hit_rect.centerx = self.sprite.pos.x
                self.X = True
            else:
                self.X = False
        if self.dir == 'y':
            hits = pg.sprite.spritecollide(self.sprite, self.group, False, collide_hit_rect)
            if hits:

                if hits[0].rect.centery > self.sprite.hit_rect.centery:
                    self.sprite.pos.y = hits[0].rect.top - self.sprite.hit_rect.height / 2.0
                if hits[0].rect.centery < self.sprite.hit_rect.centery:
                    self.sprite.pos.y = hits[0].rect.bottom + self.sprite.hit_rect.height / 2.0
                self.sprite.vel.y = 0
                self.sprite.hit_rect.centery = self.sprite.pos.y
                self.Y = True
            else:
                self.Y = False

    def collide_single(self, dir):
        self.dir = dir
        if self.dir == 'x':
            hits = pg.sprite.spritecollide(self.sprite, self.group, False, collide_hit_rect)
            if hits:
                self.X = True
            else:
                self.X = False
        if self.dir == 'y':
            hits = pg.sprite.spritecollide(self.sprite, self.group, False, collide_hit_rect)
            if hits:
                self.Y = True
            else:
                self.Y = False


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites, game.player_list
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.frozen = False
        self.walking = False
        self.jumping = False
        self.falling = False
        self.attack_count = 0
        self.attacking = False
        self.air_attacking = False
        self.on_ground = True
        self.crouch = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.anim_idle1_r[0]
        self.rect = self.image.get_rect()
        print("player_hitbox: ", self.rect)
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.bottom = self.rect.bottom
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        try:
            self.collider = collide_walls(self, self.game.walls)
            self.spike_collider = collide_walls(self, self.game.spike_list)
            self.converation = collide_walls(self, self.game.npcs)
        except:
            print("Error - Player: import colliders")

    def set_frozen(self, x):
        self.frozen = x

    def change_char(self, x, y, type):
        self.pos = vec(x, y)
        self.type = type
        self.load_images()

    def return_stat(self):
        i = [self.pos[0], self.pos[1], self.type]
        return i

    def return_char(self):
        return self.type

    def load_images(self):
        self.package = PLAYER_SPRITES

        self.anim_air_attack_1_r = [
            self.game.player_spritesheet.get_image(self.package[0], self.package[1], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[4], self.package[5], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[9], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[4], self.package[13], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[17], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[4], self.package[21], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[25], self.package[2], self.package[3])]
        print("lolol:  ", self.package[25])
        self.anim_air_attack_1_l = []
        for frame in self.anim_air_attack_1_r:
            frame.set_colorkey(BLACK)
            self.anim_air_attack_1_l.append(pg.transform.flip(frame, True, False))

        self.anim_air_attack_2_end = [
            self.game.player_spritesheet.get_image(self.package[0], self.package[49], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[4], self.package[29], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[33], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[4], self.package[37], self.package[2], self.package[3])]
        self.anim_air_attack_2_l = []
        for frame in self.anim_air_attack_2_end:
            frame.set_colorkey(BLACK)
            self.anim_air_attack_2_l.append(pg.transform.flip(frame, True, False))

        self.anim_air_attack_2_loop_r = [
            self.game.player_spritesheet.get_image(self.package[4], self.package[41], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[45], self.package[2], self.package[3])]
        self.anim_air_attack_2_loop_l = []
        for frame in self.anim_air_attack_2_loop_r:
            frame.set_colorkey(BLACK)
            self.anim_air_attack_2_loop_l.append(pg.transform.flip(frame, True, False))

        self.anim_attack_r = [
            self.game.player_spritesheet.get_image(self.package[4], self.package[53], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[57], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[4], self.package[61], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[65], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[4], self.package[69], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[4], self.package[73], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[77], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[4], self.package[81], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[85], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[4], self.package[89], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[93], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[4], self.package[97], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[101], self.package[2],self.package[3]),
            self.game.player_spritesheet.get_image(self.package[4], self.package[105], self.package[2],self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[109], self.package[2],self.package[3]),
            self.game.player_spritesheet.get_image(self.package[4], self.package[113], self.package[2],self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[117], self.package[2], self.package[3])]
        self.anim_attack_l = []
        for frame in self.anim_attack_r:
            frame.set_colorkey(BLACK)
            self.anim_attack_l.append(pg.transform.flip(frame, True, False))


        self.anim_cast_r = [
            self.game.player_spritesheet.get_image(self.package[4], self.package[121], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[125], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[4], self.package[129], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[133], self.package[2], self.package[3])]
        self.anim_cast_l = []
        for frame in self.anim_cast_r:
            frame.set_colorkey(BLACK)
            self.anim_cast_l.append(pg.transform.flip(frame, True, False))


        self.anim_cast_loop_r = [
            self.game.player_spritesheet.get_image(self.package[4], self.package[137], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[141], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[4], self.package[145], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[149], self.package[2], self.package[3])]
        self.anim_cast_loop_l = []
        for frame in self.anim_cast_loop_r:
            frame.set_colorkey(BLACK)
            self.anim_cast_loop_l.append(pg.transform.flip(frame, True, False))



        self.anim_crnr_climb_r = [
            self.game.player_spritesheet.get_image(self.package[4], self.package[153], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[157], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[4], self.package[161], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[165], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[169], self.package[2], self.package[3])]
        self.anim_crnr_climb_l = []
        for frame in self.anim_crnr_climb_r:
            frame.set_colorkey(BLACK)
            self.anim_crnr_climb_l.append(pg.transform.flip(frame, True, False))


        self.anim_crnr_gbr_r = [
            self.game.player_spritesheet.get_image(self.package[4], self.package[173], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[177], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[4], self.package[181], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[185], self.package[2], self.package[3])]
        self.anim_crnr_gbr_l = []
        for frame in self.anim_crnr_gbr_r:
            frame.set_colorkey(BLACK)
            self.anim_crnr_gbr_l.append(pg.transform.flip(frame, True, False))


        self.anim_crnr_jump_r = [
            self.game.player_spritesheet.get_image(self.package[4], self.package[189], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[193], self.package[2], self.package[3])]
        self.anim_crnr_jump_l = []
        for frame in self.anim_crnr_jump_r:
            frame.set_colorkey(BLACK)
            self.anim_crnr_jump_l.append(pg.transform.flip(frame, True, False))


        self.anim_crouch_r = [
            self.game.player_spritesheet.get_image(self.package[4], self.package[197], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[201], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[4], self.package[205], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[209], self.package[2], self.package[3])]
        self.anim_crouch_l = []
        for frame in self.anim_crouch_r:
            frame.set_colorkey(BLACK)
            self.anim_crouch_l.append(pg.transform.flip(frame, True, False))



        self.anim_die_r = [
            self.game.player_spritesheet.get_image(self.package[4], self.package[213], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[217], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[4], self.package[221], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[225], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[229], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[4], self.package[233], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[237], self.package[2], self.package[3])]
        self.anim_die_l = []
        for frame in self.anim_die_r:
            frame.set_colorkey(BLACK)
            self.anim_die_l.append(pg.transform.flip(frame, True, False))


        self.anim_fall_r = [
            self.game.player_spritesheet.get_image(self.package[4], self.package[241], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[245], self.package[2], self.package[3])]
        self.anim_fall_l = []
        for frame in self.anim_fall_r:
            frame.set_colorkey(BLACK)
            self.anim_fall_l.append(pg.transform.flip(frame, True, False))


        self.anim_hurt_r = [
            self.game.player_spritesheet.get_image(self.package[4], self.package[249], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[253], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[257], self.package[2], self.package[3])]
        self.anim_hurt_l = []
        for frame in self.anim_hurt_r:
            frame.set_colorkey(BLACK)
            self.anim_hurt_l.append(pg.transform.flip(frame, True, False))


        self.anim_idle1_r = [
            self.game.player_spritesheet.get_image(self.package[4], self.package[261], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[265], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[269], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[273], self.package[2], self.package[3])]
        self.anim_idle1_l = []
        for frame in self.anim_idle1_r:
            frame.set_colorkey(BLACK)
            self.anim_idle1_l.append(pg.transform.flip(frame, True, False))


        self.anim_idle2_r = [
            self.game.player_spritesheet.get_image(self.package[4], self.package[277], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[281], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[285], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[289], self.package[2], self.package[3])]
        self.anim_idle2_l = []
        for frame in self.anim_idle2_r:
            frame.set_colorkey(BLACK)
            self.anim_idle2_l.append(pg.transform.flip(frame, True, False))


        self.anim_items_r = [
            self.game.player_spritesheet.get_image(self.package[4], self.package[293], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[297], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[301], self.package[2], self.package[3])]
        self.anim_items_l = []
        for frame in self.anim_items_r:
            frame.set_colorkey(BLACK)
            self.anim_items_l.append(pg.transform.flip(frame, True, False))


        self.anim_jump_r = [
            #self.game.player_spritesheet.get_image(self.package[4], self.package[305], self.package[2], self.package[3]),
            #self.game.player_spritesheet.get_image(self.package[0], self.package[309], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[313], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[317], self.package[2], self.package[3])]
        self.anim_jump_l = []
        for frame in self.anim_jump_r:
            frame.set_colorkey(BLACK)
            self.anim_jump_l.append(pg.transform.flip(frame, True, False))


        self.anim_run_r = [
            self.game.player_spritesheet.get_image(self.package[4], self.package[321], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[325], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[329], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[333], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[337], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[341], self.package[2], self.package[3])]
        self.anim_run_l = []
        for frame in self.anim_run_r:
            frame.set_colorkey(BLACK)
            self.anim_run_l.append(pg.transform.flip(frame, True, False))


        self.anim_slide_r = [
            self.game.player_spritesheet.get_image(self.package[4], self.package[345], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[349], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[4], self.package[353], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[4], self.package[357], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[361], self.package[2], self.package[3])]
        self.anim_slide_l = []
        for frame in self.anim_slide_r:
            frame.set_colorkey(BLACK)
            self.anim_slide_l.append(pg.transform.flip(frame, True, False))


        self.anim_swrd_drw_r = [
            self.game.player_spritesheet.get_image(self.package[4], self.package[365], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[369], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[373], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[377], self.package[2], self.package[3])]
        self.anim_swrd_drw_l = []
        for frame in self.anim_swrd_drw_r:
            frame.set_colorkey(BLACK)
            self.anim_swrd_drw_l.append(pg.transform.flip(frame, True, False))


        self.anim_swrd_shte_r = [
            self.game.player_spritesheet.get_image(self.package[4], self.package[381], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[385], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[389], self.package[2], self.package[3]),
            self.game.player_spritesheet.get_image(self.package[0], self.package[393], self.package[2], self.package[3])]
        self.anim_swrd_shte_l = []
        for frame in self.anim_swrd_shte_r:
            frame.set_colorkey(BLACK)
            self.anim_swrd_shte_l.append(pg.transform.flip(frame, True, False))

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def jump(self):
        # jump only if standing on a platform
        self.rect.y += 2
        self.rect.y -= 2
        if not self.jumping:
            # self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP

    def attack(self):
        pass

    def update(self):
        pg.key.set_repeat(40000)
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_SPACE] and self.on_ground:
            self.acc.x += self.vel.x * (PLAYER_FRICTION)*2.2
            self.attacking = True
        else:
            self.attacking = False
        if keys[pg.K_SPACE] and not self.on_ground:
            self.air_attacking = True
        else:
            self.air_attacking = False
        if keys[pg.K_s] and not self.walking:
            self.crouch = True
            self.acc.x += self.vel.x * (PLAYER_FRICTION) * 2.2
            #self.hit_rect = PLAYER_HIT_RECT_CROUCH
        elif keys[pg.K_s] and self.walking:
            self.crouch = True
            self.acc.x += self.vel.x * (PLAYER_FRICTION) * 2.2
            #self.hit_rect = PLAYER_HIT_RECT_SLIDE
        else:
            self.crouch = False
            #self.hit_rect = PLAYER_HIT_RECT
        self.on_ground = self.collider.Y
        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        self.hit_rect.centerx = self.pos.x
        self.converation.collide_single('x')
        self.converation.collide_single('y')
        if self.converation.X or self.converation.Y:
            if keys[pg.K_SPACE]:
                # interact
                pass
        self.collider.collide('x')
        self.spike_collider.collide('X')
        self.hit_rect.centery = self.pos.y
        self.collider.collide('y')
        self.spike_collider.collide('y')
        if self.spike_collider.Y:
            self.jumping = False
            self.jump()
        self.rect.center = self.hit_rect.center


    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        # show slide animation
        if self.crouch and self.walking:
            if now - self.last_update > 270:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.anim_slide_l)
                bottom = self.rect.bottom
                if self.vel.x < 0:
                    self.image = self.anim_slide_l[self.current_frame]
                else:
                    self.image = self.anim_slide_r[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # show crouch animation
        if self.crouch and not self.walking:
            if now - self.last_update > 270:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.anim_crouch_l)
                bottom = self.rect.bottom
                if self.vel.x < 0:
                    self.image = self.anim_crouch_l[self.current_frame]
                else:
                    self.image = self.anim_crouch_r[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # show walk animation
        if self.walking and self.on_ground and not self.jumping and not self.attacking and not self.crouch:
            if now - self.last_update > 40:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.anim_run_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.anim_run_r[self.current_frame]
                else:
                    self.image = self.anim_run_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # show attack animation
        if self.attacking:
            if now - self.last_update > 150:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.anim_attack_l)
                bottom = self.rect.bottom
                if self.vel.x < 0:
                    self.image = self.anim_attack_l[self.current_frame]
                else:
                    self.image = self.anim_attack_r[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # show air_attack animation
        if self.air_attacking:
            if now - self.last_update > 150:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.anim_air_attack_1_l)
                bottom = self.rect.bottom
                if self.vel.x < 0:
                    self.image = self.anim_air_attack_1_l[self.current_frame]
                else:
                    self.image = self.anim_air_attack_1_r[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # show jump animation
        if self.jumping:
            if now - self.last_update > 220:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.anim_jump_l)
                bottom = self.rect.bottom
                if self.vel.x < 0:
                    self.image = self.anim_jump_l[self.current_frame]
                else:
                    self.image = self.anim_jump_r[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # show falling animation
        if not self.jumping and not self.on_ground:
            if now - self.last_update > 60:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.anim_fall_l)
                bottom = self.rect.bottom
                if self.vel.x < 0:
                    self.image = self.anim_fall_l[self.current_frame]
                else:
                    self.image = self.anim_fall_r[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # show idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 270:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.anim_idle1_r)
                bottom = self.rect.bottom
                self.image = self.anim_idle1_r[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        self.mask = pg.mask.from_surface(self.image)


class NPC(pg.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.npcs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = type
        self.walking = False
        self.jumping = False
        self.on_ground = False
        self.is_talking = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.collider = collide_walls(self, self.game.walls)
        self.conversation = collide_walls(self, self.game.player_list)
        self.bla = Active_Animation(self.game, self.hit_rect.x, self.hit_rect.y - 20, "bubbles")

    def load_images(self):
        if 'green' in self.type:
            self.package = NPC_GREEN
        if 'grey' in self.type:
            self.package = NPC_GREY
        if 'red' in self.type:
            self.package = NPC_RED
        if 'blue' in self.type:
            self.package = NPC_BLUE
        self.standing_frames = [self.game.spritesheet.get_image(self.package[0], self.package[1], self.package[2], self.package[3])]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)

        self.walk_frames_r = [self.game.spritesheet.get_image(self.package[4], self.package[5], self.package[6], self.package[7]),
                                self.game.spritesheet.get_image(self.package[8], self.package[9], self.package[10], self.package[11]),
                                self.game.spritesheet.get_image(self.package[12], self.package[13], self.package[14], self.package[15])]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        self.jump_frames_r = [self.game.spritesheet.get_image(self.package[16], self.package[17], self.package[18], self.package[19]),
                            self.game.spritesheet.get_image(self.package[20], self.package[21], self.package[22], self.package[23])]
        self.jump_frames_l = []
        for frame in self.jump_frames_r:
            frame.set_colorkey(BLACK)
            self.jump_frames_l.append(pg.transform.flip(frame, True, False))

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def jump(self):
        # jump only if standing on a platform
        self.rect.y += 2
        self.rect.y -= 2
        if not self.jumping:
            # self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = -NPC_JUMP

    def update(self):
        self.animate()
        self.bla.pos = vec(self.hit_rect.x, self.hit_rect.y -20)
        self.keys = pg.key.get_pressed()
        self.acc = vec(0, NPC_GRAV)
        self.on_ground = self.collider.X or self.collider.Y
        # apply friction
        self.acc.x += self.vel.x * NPC_FRICTION
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc

        self.conversation.collide_single('x')
        if self.conversation.X:
            self.bla.active(True)
            self.is_talking = True
            if self.keys[pg.K_SPACE]:
                i = self.game.player.return_stat()
                self.game.player.change_char(self.pos[0], self.pos[1], self.type)
                self.pos = vec(i[0], i[1])
                self.type = i[2]
                self.load_images()
        else:
            self.bla.active(False)
            self.is_talking = False

        self.hit_rect.centerx = self.pos.x
        self.collider.collide('x')
        self.hit_rect.centery = self.pos.y
        self.collider.collide('y')
        self.rect.center = self.hit_rect.center

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        # show walk animation
        if self.walking and not self.jumping:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        if self.jumping and self.walking:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.jump_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.jump_frames_r[self.current_frame]
                else:
                    self.image = self.jump_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        # show idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        self.mask = pg.mask.from_surface(self.image)


class Attack(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, type):
        self.type = type
        self.game = game
        self.groups = self.game.hit_boxes_list
        pg.sprite.Sprite.__init__(self, self.groups)
        self.rect = pg.Rect(x, y, w, h)


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, type):
        self.type = type
        if self.type == 'spikes':
            self.groups = game.spike_list
        else:
            self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


class Effect(pg.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self.groups = game.effects_list
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x, self.y = x, y
        self.type = type
        self.particles = []

    def update(self):
        self.particles.append([[self.x, self.y], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 6)])

        for particle in self.particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.1
            particle[1][1] += 0.1
            pg.draw.circle(self.game.screen, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                self.particles.remove(particle)


class Portal(pg.sprite.DirtySprite):
    def __init__(self, game, x, y, w, h, type, name):
        self.groups = game.portal_list
        pg.sprite.Sprite.__init__(self, self.groups)
        self.dirty = 1
        self.visible = 0
        self.name = name
        self.type = type
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.surface = pg.Surface((self.rect[2], self.rect[3]))
        self.surface.fill(BLACK)
        self.rect.x = x
        self.rect.y = y
        self.collide = collide_walls(self, self.game.player_list)
        self.active = False

    def get_name(self):
        return self.name

    def update(self):

        self.collide.collide_single('x')
        if self.collide.X:
            self.active = True
        self.collide.collide_single('y')
        if self.collide.Y:
            self.active = True
        if self.active:
            self.game.next_level = self.type
            self.game.player_location = self.name
            self.game.playing = False
