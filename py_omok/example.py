import sys
from math import *
from pygame import *
from pygame.locals import *

init()
display.set_caption("Omok")
screen = display.set_mode((601, 601))
clock = time.Clock()
fps = 30
board_image = image.load("C:/Users/rhseung/Coding/Repositories/gsa-projects/Assignments/py_omok/assets/board.png")  # (601, 601), (20, 20), step 40
white_stone = image.load("C:/Users/rhseung/Coding/Repositories/gsa-projects/Assignments/py_omok/assets/white_stone.png")    # (30, 30)
black_stone = image.load("C:/Users/rhseung/Coding/Repositories/gsa-projects/Assignments/py_omok/assets/black_stone.png")    # (30, 30)

# stones = [[None for _ in range(15)] for _ in range(15)]

while True:
    for evt in event.get():
        if evt.type == QUIT:
            quit()
            sys.exit()
        # elif evt.type == MOUSEBUTTONDOWN:
        #     stones[nth(mouse_y)][nth(mouse_x)] = "white"

    mouse_x, mouse_y = mouse.get_pos()
    nth = lambda pos: round((pos - 20) / 40)
    white_stone.set_alpha(128)    
    screen.blit(white_stone, (20 + 40 * nth(mouse_x) - 15, 20 + 40 * nth(mouse_y) - 15))
    screen.blit(board_image, (0, 0))

    display.update()
    clock.tick(fps)
