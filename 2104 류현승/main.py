from pygame import *
from pygame.locals import *
from dataclasses import dataclass
from math import *
from random import *
import sys
from colorsys import hsv_to_rgb

WIDTH, HEIGHT = 1000, 600
e, f, g, a = 0.5, -0.008, 0.02, 0.0002
PLATFORM_HEIGHT = 40

def draw_arrow(screen, line_color, triangle_color, start, end, triangle_radian, thickness=2):
    rad = pi / 180
    draw.line(screen, line_color, (start.x, start.y), (end.x, end.y), thickness)
    rotation = (atan2(start.y - end.y, end.x - start.x)) + pi / 2   
    draw.polygon(screen, triangle_color, (
    (end.x + triangle_radian * sin(rotation), end.y + triangle_radian * cos(rotation)),
    (end.x + triangle_radian * sin(rotation - 120 * rad), end.y + triangle_radian * cos(rotation - 120 * rad)),
    (end.x + triangle_radian * sin(rotation + 120 * rad), end.y + triangle_radian * cos(rotation + 120 * rad))))

class Circle(sprite.Sprite):
    def __init__(self, color, mass, pos_x: int, pos_y=385):
        super().__init__()
        self.color = color
        self.mass = mass
        self.radius = round((log10(mass) + 1) * 8)
        self.rect = Rect(pos_x - self.radius, pos_y - self.radius, self.radius * 2, self.radius * 2)
        self.pos = Vec(pos_x, pos_y)
        self.vel = Vec(0, 0)
        self.acc = Vec(0, 0)
        self.apos = 0
        self.avel = 0
        self.rect.center = (self.pos.x, self.pos.y)

    def same(self, other):
        return self.mass == other.mass and self.pos == other.pos and self.vel == other.vel and self.acc == other.acc and self.color == other.color and self.radius == other.radius

    def update(self):
        self.avel = abs(self.vel / self.radius)
        self.avel *= 1 if self.vel.x > 0 else -1
        self.apos += self.avel
        self.rect.center = (self.pos.x, self.pos.y)

    def draw(self, screen):
        draw.circle(screen, self.color, self.pos.int().to_tuple(), self.radius, width=3)
        draw.line(screen, self.color, self.pos.to_tuple(),
                  (self.pos + self.radius * Vec(cos(self.apos), sin(self.apos))).to_tuple(), 3)

    def move(self, platforms):
        self.acc = Vec(0, g)
        self.acc.x += self.vel.x * f
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
            self.vel.x *= -1
        if self.pos.x < 0:
            self.pos.x = 0
            self.vel.x *= -1

        for platform in platforms:
            if not (platform.rect.left <= self.right and self.left <= platform.rect.right):
                continue

            if platform.rect.left <= self.pos.x <= platform.rect.right:
                if platform.rect.top <= self.bottom <= platform.rect.centery:
                    self.vel.y *= -e
                    self.pos.y = platform.rect.top - self.radius
                elif platform.rect.bottom >= self.top >= platform.rect.centery:
                    self.vel.y *= -1
                    self.pos.y = platform.rect.bottom + self.radius
            if platform.rect.bottom - 1 > self.top and self.bottom > platform.rect.top + 1:
                if platform.rect.left <= self.right:
                    self.vel.x *= -1
                elif self.left <= platform.rect.right:
                    self.vel.x *= -1

        if self.pos.y < 0:
            self.pos.y = 0
            self.vel.y *= -1

    def is_hit(self, other, margin=0):
        return Vec.dist(self.pos, other.pos) < (self.radius + other.radius) + margin

    def collision(self, other):
        if self.is_hit(other):
            energy_before = self.mass * abs(self.vel) ** 2 / 2 + other.mass * abs(other.vel) ** 2 / 2
            angle = atan2(self.pos.y - other.pos.y, self.pos.x - other.pos.x)
            self.vel = Vec(cos(angle), sin(angle))
            other.vel = Vec(-cos(angle), -sin(angle))
            energy_after = self.mass * abs(self.vel) ** 2 / 2 + other.mass * abs(other.vel) ** 2 / 2
            factor = sqrt(energy_before / energy_after)
            self.vel *= factor
            other.vel *= factor

            collision_vector = self.pos - other.pos
            distance = Vec.dist(self.pos, other.pos)
            overlap = (self.radius + other.radius) - distance
            unit_collision_vector = collision_vector / distance

            if overlap > 0:
                self.pos += unit_collision_vector * (overlap / 2)
                other.pos -= unit_collision_vector * (overlap / 2)

    @property
    def bottom(self):
        return self.pos.y + self.radius

    @property
    def top(self):
        return self.pos.y - self.radius

    @property
    def left(self):
        return self.pos.x - self.radius

    @property
    def right(self):
        return self.pos.x + self.radius

