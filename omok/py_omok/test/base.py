import sys
from copy import copy
from dataclasses import dataclass
import pygame
import torch
class Asset:
    def __init__(self, path):
        self.path = path
        self.image = pygame.image.load(path)
    def __eq__(self, other) -> bool:
        if not isinstance(other, Asset): return False
        else: return self.path == other.path
    def __copy__(self): return Asset(self.path)
    def get_size(self): return self.image.get_size()
    def set_alpha(self, alpha): self.image.set_alpha(alpha)
    def get_width(self): return self.image.get_width()
    def get_height(self): return self.image.get_height()
@dataclass
class Value:
    no: int
    stone: Asset
@dataclass
class BoardPos:
    row: int
    col: int
    def fit_in(self):
        self.row = max(0, min(14, self.row))
        self.col = max(0, min(14, self.col))
        return self
    def __add__(self, other): return BoardPos(self.row + other.row, self.col + other.col)
    def __sub__(self, other): return BoardPos(self.row - other.row, self.col - other.col)
    @property
    def isin(self): return 0 <= self.row < 15 and 0 <= self.col < 15
class Board:
    def __init__(self, startpx: tuple[int, int], endpx: tuple[int, int], steppx: int, stone_size: int):
        self.start = startpx
        self.end = endpx
        self.step = steppx
        self.stone_size = stone_size
        self.count = 0
        self.stones: list[list[Value | None]] = [[None for _ in range(15)] for _ in range(15)]
    def __getitem__(self, pos: BoardPos, also_no: bool = False) -> Asset | Value | None:
        if self.empty(pos): return None
        elif also_no: return self.stones[pos.row][pos.col]
        else: return self.stones[pos.row][pos.col].stone
    def __setitem__(self, pos: BoardPos, image: Asset):
        if self.empty(pos):
            self.count += 1
            self.stones[pos.row][pos.col] = Value(self.count, image)
            return True
        else: return False
    def empty(self, pos: BoardPos):
        return self.stones[pos.row][pos.col] is None
    def get_counts(self, pos: BoardPos, user: Asset, bot: Asset | None = None, get_pos=False) -> dict[tuple[int, int], int]:
        counts = {}
        for factor in ((1, 0), (0, 1), (1, 1), (1, -1)):
            counts[factor] = self.get_counts_each(pos, BoardPos(*factor), user, bot, get_pos)
        return counts
    def get_counts_each(self, pos: BoardPos, diff: BoardPos, user: Asset, bot: Asset | None = None, get_pos=False) -> int | list[BoardPos]:
        to_bot = bot is not None
        if get_pos:
            count = []
            if not to_bot:
                count.append(pos)
        else: count = 0 if to_bot else 1
        tmp = pos
        while True:
            tmp += diff
            if not tmp.isin: break
            if self[tmp] == user:
                if get_pos: count.append(tmp)
                else: count += 1
            else: break
        tmp = pos
        while True:
            tmp -= diff
            if not tmp.isin: break
            if self[tmp] == user:
                if get_pos: count.append(tmp)
                else: count += 1
            else: break
        return count
    def placement(self, pos: BoardPos, stone: Asset):
        stamp = copy(stone)
        stamp.set_alpha(255)
        self[pos] = stamp
    def best_pos(self, user: Asset, bot: Asset) -> BoardPos:
        input_data = torch.zeros((15, 15))
        for row in range(15):
            for col in range(15):
                if not self.empty(BoardPos(row, col)):
                    input_data[row, col] = float(self.__getitem__(BoardPos(row, col), also_no=True).no)
        model = torch.load('C:/Users/rhseung/Coding/Repositories/gsa-projects/Assignments/py_omok/test/models/model.pt')
        output = model(input_data.reshape((1, 15, 15)))[0]
        idxs = []
        counts_s = [[{} for _ in range(15)] for _ in range(15)]
        is_4 = False
        for row in range(15):
            for col in range(15):
                if self.empty(BoardPos(row, col)):
                    tmp = BoardPos(row, col)
                    counts_s[row][col] = self.get_counts(tmp, user=user, bot=bot)
                    counts = counts_s[row][col]
                    values = counts.values()
                    if all(count < 5 for count in values):
                        if any(count == 4 for count in values): is_4 = True
                        for diff, count in counts.items():
                            if count == (4 if is_4 else 3):                                
                                if not is_4:
                                    forward = tmp + BoardPos(*diff)
                                    backward = tmp - BoardPos(*diff)
                                    if not ((not forward.isin) or self[forward] == user) or ((not backward.isin) or self[backward] == user): # 벽이거나, 유저 돌이라서 막혀 있다면 -> 한 쪽이 막혀있는 3목
                                        idxs.append(tmp)
                                else: idxs.append(tmp)
        if len(idxs) == 0:
            for row in range(15):
                for col in range(15):
                    if self.empty(BoardPos(row, col)):
                        counts = counts_s[row][col]
                        if any(count >= 6 for count in counts.values()): continue
                        idxs.append(BoardPos(row, col))
        try: idx = idxs[0]
        except IndexError:
            print('징한놈 ㅋㅋ')  # 기보가 전부 돌로 다 채워지면 이렇게 하고 끝내기
            quit(); sys.exit()
        for pos in idxs:
            if output[idx.row, idx.col].item() < output[pos.row, pos.col].item(): idx = pos
        return idx
    def from_pixel(self, pixel: tuple[int, int]) -> BoardPos:
        from_ = lambda pos: round((pos - self.start[0]) / self.step)
        return BoardPos(from_(pixel[0]), from_(pixel[1]))
    def to_pixel(self, pos: BoardPos) -> tuple[int, int]:
        to_ = lambda pos: pos * self.step + self.start[0] - self.stone_size // 2
        return to_(pos.row), to_(pos.col)