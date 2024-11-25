import asyncio
import math
import sys

import pygame as pg
from player import Player
from sprites.helpers import colour
from sprites.viewport import Viewport
from sprites.world import World

pg.init()
pg.display.set_caption("IRIID")
pg.display.set_mode((640, 640))
clock = pg.time.Clock()


async def main():
    all_sprites = pg.sprite.LayeredUpdates()
    world = World(all_sprites, tiles_x=100, tiles_y=100)
    Player(all_sprites)
    Viewport(all_sprites)

    a = 0

    while True:
        a += 1
        pg.display.update()
        await asyncio.sleep(0)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        all_sprites.update()

        display_surface = pg.display.get_surface()
        display_surface.fill(colour.DARK_GREY)

        # world.set_displacement([(math.sin(a / 100) + 1) * 100, 0])
        world.set_zoom(math.sin(a / 100) + 1)

        all_sprites.draw(display_surface)

        clock.tick(60)


asyncio.run(main())
