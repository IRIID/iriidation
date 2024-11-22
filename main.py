import asyncio
import sys

import pygame

pygame.init()
pygame.display.set_caption("IRIID")
pygame.display.set_mode((100, 100))
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    acc = 0.5
    fric = -0.12

    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(0, 0))

        self.pos = pygame.math.Vector2((0, 0))
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)

    def move(self):
        self.acc = pygame.math.Vector2(0, 0)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_LEFT]:
            self.acc.x = -Player.acc
        if pressed_keys[pygame.K_RIGHT]:
            self.acc.x = Player.acc
        if pressed_keys[pygame.K_DOWN]:
            self.acc.y = Player.acc
        if pressed_keys[pygame.K_UP]:
            self.acc.y = -Player.acc

        self.acc.x += self.vel.x * Player.fric
        self.acc.y += self.vel.y * Player.fric

        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        window_width, window_height = pygame.display.get_surface().get_size()
        if self.pos.x > window_width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = window_width
        if self.pos.y > window_height:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = window_height

        self.rect.midbottom = self.pos


async def main():
    P1 = Player()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(P1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        display_surface = pygame.display.get_surface()
        display_surface.fill((24, 24, 24))

        P1.move()

        for entity in all_sprites:
            display_surface.blit(entity.surf, entity.rect)

        pygame.display.update()

        asyncio.sleep(0)
        clock.tick(60)


asyncio.run(main())
