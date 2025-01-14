import pygame as game
from os import path
import os
import json
from basic import *

constants = {}
with open('physics/3트/constants.json') as file:
    constants = json.load(file)

game.init()
game.display.set_caption("2D Physics")
width, height = constants['width'], constants['height']
screen = game.display.set_mode((width, height))
clock = game.time.Clock()

balls = game.sprite.Group()
a=Ball((200, 100), 5, (255, 155, 155))
b=Ball((300, 100), 10, (155, 155, 255))
balls.add(a, b)

platforms = game.sprite.Group()
platforms.add(
    Platform.init((0, 15), right=width),
    Platform.init((200, 120), right=100, up=-(100 / sqrt(3))),
    Platform.init((400, 125), right=width//3, up=50)
)

all_sprites = game.sprite.Group()
all_sprites.add(balls, platforms)

while True:
    mouse_pos = Vector(*change_axis(game.mouse.get_pos()))

    for event in game.event.get():
        if event.type == game.QUIT:
            game.quit()
            quit()
        # elif event.type == game.KEYDOWN:
        #     a.jump(platforms, event.key, jump_key=game.K_w)
        #     b.jump(platforms, event.key, jump_key=game.K_UP)
        elif event.type == game.MOUSEBUTTONDOWN:
            for ball in balls:
                if Vector.dist(ball.pos, mouse_pos) <= 2 * ball.radius:
                    ball.dragging = True
                    # print(ball, 'dragging on')
        elif event.type == game.MOUSEBUTTONUP:
            for ball in balls:
                if ball.dragging:
                    ball.dragging = False
                    # print(ball, 'dragging off')

    screen.fill(tuple(constants['background_color']))

    for sprite in all_sprites:
        sprite.draw(screen)

    a.update(platforms, mouse_pos, jump_key=game.K_w, left_key=game.K_a, right_key=game.K_d)
    b.update(platforms, mouse_pos, jump_key=game.K_UP, left_key=game.K_LEFT, right_key=game.K_RIGHT)

    game.display.update()
    # clock.tick(10000)
