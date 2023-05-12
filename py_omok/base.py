from pygame import Surface
from copy import copy
from dataclasses import dataclass
import pygame
import sys
import torch

class Asset:
    def __init__(self, path):
        self.path = path
        self.image = pygame.image.load(path)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Asset):
            return False
        else:
            return self.path == other.path

    def __copy__(self):
        return Asset(self.path)
    
    def get_size(self):
        return self.image.get_size()
    
    def set_alpha(self, alpha):
        self.image.set_alpha(alpha)

    def get_width(self):
        return self.image.get_width()
    
    def get_height(self):
        return self.image.get_height()
    
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

    def __add__(self, other):
        return BoardPos(self.row + other.row, self.col + other.col)
    
    def __sub__(self, other):
        return BoardPos(self.row - other.row, self.col - other.col)
    
    @property
    def isin(self):
        return 0 <= self.row < 15 and 0 <= self.col < 15

class Board:
    def __init__(self, startpx: tuple[int, int], endpx: tuple[int, int], steppx: int, stone_size: int):
        self.start = startpx
        self.end = endpx
        self.step = steppx
        self.stone_size = stone_size
        self.count = 0
        self.stones: list[list[Value | None]] = [[None for _ in range(15)] for _ in range(15)]

    def __getitem__(self, pos: BoardPos, also_no: bool = False) -> Asset | Value | None:
        if self.empty(pos):
            return None
        else:
            if also_no:
                return self.stones[pos.row][pos.col]
            else:
                return self.stones[pos.row][pos.col].stone

    def __setitem__(self, pos: BoardPos, image: Asset):
        if self.empty(pos):
            self.count += 1
            self.stones[pos.row][pos.col] = Value(self.count, image)
            return True
        else:
            return False

    def empty(self, pos: BoardPos):
        return self.stones[pos.row][pos.col] is None

    # FIXME - 다 틀림
    def get_counts(self, pos: BoardPos, stone: Asset) -> dict[tuple, int]:
        counts = {}
        for factor in ((1, 0), (0, 1), (1, 1), (1, -1)):
            counts[factor] = self.get_counts_each(pos, factor, stone)

        return counts

    # FIXME - 다 틀림
    def get_counts_each(self, pos: BoardPos, factor: tuple[int, int], stone: Asset) -> int:
        diff = BoardPos(*factor)
        count = 1

        tmp = pos
        while True:
            tmp += diff

            if not tmp.isin:
                break
            if self[tmp] == stone:
                count += 1
            else:
                break

        tmp = pos
        while True:
            tmp -= diff

            if not tmp.isin:
                break
            if self[tmp] == stone:
                count += 1
            else:
                break

        return count
    
    def placement(self, pos: BoardPos, stone: Asset):
        stamp = copy(stone)
        stamp.set_alpha(255)
        self[pos] = stamp

    def best_pos(self) -> BoardPos:
        input_data = torch.zeros((15, 15))
        for row in range(15):
            for col in range(15):
                if not self.empty(BoardPos(row, col)):
                    input_data[row, col] = float(self.__getitem__(BoardPos(row, col), also_no=True).no)

        model = torch.load('model.pt')
        output = model(input_data.reshape((1, 15, 15)))[0]

        for row in range(15):
            for col in range(15):
                print(round(output[row, col].item(), 1), end=' ')
            print()

        for row in range(15):
            for col in range(15):
                if round(output[row, col].item()) == self.count + 1:
                    return BoardPos(row, col)
    
    def from_pixel(self, pixel: tuple[int, int]) -> BoardPos:
        from_ = lambda pos: round((pos - self.start[0]) / self.step)
        return BoardPos(from_(pixel[0]), from_(pixel[1]))

    def to_pixel(self, pos: BoardPos) -> tuple[int, int]:
        to_ = lambda pos: pos * self.step + self.start[0] - self.stone_size // 2
        return to_(pos.row), to_(pos.col)