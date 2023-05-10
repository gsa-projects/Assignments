from pygame import Surface
from copy import copy
from dataclasses import dataclass
import pygame

class Image:
    def __init__(self, path):
        self.path = path
        self.image = pygame.image.load(path)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Image):
            return False
        else:
            return self.path == other.path

    def __copy__(self):
        return Image(self.path)
    
    def get_size(self):
        return self.image.get_size()
    
    def set_alpha(self, alpha):
        self.image.set_alpha(alpha)

    def get_width(self):
        return self.image.get_width()
    
    def get_height(self):
        return self.image.get_height()
    
@dataclass
class Point:
    no: int
    stone: Image

class Board:
    def __init__(self, startpx: tuple[int, int], endpx: tuple[int, int], steppx: int, stone_size: int):
        self.start = startpx
        self.end = endpx
        self.step = steppx
        self.stone_size = stone_size
        self.count = 0
        self.stones: list[list[Point | None]] = [[None for _ in range(15)] for _ in range(15)]

    def __getitem__(self, pos: tuple[int, int], also_no: bool = False) -> Point | None:
        if self.stones[pos[0]][pos[1]] is None:
            return None
        else:
            if also_no:
                return self.stones[pos[0]][pos[1]]
            else:
                return self.stones[pos[0]][pos[1]].stone

    def __setitem__(self, pos: tuple[int, int], value: Image):
        if self.empty(pos):
            self.count += 1
            self.stones[pos[0]][pos[1]] = Point(self.count, value)
            return True
        else:
            return False

    def empty(self, pos: tuple[int, int]):
        return self[pos] is None

    def get_counts(self, pos: tuple[int, int], stone: Image) -> dict[tuple, int]:
        counts = {}
        for factor in ((1, 0), (0, 1), (1, 1), (1, -1)):
            counts[factor] = self.get_counts_each(pos, factor, stone)

        return counts

    # FIXME - 다 틀림
    def get_counts_each(self, pos: tuple[int, int], factor: tuple[int, int], stone: Image) -> int:
        count = 1
        
        x, y = pos
        dx, dy = factor
        while True:
            x += dx * self.step
            y += dy * self.step

            if not (self.start[0] <= x <= self.end[0] and self.start[1] <= y <= self.end[1]):
                break
            if self[self.nth(x), self.nth(y)] == stone:
                count += 1
            else:
                break

        x, y = pos
        dx, dy = factor
        while True:
            x -= dx * self.step
            y -= dy * self.step

            if not (self.start[0] <= x <= self.end[0] and self.start[1] <= y <= self.end[1]):
                break
            if self[self.nth(x), self.nth(y)] == stone:
                count += 1
            else:
                break

        return count
    
    def placement(self, pos: tuple[int, int], stone: Image):
        stamp = copy(stone)
        stamp.set_alpha(255)
        self[pos] = stamp

    def best_pos(self):
        # TODO - implement AI

        for i in range(15):
            for j in range(15):
                if self.empty((i, j)):
                    return i, j

    def nth(self, pos: int) -> int:
        pos = min(max(pos, self.start[0]), self.end[0])
        return round((pos - self.start[0]) / self.step)
    
    def nth_to_pos(self, pos: int) -> int:
        return self.to_pos(self.nth(pos))
    
    def to_pos(self, pos: int) -> int:
        return pos * self.step + self.start[0] - self.stone_size // 2