import pygame as game
import json
from math import *
from dataclasses import dataclass

with open("constants.json") as file:
    constants = json.load(file)

g = constants['gravity']
e = constants['cor']
π = pi

def change_axis(x, y=None):
    if y is None:
        if isinstance(x, Vector):
            return x.x, constants['height'] - x.y
        elif isinstance(x, tuple):
            return x[0], constants['height'] - x[1]
    else:
        return x, constants['height'] - y

@dataclass
class Vector:
    x: int | float
    y: int | float

    def __post_init__(self):
        pass

        def make_zero(x, tol=1e-4):
            if abs(x) < tol:
                return 0
            return x

        self.x = round(make_zero(self.x), 5)
        self.y = round(make_zero(self.y), 5)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return str(self)

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
        return self * k

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

class Platform(game.sprite.Sprite):
    def __init__(self, start: tuple[int, int], end: tuple[int, int], thickness=max(1, constants['margin'] * 2), color=(255, 255, 255), friction=0):
        super().__init__()

        self.start = Vector(*start)
        self.end = Vector(*end)
        self.thickness = thickness
        self.color = color
        self.friction = friction

    def __str__(self):
        return f"Platform(from={self.start}, to={self.end}, μ={self.friction})"

    def __repr__(self):
        return str(self)

    @staticmethod
    def init(start: tuple[int, int], right, up=0, thickness=max(1, constants['margin'] * 2), color=(255, 255, 255), friction=0):
        return Platform(start, (start[0] + right, start[1] + up), thickness, color, friction)

    @property
    def left(self):
        return self.start.x

    @property
    def right(self):
        return self.end.x

    @property
    def slope(self):
        return (self.end.y - self.start.y) / (self.end.x - self.start.x)

    @property
    def angle(self):
        return atan(self.slope)

    def dist(self, ball):
        a, b = self.start
        c, d = self.end
        c1, c2 = ball.pos
        dist = abs((d - b) * c1 + (a - c) * c2 + b * c - a * d) / sqrt((d - b) ** 2 + (a - c) ** 2) + self.thickness / 2
        return dist if ball.pos.y >= self.top(ball.pos.x) else -dist

    def top(self, x):
        return self.slope * (x - self.start.x) + self.start.y

    def bottom(self, x):
        return self.top(x) - self.thickness

    def draw(self, screen):
        game.draw.line(screen, self.color, change_axis(self.start), change_axis(self.end), self.thickness)

class Ball(game.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], radius, color: tuple[int, int, int]):
        super().__init__()
        self.radius = radius
        self.color = color
        self.pos = Vector(*pos)
        self.vel = Vector(0, 0)
        self.acc = Vector(0, -g)

        self.dragging = False
        self.canjump = False

    def __str__(self):
        return f"Ball(r={self.radius}, s={self.pos}, v={self.vel}, a={self.acc})"

    def __repr__(self):
        return str(self)

    @property
    def left(self):
        return self.pos.x - self.radius

    @property
    def right(self):
        return self.pos.x + self.radius

    @property
    def top(self):
        return self.pos.y + self.radius

    @property
    def bottom(self):
        return self.pos.y - self.radius

    def on_platform(self, platforms):
        # 닿은 플랫폼과, 플랫폼의 어느 부분에 맞았는지를 반환합니다.

        for platform in platforms:
            if platform.left <= self.pos.x <= platform.right:
                plat = platform.thickness / 2
                dist = platform.dist(self)

                if dist >= 0:
                    if 0.5 + plat >= dist - self.radius >= plat:
                        self.canjump = True
                        return platform, 'top'
                else:
                    if 0.5 + plat >= -dist - self.radius >= plat:
                        self.canjump = False
                        return platform, 'bottom'

        self.canjump = False
        return None

    def update(self, platforms, mouse_pos, jump_key=game.K_SPACE, left_key=game.K_LEFT, right_key=game.K_RIGHT):
        if self.dragging:
            self.vel = Vector(0, 0)
            self.acc = Vector(0, -g)
            self.pos = mouse_pos
            return

        pressed_keys = game.key.get_pressed()
        a = constants['acceleration']
        f = constants['friction']

        # if pressed_keys[left_key]:
        #     self.vel.x -= 0.001
            # self.vel.x += 5
        # elif pressed_keys[right_key]:
        #     self.vel.x += 0.001
            # self.vel.x -= 5

        if self.pos.x > constants['width']:
            self.pos.x = constants['width']
            self.vel.x *= -1
            self.acc.x *= -1
        if self.pos.x < 0:
            self.pos.x = 0
            self.vel.x *= -1
            self.acc.x *= -1
        if self.pos.y > constants['height']:
            self.pos.y = constants['height']
            self.vel.y *= -1
            self.acc.y *= -1

        on = self.on_platform(platforms)
        if on is not None:
            platform, status = on

            if status == 'top':
                if platform.left == 400:
                    print(f'v={self.vel}, a={self.acc}')

                θ = platform.angle
                N = Vector(g*cos(θ)*cos(θ + π/2), g*cos(θ)*sin(θ + π/2))
                a, b = self.vel
                self.vel.x = a*cos(θ)**2 + b*sin(θ)*cos(θ) - e*(a*sin(θ)**2 + b*sin(θ)*cos(θ))
                self.vel.y = a*sin(θ)*cos(θ) + b*sin(θ)**2 - e*(a*sin(θ)*cos(θ) + b*cos(θ)**2)
                self.acc = N + Vector(0, -g)
            elif status == 'bottom':
                self.pos.y = platform.bottom(self.pos.x) - self.radius - platform.thickness / 2
                self.vel.y *= -1
        else:
            self.acc.y = -g

        if pressed_keys[jump_key] and self.canjump:
            θ = on[0].angle + π / 2
            add = constants['jump'] * Vector(cos(θ), sin(θ))
            self.vel += add

        self.acc.x += self.vel.x * f
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

    def jump(self, platforms, pressed_key, jump_key=game.K_SPACE):
        pass
        # if pressed_key == jump_key:
        #     on = self.on_platform(platforms)
        #     print(self, on)
        #     if on is not None:
        #         θ = on[0].angle + π / 2
        #         add = constants['jump'] * Vector(cos(θ), sin(θ))
        #         print(degrees(θ), add)
        #
        #         self.vel += add

    def draw(self, screen):
        game.draw.circle(screen, self.color, change_axis(self.pos), self.radius)
