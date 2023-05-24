import time
import sys
from os import path
from pygame import *
from pygame.locals import *
from time import sleep
from math import *
from random import *
from colorsys import hsv_to_rgb
from dataclasses import dataclass

WIDTH, HEIGHT = 700, 600
g, f = 0.4, -0.08

def change_axis(x, y=None):
    if isinstance(x, Vector):
        return x.x, HEIGHT - x.y
    elif isinstance(x, tuple):
        return x[0], HEIGHT - x[1]
    else:
        return x, HEIGHT - y

@dataclass
class Vector:
    x: int | float
    y: int | float

    def __iter__(self):
        yield self.x
        yield self.y

    def __abs__(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, k):
        if isinstance(k, Vector):
            return self.x * k.x + self.y * k.y
        elif isinstance(k, int) or isinstance(k, float):
            return Vector(self.x * k, self.y * k)

    def __rmul__(self, k: int | float):
        if isinstance(k, Vector):
            return self.x * k.x + self.y * k.y
        elif isinstance(k, int) or isinstance(k, float):
            return Vector(self.x * k, self.y * k)

    def __truediv__(self, k: int | float):
        return Vector(self.x / k, self.y / k)

    def __floordiv__(self, k: int | float):
        return Vector(self.x // k, self.y // k)

    def __mod__(self, k: int | float):
        return Vector(self.x % k, self.y % k)

    def __matmul__(self, other):
        # 2차원 벡터끼리의 크로스곱은 따로 정의되지 않습니다.
        pass

    @staticmethod
    def dist(a, b):
        return sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


class Object(sprite.Sprite):
    def __init__(self, pos: tuple[int, int], mass: int, color=(255, 255, 255)):
        super().__init__()

        self.mass = mass
        self.color = color
        self.s = Vector(*pos)
        self.v = Vector(0, 0)
        self.a = Vector(0, 0)

        self.rect = Rect(*change_axis(self.s), 0, 0)

    def draw(self, screen: Surface):
        pass

    def __str__(self):
        return f"Object(mass={self.mass}, pos={self.s}, vel={self.v}, acc={self.a})"

    def __repr__(self):
        return str(self)

class Circle(Object):
    def __init__(self, pos: tuple[int, int], mass: int, radius: int, color=(255, 255, 255)):
        super().__init__(pos, mass, color=color)

        self.radius = radius
        self.θ = 0
        self.ω = 0
        self.α = 0

        self.rect = Rect(*change_axis(self.s), 2 * self.radius, 2 * self.radius)

    def move(self, platforms, left_key=K_LEFT, right_key=K_RIGHT):
        self.a = Vector(0, -g)

        # for platform in platforms:
        #     if not (platform.left <= self.s.x <= platform.right):
        #         continue
        #
        #     print(platform.top, self.bottom, platform.centery)
        #     if platform.top >= self.bottom >= platform.centery:
        #         print("top")
        #         self.v.y = 0
        #         self.s.y = platform.top + self.radius
        #     elif platform.bottom <= self.top <= platform.centery:
        #         print("bottom")
        #         self.v.y *= -1
        #         self.s.y = platform.bottom - self.radius

        if self.bottom <= 5:
            self.s.y = 5 + self.radius + 1
            self.v.y = 0

        pressed_keys = key.get_pressed()

        if pressed_keys[left_key]:
            self.a.x = -0.5
        if pressed_keys[right_key]:
            self.a.x = +0.5

        self.a.x += self.v.x * f
        self.v += self.a
        self.s += self.v + 0.5 * self.a

        self.α = 0
        self.ω += self.α
        self.θ += self.ω + 0.5 * self.α

    def jump(self, evt_key, jump_key=K_SPACE):
        if evt_key == jump_key:
            self.v.y += 15

    @property
    def I(self):
        return self.mass * self.radius ** 2

    @property
    def τ(self):
        return self.I * self.α

    @property
    def left(self):
        return self.s.x - self.radius

    @property
    def right(self):
        return self.s.x + self.radius

    @property
    def top(self):
        return self.s.y - self.radius

    @property
    def bottom(self):
        return self.s.y + self.radius

    def draw(self, screen: Surface):
        draw.circle(screen, self.color, change_axis(*self.s), self.radius)

    def __str__(self):
        return f"Circle(mass={self.mass}, radius={self.radius}, pos={self.s}, vel={self.v}, acc={self.a})"

    def __repr__(self):
        return str(self)


class Platform(sprite.Sprite):
    def __init__(self, start: tuple[int, int], width=1, thickness=1, color=(255, 255, 255)):
        super().__init__()

        self.color = color
        self.surf = Surface((width, thickness))
        self.surf.fill(color)
        self.rect = self.surf.get_rect(center=change_axis(start[0] + width/2, start[1] - thickness/2))

    def __call__(self, **kwargs):
        x = kwargs.get("x")
        # return self.start.y + (self.end.y - self.start.y) / (self.end.x - self.start.x) * (x - self.start.x)
        return self.rect.top

    @property
    def left(self):
        return self.rect.left

    @property
    def right(self):
        return self.rect.right

    @property
    def top(self):
        return HEIGHT - self.rect.top

    @property
    def bottom(self):
        return HEIGHT - self.rect.bottom

    @property
    def centery(self):
        return HEIGHT - self.rect.centery

    @property
    def centerx(self):
        return self.rect.centerx

    def draw(self, screen: Surface):
        # draw.line(screen, self.color, change_axis(self.start), change_axis(self.end))
        draw.rect(screen, self.color, self.rect)

    def __str__(self):
        return f"Platform{self.rect}"