import time
from os import path
from pygame import *
from pygame.locals import *
from time import sleep
import sys
from base import *

init()
display.set_caption("Rider")
screen = display.set_mode((WIDTH, HEIGHT))
clock = time.Clock()
fps = 60

# x, y = 100, 500
# v_x, v_y = 0, 0
# g = 1.0

PT1 = Platform()
player = Player()

all_sprites = sprite.Group()
all_sprites.add(PT1)
all_sprites.add(player)

while True:
    for evt in event.get():
        if evt.type == QUIT:
            quit()
            sys.exit()

    screen.fill((255, 255, 255))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # v_y -= g
    # y += v_y
    # y = max(y, rider.get_height())

    player.move()
    display.update()
    clock.tick(fps)