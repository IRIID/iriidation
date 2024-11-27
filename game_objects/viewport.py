import pygame as pg
from utils.layers import LAYERS


class Viewport(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self._layer = LAYERS["VIEWPORT"]

        window = pg.display.get_surface().get_rect()
        self.image = pg.Surface((window.width, window.height))
        self.image.set_colorkey(pg.Color("white"))

        self.rect = self.image.get_rect()
        self.inner_rect = pg.Rect((40, 40), (window.width - 80, window.height - 80))

    def update(self):
        self.image.fill(pg.Color("black"))
        pg.draw.rect(self.image, pg.Color("white"), self.inner_rect)
