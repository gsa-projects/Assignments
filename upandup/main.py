import time
from os import path
from pygame import *
from pygame.locals import *
from time import sleep
from math import *
import sys
from base import *

init()
display.set_caption("Up & Up")
screen = display.set_mode((WIDTH, HEIGHT))
clock = time.Clock()
fps = 60

# x, y = 100, 500
# v_x, v_y = 0, 0
# g = 1.0
m1 = 1
m2 = 100

platforms = sprite.Group()
all_sprites = sprite.Group()

player = Player()

bottom = Platform(width=WIDTH, center_x=WIDTH/2)
for x in range(5):
    p = Platform()
    platforms.add(p)
    all_sprites.add(p)

platforms.add(bottom)
all_sprites.add(platforms, player)

while True:
    for evt in event.get():
        if evt.type == QUIT:
            quit()
            sys.exit()
        elif evt.type == KEYDOWN:
            if evt.key == K_SPACE:
                player.jump(platforms)

    screen.fill((0, 0, 0))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    player.move(left_key=K_LEFT, right_key=K_RIGHT)
    player.update(platforms)

    display.update()
    clock.tick(fps)