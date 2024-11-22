import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(0, 0))

        self.global_acc = 0.5
        self.global_fric = -0.12

        self.pos = pygame.math.Vector2((0, 0))
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)

    def move(self):
        self.acc = pygame.math.Vector2(0, 0)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_LEFT]:
            self.acc.x = -self.global_acc
        if pressed_keys[pygame.K_RIGHT]:
            self.acc.x = self.global_acc
        if pressed_keys[pygame.K_DOWN]:
            self.acc.y = self.global_acc
        if pressed_keys[pygame.K_UP]:
            self.acc.y = -self.global_acc

        self.acc.x += self.vel.x * self.global_fric
        self.acc.y += self.vel.y * self.global_fric

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
