from dataclasses import dataclass

@dataclass
class Point:
    no: int
    stone: Surface

class Board:
    def __init__(self):
        self.width = 15
        self.height = 15
        self.count = 0
        self.stones: list[list[Point | None]] = [[None for _ in range(self.width)] for _ in range(self.height)]

    def __getitem__(self, pos: tuple[int, int]):
        return self.stones[pos[0]][pos[1]].stone

    def __setitem__(self, pos: tuple[int, int], value: Surface):
        if self.empty(*pos):
            self.count += 1
            self.stones[pos[0]][pos[1]] = Point(self.count, value)
            return True
        else:
            return False

    def empty(self, x: int, y: int):
        return self[x, y] is None

    def iterate(self, func):
        for i in range(self.width):
            for j in range(self.height):
                func(i, j)

class Omok:
    def __init__(self, board: Board):
        self.board = board

    def check_8dir(self, pos: tuple[int, int], stone: Surface) -> dict[tuple, int]:
        counts = {}
        for factor in (RIGHT, DOWN, RIGHT_DOWN, RIGHT_UP):
            counts[factor] = self.check_line(pos, factor, stone)

        return counts

    def check_line(self, pos: tuple[int, int], factor: tuple[int, int], stone: Surface) -> int:
        x, y = pos
        dx, dy = factor
        count = 1
        while True:
            x, y = x + dx, y + dy
            if not (0 <= x < self.board.width and 0 <= y < self.board.height):
                break
            if self.board[x, y] == stone:
                count += 1
            else:
                break

        x, y = pos
        dx, dy = factor
        while True:
            x, y = x - dx, y - dy
            if not (0 <= x < self.board.width and 0 <= y < self.board.height):
                break
            if self.board[x, y] == stone:
                count += 1
            else:
                break

        return count
