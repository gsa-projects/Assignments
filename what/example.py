import sys
import pygame
from pygame.locals import *
import random

pygame.init()
pygame.display.set_caption("Example")
screen_size = (640, 480)    # (height, width)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
fps = 30

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(WHITE)
    pygame.display.update()
    clock.tick(fps)