class Platform(sprite.Sprite):
    def __init__(self, width=WIDTH, center=(WIDTH / 2, HEIGHT - PLATFORM_HEIGHT / 2)):
        super().__init__()
        self.surf = Surface((width, PLATFORM_HEIGHT))
        self.surf.fill((50, 50, 50))
        self.rect = self.surf.get_rect(center=center)

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

    def __truediv__(self, k: int | float):
        return Vec(self.x / k, self.y / k)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def to_tuple(self):
        return self.x, self.y

    def int(self):
        return Vec(int(self.x), int(self.y))

    @staticmethod
    def dist(self, other):
        return abs(self - other)

init()
display.set_caption("Physics")
screen = display.set_mode((WIDTH, HEIGHT))
dots = []
platforms = sprite.Group(Platform(), Platform(width=200, center=(300, 400)), Platform(width=300, center=(700, 300)), Platform(width=250, center=(500, 200)))
clock = time.Clock()

def make_circle(x, y):
    mass = randint(1, 101)
    brightness = max(0.1, 1 - (mass - 1) / 200)
    color = random()
    saturation = uniform(0.5, 0.7)
    dots.append(Circle(tuple(map(lambda c: round(c * 255), hsv_to_rgb(color, saturation, brightness))), mass, x, y))

arrow_opacity = 0
mouse_pressed = False
mouse_start, mouse_end = None, None
yet_start, yet_end = mouse_start, mouse_end

while True:
    for evt in event.get():
        if evt.type == QUIT:
            quit()
            sys.exit()
        elif evt.type == MOUSEBUTTONDOWN:
            if evt.button == 1:
                mouse_start = Vec(*mouse.get_pos())
                mouse_pressed = True
                yet_start = mouse_start
                arrow_opacity = 127
            elif evt.button == 3:
                make_circle(*mouse.get_pos())
        elif evt.type == MOUSEBUTTONUP:
            if evt.button == 1:
                mouse_end = Vec(*mouse.get_pos())
                mouse_pressed = False
                yet_end = mouse_end
                arrow_opacity = 127

    screen.fill((0, 0, 0))

    if not mouse_pressed and mouse_start is not None and mouse_end is not None:
        for dot in dots:
            if Vec.dist(dot.pos, mouse_start) < 60:
                dot.vel = (0.02 - sqrt(dot.mass) * 0.0003) * (mouse_end - mouse_start)
        mouse_start, mouse_end = None, None

    for platform in platforms:
        screen.blit(platform.surf, platform.rect)
    for dot in dots:
        dot.move(platforms)
        dot.draw(screen)
        dot.update()

    arrow_color = (arrow_opacity * 2, arrow_opacity * 2, arrow_opacity * 2)
    if mouse_pressed:
        yet_end = Vec(*mouse.get_pos())
        draw_arrow(screen, arrow_color, arrow_color, yet_start, yet_end, 10, 4)
    if not mouse_pressed and arrow_opacity != 0:
        arrow_opacity -= 1
        draw_arrow(screen, arrow_color, arrow_color, yet_start, yet_end, 10, 4)
    if arrow_opacity == 0:
        yet_start, yet_end = None, None

    for i in range(len(dots)):
        for j in range(i + 1, len(dots)):
            dots[i].collision(dots[j])

    display.update()
    clock.tick(1000)