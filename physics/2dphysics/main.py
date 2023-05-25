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
display.set_caption("Rider")
screen = display.set_mode((WIDTH, HEIGHT))
clock = time.Clock()
fps = 60

# x, y = 100, 500
# v_x, v_y = 0, 0
# g = 1.0
count = 50
show = 0
floor = Platform()
pt1 = Platform(width=200, center=(300, 400))
pt2 = Platform(width=200, center=(700, 300))
dots = sprite.Group()
platforms = sprite.Group()
platforms.add(floor, pt1, pt2)
dotss = []

for i in range(count):
    mass = randint(1, 101)
    massidx = max(0.1, 1 - (mass - 1) / 100)
    coloridx = random()
    s = uniform(0.4, 0.8)
    color = tuple(map(lambda c: round(c * 255), hsv_to_rgb(coloridx, s, massidx)))
    dot = MassPoint(color, mass, (i + 1) * WIDTH // (count + 1), HEIGHT - 100 - 30 * i)
    dotss.append(dot)

dots.add(*dotss)
all_sprites = sprite.Group()
all_sprites.add(platforms)
mouse_pressed = False
mouse_start = (-1, -1)
mouse_end = (-1, -1)
yet_start = mouse_start
yet_end = mouse_end

while True:
    for evt in event.get():
        if evt.type == QUIT:
            quit()
            sys.exit()
        elif evt.type == KEYDOWN:
            if evt.key == K_SPACE:
                for dot in dots:
                    dot.jump(platforms, dotss)
        elif evt.type == MOUSEBUTTONDOWN:
            mouse_start = mouse.get_pos()
            mouse_pressed = True
            yet_start = mouse_start
            show = 10
        elif evt.type == MOUSEBUTTONUP:
            mouse_end = mouse.get_pos()
            yet_end = mouse_end
            show = 10
            mouse_pressed = False

    if mouse_start != (-1, -1) and mouse_end != (-1, -1):
        for dot in dotss:
            if dot.pos.dist(Vec(mouse_start[0], mouse_start[1])) < dot.radius * 3:
                dot.vel = (0.3 - log2(dot.mass) / 50) * Vec(mouse_end[0] - mouse_start[0], mouse_end[1] - mouse_start[1])

        mouse_start = (-1, -1)
        mouse_end = (-1, -1)

    screen.fill((0, 0, 0))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    for dot in dots:
        dot.move(platforms, left_key=K_KP4, right_key=K_KP6)
        draw.circle(screen, dot.color, (dot.pos.x, dot.pos.y), dot.radius)
        dot.update()
        screen.blit(dot.text, (dot.pos.x - dot.radius / 2, dot.pos.y - dot.radius / 2))

    color_arrow = (show * 51//2, show * 51//2, show * 51//2)

    if mouse_pressed:
        yet_end = mouse.get_pos()
        arrow(screen, color_arrow, color_arrow, yet_start, yet_end, 10, 4)
    if not mouse_pressed and show != 0:
        arrow(screen, color_arrow, color_arrow, yet_start, yet_end, 10, 4)
        show -= 1
    if show == 0:
        yet_start = (-1, -1)
        yet_end = (-1, -1)

    for i in range(len(dotss)):
        for j in range(i + 1, len(dotss)):
            dotss[i].collision(dotss[j])

    display.update()
    clock.tick(fps)