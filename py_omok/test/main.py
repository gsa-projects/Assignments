from os import path
from pygame import *
from pygame.locals import *
from base import *
from time import sleep
def main(mouse_pos, board: Board):
    global stat, indices
    for evt in event.get():
        if evt.type == QUIT:
            quit()
            sys.exit()
        elif evt.type == MOUSEBUTTONDOWN:
            placement_pos = board.from_pixel(mouse_pos)
            if not board.empty(placement_pos):
                stat, indices = 'no', None
                continue
            counts = board.get_counts(placement_pos, user_stone)
            if all(count <= 5 for count in counts.values()):
                board.placement(placement_pos, user_stone)
                for diff, count in counts.items():
                    if count >= 5:
                        stat, indices = 'win', board.get_counts_each(placement_pos, BoardPos(*diff), user_stone, get_pos=True)
            else:
                stat, indices = 'no', None
                continue
            placement_pos = board.best_pos(user=user_stone, bot=bot_stone)
            board.placement(placement_pos, bot_stone)
            counts = board.get_counts(placement_pos, bot_stone)
            for diff, count in counts.items():
                if count >= 5: stat, indices = 'lose', board.get_counts_each(placement_pos, BoardPos(*diff), bot_stone, get_pos=True)
    screen.blit(board_background.image, (0, 0))
    for i in range(15):
        for j in range(15):
            if not board.empty(BoardPos(i, j)):
                screen.blit(board[BoardPos(i, j)].image, board.to_pixel(BoardPos(i, j)))
    pre_pos = board.from_pixel(mouse.get_pos()).fit_in()
    counts = board.get_counts(pre_pos, user_stone)
    is_long = board.empty(pre_pos) and any(count >= 6 for count in counts.values())
    screen.blit(no.image if is_long else user_stone.image, board.to_pixel(pre_pos))
    return stat, indices, board
if __name__ == "__main__":
    init()
    assets = path.join(path.dirname(__file__), "assets")
    no, win, lose = Asset(path.join(assets, 'no.png')), Asset(path.join(assets, 'win.png')), Asset(path.join(assets, 'lose.png'))
    bot_stone, user_stone = Asset(path.join(assets, 'white_stone.png')), Asset(path.join(assets, 'black_stone.png'))
    board_background = Asset(path.join(assets, 'board.png'))
    board = Board(startpx=(30, 30), endpx=(590, 590), steppx=40, stone_size=user_stone.get_width())
    display.set_caption("Omok")
    screen, clock, fps = display.set_mode(board_background.get_size()), time.Clock(), 30
    stat, indices = 'nothing', None
    while True:
        user_stone.set_alpha(128)
        no.set_alpha(128)
        stat, indices, board = main(mouse.get_pos(), board)
        if indices is not None:
            line = copy(win if stat == 'win' else lose)
            for index in indices:
                screen.blit(line.image, board.to_pixel(index))
        display.update()
        if stat == 'win' or stat == 'lose':
            sleep(5)
            quit()
            sys.exit()
        clock.tick(fps)