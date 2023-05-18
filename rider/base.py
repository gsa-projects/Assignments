from pygame import *
from os import path

HEIGHT = 600
WIDTH = 1200
ACC = 0.5
FRIC = -0.12
ASSETS = path.join(path.dirname(__file__), "assets")


class Player(sprite.Sprite):
    def __init__(self):
        super().__init__()
        # self.surf = image.load(path.join(ASSETS, "rider.png"))
        self.surf = Surface((30, 30))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect(center=(30, HEIGHT - 30))

        self.pos = Vector2(10, 385)
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)

    def move(self):
        self.acc = Vector2(0, 0)

        pressed_keys = key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos


class Platform(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = Surface((WIDTH, 20))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center=(WIDTH / 2, HEIGHT - 10))
