from dataclasses import dataclass
from pygame import *
from os import path
from math import *

HEIGHT = 700
WIDTH = 1200
ASSETS = path.join(path.dirname(__file__), "assets")
a = 0.5
g = 0.6
f = -0.12
e = 1
PLATFORM_HEIGHT = 40

def arrow(screen, lcolor, tricolor, start, end, trirad, thickness=2):
    rad = pi / 180
    draw.line(screen, lcolor, start, end, thickness)
    rotation = (atan2(start[1] - end[1], end[0] - start[0])) + pi/2
    draw.polygon(screen, tricolor, ((end[0] + trirad * sin(rotation),
                                        end[1] + trirad * cos(rotation)),
                                       (end[0] + trirad * sin(rotation - 120*rad),
                                        end[1] + trirad * cos(rotation - 120*rad)),
                                       (end[0] + trirad * sin(rotation + 120*rad),
                                        end[1] + trirad * cos(rotation + 120*rad))))

class MassPoint(sprite.Sprite):
    def __init__(self, color, mass, pos_x: int, pos_y=385):
        super().__init__()
        self.color = color
        self.mass = mass
        self.radius = (round(log2(mass) + 1) * 13) // 4
        self.font = font.Font(path.join(ASSETS, "font.ttf"), 15 + int(log2(self.mass) / 6))
        self.text = self.font.render(str(self.mass), True, (255, 255, 255))
        self.rect = self.text.get_rect()

        self.pos = Vec(pos_x, pos_y)
        self.vel = Vec(0, 0)
        self.acc = Vec(0, 0)

        self.rect.center = (self.pos.x, self.pos.y)

    def same(self, other):
        return self.mass == other.mass and self.pos == other.pos and self.vel == other.vel and self.acc == other.acc and self.color == other.color and self.radius == other.radius

    def update(self):
        self.text = self.font.render(str(self.mass), True, (255, 255, 255))
        self.rect = self.text.get_rect()
        self.rect.center = (self.pos.x, self.pos.y)

    def move(self, left_key, right_key):
        self.acc = Vec(0, g)

        pressed_keys = key.get_pressed()

        if pressed_keys[left_key]:
            self.acc.x = -a
        elif pressed_keys[right_key]:
            self.acc.x = a

        self.acc.x += self.vel.x * f
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            # self.pos.x = 1
            self.pos.x = WIDTH
            self.vel.x *= -1
        if self.pos.x < 0:
            # self.pos.x = WIDTH - 1
            self.pos.x = 0
            self.vel.x *= -1
        if self.pos.y > HEIGHT - PLATFORM_HEIGHT - self.radius:
            self.pos.y = HEIGHT - PLATFORM_HEIGHT - self.radius + 1
            self.vel.y = 0
        if self.pos.y < 0:
            self.pos.y = 0
            self.vel.y *= -1

    def ishit(self, other, margin=0):
        return self.pos.dist(other.pos) < (self.radius + other.radius) + margin

    def ison(self, platform):
        return self.pos.y >= HEIGHT - platform.surf.get_height() - self.radius

    def jump(self, platform, dots):
        if self.ison(platform):
            self.vel.y -= 15
            return

        for dot in dots:
            if not self.same(dot) and self.ishit(dot, margin=2):
                self.vel.y -= 15
                return
            
    def collision(self, other):
        if self.ishit(other):
            energy_before = self.mass * abs(self.vel) ** 2 / 2 + other.mass * abs(other.vel) ** 2 / 2

            angle = atan2(self.pos.y - other.pos.y, self.pos.x - other.pos.x)
            self.vel = Vec(cos(angle), sin(angle))
            other.vel = Vec(-cos(angle), -sin(angle))

            energy_after = self.mass * abs(self.vel) ** 2 / 2 + other.mass * abs(other.vel) ** 2 / 2

            factor = sqrt(energy_before / energy_after)
            self.vel *= factor
            other.vel *= factor

            collision_vector = self.pos - other.pos
            dist = self.pos.dist(other.pos)
            overlap = (self.radius + other.radius) - dist

            if dist != 0:
                adjust_x = (overlap * collision_vector.x) / dist
                adjust_y = (overlap * collision_vector.y) / dist
            else:
                adjust_x = overlap
                adjust_y = 0

            if self.pos.x < other.pos.x:
                self.pos.x -= adjust_x // 2 + 1
                other.pos.x += adjust_x // 2 + 1
            else:
                self.pos.x += adjust_x // 2 + 1
                other.pos.x -= adjust_x // 2 + 1

            if self.pos.y < other.pos.y:
                self.pos.y -= adjust_y // 2 + 1
                other.pos.y += adjust_y // 2 + 1
            else:
                self.pos.y += adjust_y // 2 + 1
                other.pos.y -= adjust_y // 2 + 1


class Platform(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = Surface((WIDTH, PLATFORM_HEIGHT))
        self.surf.fill((50, 50, 50))
        self.rect = self.surf.get_rect(center=(WIDTH / 2, HEIGHT - PLATFORM_HEIGHT/2))

@dataclass
class Vec:
    x: any
    y: any

    def __abs__(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec(self.x - other.x, self.y - other.y)

    def __mul__(self, k: int | float):
        return Vec(self.x * k, self.y * k)

    def __rmul__(self, k: int | float):
        return Vec(self.x * k, self.y * k)

    def dist(self, other):
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)