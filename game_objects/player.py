import pygame as pg


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self._layer = 0

        self.image = pg.Surface((40, 40))
        self.image.blit(pg.image.load("sprites/player.png").convert_alpha(), (0, 0))
        self.rect = self.image.get_rect(center=(0, 0))

        self.global_acc = 0.5
        self.global_fric = -0.12

        self.pos = pg.math.Vector2((320, 320))
        self.vel = pg.math.Vector2(0, 0)
        self.acc = pg.math.Vector2(0, 0)

    def update(self):
        self.acc = pg.math.Vector2(0, 0)

        pressed_keys = pg.key.get_pressed()

        if pressed_keys[pg.K_LEFT]:
            self.acc.x = -self.global_acc
        if pressed_keys[pg.K_RIGHT]:
            self.acc.x = self.global_acc
        if pressed_keys[pg.K_DOWN]:
            self.acc.y = self.global_acc
        if pressed_keys[pg.K_UP]:
            self.acc.y = -self.global_acc

        self.acc.x += self.vel.x * self.global_fric
        self.acc.y += self.vel.y * self.global_fric

        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.center = self.pos
