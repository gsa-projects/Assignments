import sys
from os import path
from pygame import *
from pygame.locals import *
from copy import copy

class Board:
    def __init__(self, w=15, h=15):
        self.width = w
        self.height = h
        self.stones: list[list[Surface | None]] = [[None for _ in range(w)] for _ in range(h)]

    def __getitem__(self, pos: tuple[int, int]):
        return self.stones[pos[0]][pos[1]]

    def __setitem__(self, pos: tuple[int, int], value: Surface):
        if self.empty(*pos):
            self.stones[pos[0]][pos[1]] = value
            return True
        else:
            return False

    def empty(self, x: int, y: int):
        return self[x, y] is None

class Omok:
    def __init__(self, board: Board):
        self.board = board

def main(mouse_pos, board: Board):
    mouse_x, mouse_y = mouse_pos

    def nth(pos: int) -> int:
        return round((pos - 20) / 40)

    for evt in event.get():
        if evt.type == QUIT:
            quit()
            sys.exit()
        elif evt.type == MOUSEBUTTONDOWN:
            set_x, set_y = nth(mouse_x), nth(mouse_y)

            if board.empty(set_x, set_y):
                stamp_white_stone = copy(white_stone)
                stamp_white_stone.set_alpha(255)
                board[set_x, set_y] = stamp_white_stone
            else:
                continue

            board[best_pos(board)] = copy(black_stone)

    screen.blit(board_image, (0, 0))

    for i in range(15):
        for j in range(15):
            if not board.empty(i, j):
                screen.blit(board[i, j], (20 + 40 * i - 15, 20 + 40 * j - 15))

    white_stone.set_alpha(128)
    screen.blit(white_stone, (20 + 40 * nth(mouse_x) - 15, 20 + 40 * nth(mouse_y) - 15))

def best_pos(board: Board):
    # TODO - implement AI   
    for i in range(15):
        for j in range(15):
            if board.empty(i, j):
                return i, j

if __name__ == "__main__":
    init()
    display.set_caption("Omok")
    screen = display.set_mode((601, 601))
    clock = time.Clock()
    fps = 30

    assets = path.join(path.dirname(__file__), "assets")
    board_image = image.load(path.join(assets, 'board.png'))  # (601, 601), (20, 20), step 40
    white_stone = image.load(path.join(assets, 'white_stone.png'))  # (30, 30)
    black_stone = image.load(path.join(assets, 'black_stone.png'))  # (30, 30)

    board = Board(w=15, h=15)
    while True:
        main(mouse.get_pos(), board)
        display.update()
        clock.tick(fps)
