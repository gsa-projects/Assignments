from dataclasses import dataclass
from pygame import *
from os import path
from math import *
from random import randint

HEIGHT = 800
WIDTH = 600
PLATFORM_HEIGHT = 20
PLAYER_SIZE = 20
ASSETS = path.join(path.dirname(__file__), "assets")

a = 0.5
g = 0.5
f = -0.08
e = 1

class Player(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.surf.fill((255, 255, 0))
        self.rect = self.surf.get_rect()

        self.pos = Vector2(WIDTH / 2, 600)
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)

    def move(self, left_key, right_key):
        self.acc = Vector2(0, g)

        pressed_keys = key.get_pressed()

        if pressed_keys[left_key]:
            self.acc.x = -a
        elif pressed_keys[right_key]:
            self.acc.x = a

        self.acc.x += self.vel.x * f
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH - self.rect.width:
            self.pos.x = WIDTH - self.rect.width - 1
        if self.pos.x < self.rect.width:
            self.pos.x = self.rect.width + 1
        if self.pos.y > HEIGHT:
            self.pos.y = HEIGHT - 1

        self.rect.midbottom = self.pos

    def update(self, platforms):
        hits = sprite.spritecollide(self, platforms, False)

        if hits:
            if self.pos.y + PLAYER_SIZE >= hits[0].rect.top:
                self.pos.y = hits[0].rect.top + 1
                self.vel.y = 0
            else:
                self.pos.y = hits[0].rect.bottom + 1
                self.vel.y *= -1

    def jump(self, platforms):
        hits = sprite.spritecollide(self, platforms, False)

        if self.pos.y > HEIGHT or hits:
            self.vel.y -= 15


class Platform(sprite.Sprite):
    last = HEIGHT - PLATFORM_HEIGHT / 2

    def __init__(self, width=150, center_x=None):
        super().__init__()
        self.surf = Surface((width, PLATFORM_HEIGHT))
        self.surf.fill((155, 155, 155))
        self.rect = self.surf.get_rect(center=(randint(10, WIDTH - 10) if center_x is None else center_x, Platform.last))
        Platform.last -= 150