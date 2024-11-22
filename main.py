import asyncio
import sys

import pygame
from objects.player import Player

pygame.init()
pygame.display.set_caption("IRIID")
pygame.display.set_mode((100, 100))
clock = pygame.time.Clock()


async def main():
    p1 = Player()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(p1)

    while True:
        pygame.display.update()
        await asyncio.sleep(0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        display_surface = pygame.display.get_surface()
        display_surface.fill((24, 24, 24))

        p1.move()

        for entity in all_sprites:
            display_surface.blit(entity.surf, entity.rect)

        clock.tick(60)


asyncio.run(main())
