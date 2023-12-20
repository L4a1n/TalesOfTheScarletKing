from settings import *


class Button:
    def __init__(self, text, x, y, width, height, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height

    def draw(self, win):
        pg.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pg.font.Font(TITLE_FONT3, 35)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2)
                        - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


class Text:
    def __init__(self, screen, text, font, size, color, x, y):
        self.screen = screen
        self.text = text
        self.font = font
        self.size = size
        self.color = color
        self.rect = (x, y)
        self.font = pg.font.Font(self.font, self.size)
        self.surf_rect = self.font.render(self.text, True, self.color)
        self.align = "tl"

    def set_align(self, align="tl"):
        if align == "tl":
            self.surf_rect.topleft = (self.rect[0], self.rect[1])
        if align == "tr":
            self.surf_rect.topright = (self.rect[0], self.rect[1])
        if align == "bl":
            self.surf_rect.bottomleft = (self.rect[0], self.rect[1])
        if align == "br":
            self.surf_rect.bottomright = (self.rect[0], self.rect[1])
        if align == "mt":
            self.surf_rect.midtop = (self.rect[0], self.rect[1])
        if align == "mb":
            self.surf_rect.midbottom = (self.rect[0], self.rect[1])
        if align == "mr":
            self.surf_rect.midright = (self.rect[0], self.rect[1])
        if align == "ml":
            self.surf_rect.midleft = (self.rect[0], self.rect[1])
        if align == "center":
            self.surf_rect.center = (self.rect[0], self.rect[1])

    def draw(self):
        self.set_align(self.align)