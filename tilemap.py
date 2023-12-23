from settings import *
import pytmx


def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)


class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelapha=True)
        self.width = (tm.width * tm.tilewidth)
        self.height = (tm.height * tm.tileheight)
        print(self.width, self.height)
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface


class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.offset_x = 0
        self.offset_y = 0
        self.x = 0
        self.y = 0
        self.vel = 0

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def camera_shake(self):
        pass

    def update(self, target):

        target_x = -target.rect.centerx + int(WIDTH / 2)
        target_y = -target.rect.centery + int(HEIGHT / 2)
        #self.x = -target.rect.centerx + int(WIDTH / 2)
        #self.y = -target.rect.centery + int(HEIGHT / 2)

        if self.x > target_x:
            self.x -= (self.x - target_x)/15
        elif self.x < target_x:
            self.x += (target_x - self.x)/15

        if self.y > target_y:
            self.y -= (self.y - target_y)/15
        elif self.y < target_y:
            self.y += (target_y - self.y)/15

        # limit scrolling to map size
        self.x = min(0, self.x)  # left
        self.y = min(0, self.y)  # top
        self.x = max(-(self.width - WIDTH), self.x)  # right
        self.y = max(-(self.height - HEIGHT), self.y)  # bottom
        self.camera = pg.Rect(self.x, self.y, self.width, self.height)
        self.offset_x = -self.x
        self.offset_y = -self.y
