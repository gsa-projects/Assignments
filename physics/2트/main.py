import time
from os import path
from pygame import *
from pygame.locals import *
from time import sleep
from math import *
from random import *
import sys
from base import *
from colorsys import hsv_to_rgb

init()
display.set_caption("Physics")

screen = display.set_mode((WIDTH, HEIGHT))
clock = time.Clock()
fps = 60

all_sprites = sprite.Group()

circles = sprite.Group()
circles.add(
    Circle((WIDTH // 2 - 100, HEIGHT // 2), mass=10, radius=10, color=(255, 0, 0)),
    # Circle((WIDTH // 2 + 100, HEIGHT // 2), mass=10, radius=10)
)

platforms = sprite.Group()
platforms.add(
    Platform((0, 5), width=WIDTH, thickness=100),
    Platform((100, 200), width=400, thickness=100)
)

all_sprites.add(circles, platforms)

while True:
    for evt in event.get():
        if evt.type == QUIT:
            quit()
            sys.exit()
        elif evt.type == KEYDOWN:
            for platform in circles:
                platform.jump(evt.key)

    screen.fill((0, 0, 0))

    for platform in platforms:
        screen.blit(platform.surf, platform.rect)

    for circle in circles:
        circle.move(platforms)
        draw.circle(screen, circle.color, change_axis(circle.s), circle.radius)
        # platform.draw(screen)

    display.update()
    clock.tick(fps)