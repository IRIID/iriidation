import asyncio
import sys

import pygame as pg
from objects.player import Player
from objects.world import World
from sprites.viewport import Viewport
from ui import colour

pg.init()
pg.display.set_caption("IRIID")
pg.display.set_mode((640, 640))
clock = pg.time.Clock()


async def main():
    # world = World(100, 100)

    all_sprites = pg.sprite.LayeredUpdates()
    Viewport(all_sprites)
    Player(all_sprites)

    while True:
        pg.display.update()
        await asyncio.sleep(0)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        all_sprites.update()

        display_surface = pg.display.get_surface()
        display_surface.fill(colour.DARK_GREY)

        all_sprites.draw(display_surface)

        # pg.display.flip()
        clock.tick(60)


asyncio.run(main())
