import sys
from os import path
from pygame import *
from pygame.locals import *
from copy import copy
from base import *

def main(mouse_pos, omok: Omok):
    mouse_x, mouse_y = mouse_pos

    def nth(pos: int) -> int:
        pos = min(max(pos, 11), 610)
        return round((pos - 30) / 40)

    for evt in event.get():
        if evt.type == QUIT:
            quit()
            sys.exit()

        elif evt.type == MOUSEBUTTONDOWN:
            set_x, set_y = nth(mouse_x), nth(mouse_y)

            if omok.board.empty(set_x, set_y):
                stamp = copy(user_stone)
                stamp.set_alpha(255)

                counts = omok.check_8dir((set_x, set_y), user_stone)
                if not any(count >= 6 for count in counts.values()):
                    omok.board[set_x, set_y] = stamp

                    if any(count == 5 for count in counts.values()):
                        print("User win")
                        quit()
                        sys.exit()
                else:
                    print('장목!!!')

                counts = omok.check_8dir((set_x, set_y), user_stone)
                if line:
                    print("User win")
                    quit()
                    sys.exit()
            else:
                continue

            omok.board[best_pos(omok.board)] = copy(bot_stone)
            counts = omok.check_8dir((set_x, set_y), user_stone)
            if any(count >= 5 for count in counts.values()):
                print("Bot win")
                quit()
                sys.exit()

    screen.blit(board_image, (0, 0))

    omok.board.iterate(lambda i, j:
        screen.blit(omok.board[i, j],
                  (30 + 40 * i - user_stone.get_size()[0] / 2, 30 + 40 * j - user_stone.get_size()[0] / 2))
        if not omok.board.empty(i, j) else None
    )

    user_stone.set_alpha(128)
    screen.blit(user_stone, (
    30 + 40 * nth(mouse_x) - user_stone.get_size()[0] / 2, 30 + 40 * nth(mouse_y) - user_stone.get_size()[0] / 2))

def best_pos(board: Board):
    # TODO - implement AI

    for i in range(15):
        for j in range(15):
            if board.empty(i, j):
                return i, j


if __name__ == "__main__":
    init()
    assets = path.join(path.dirname(__file__), "assets")
    board_image = image.load(path.join(assets, 'board.png'))  # (621, 621), (30, 30), step 40
    white_stone = image.load(path.join(assets, 'white_stone.png'))
    black_stone = image.load(path.join(assets, 'black_stone.png'))
    user_stone, bot_stone = black_stone, white_stone

    display.set_caption("Omok")
    screen = display.set_mode(board_image.get_size())
    clock = time.Clock()
    fps = 30

    RIGHT, DOWN, RIGHT_DOWN, RIGHT_UP = (1, 0), (0, 1), (1, 1), (1, -1)

    omok = Omok(Board())
    while True:
        main(mouse.get_pos(), omok)
        display.update()
        clock.tick(fps)
