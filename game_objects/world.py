import os
import random

import pygame as pg
from utils.layers import LAYERS

TILE_IMG_DIR = "sprites"
PIXEL_SIZE_OF_TILE = 40


class Tile:
    walk_speed_factor = 1.0


class DirtTile(Tile):
    source = os.path.join(TILE_IMG_DIR, "tile_dirt.png")


class GrassTile(Tile):
    walk_speed_factor = 0.6
    source = os.path.join(TILE_IMG_DIR, "tile_grass.png")


class World(pg.sprite.Sprite):
    def __init__(self, tiles_x: int, tiles_y: int):
        super().__init__()
        self._layer = LAYERS["WORLD"]

        self.tiles_x = tiles_x
        self.tiles_y = tiles_y

        self.image = pg.Surface(
            (PIXEL_SIZE_OF_TILE * tiles_x, PIXEL_SIZE_OF_TILE * tiles_y)
        )
        self.rect = self.image.get_rect()

        self.tile_map = self._generate_tile_map(tiles_x, tiles_y)
        self._old_displacement = [0, 0]
        self._displacement = [0, 0]
        self._old_zoom = 1.0
        self._zoom = 1.0

        self._blit_tile_map()

    def set_displacement(self, new_displacement):
        if new_displacement != self._displacement:
            self._displacement = new_displacement

    def set_zoom(self, new_zoom):
        if new_zoom != self._zoom:
            self._zoom = new_zoom

    def update(self):
        if self._displacement[0] != self._old_displacement[0]:
            self.rect.x = self._displacement[0]
            self._old_displacement[0] = self._displacement[0]
        if self._displacement[1] != self._old_displacement[1]:
            self.rect.y = self._displacement[1]
            self._old_displacement[1] = self._displacement[1]
        if self._zoom != self._old_zoom:
            self.image = pg.transform.scale(
                self.image,
                (
                    self._zoom * PIXEL_SIZE_OF_TILE * self.tiles_x,
                    self._zoom * PIXEL_SIZE_OF_TILE * self.tiles_y,
                ),
            )
            self._old_zoom = self._zoom

    def _blit_tile_map(self):
        for y, tile_row in enumerate(self.tile_map):
            for x, tile in enumerate(tile_row):
                self.image.blit(
                    source=pg.image.load(tile.source).convert_alpha(),
                    dest=(x * PIXEL_SIZE_OF_TILE, y * PIXEL_SIZE_OF_TILE),
                )

    def _generate_tile_map(self, tiles_x: int, tiles_y: int) -> list[list[Tile]]:
        return [
            [random.choice(Tile.__subclasses__()) for _ in range(tiles_x)]
            for _ in range(tiles_y)
        ]
