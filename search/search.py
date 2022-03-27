import json
from typing import List


class Hexagon:
    coords: (int, int)
    color: str

    def __init__(self, i: int, j: int):
        self.coords = (i, j)

    def __repr__(self):
        return f"{self.coords} {self.color}"

    def __add__(self, other):
        return Hexagon(self.coords[0] + other.coords[0],
                       self.coords[1] + other.coords[1])


def neighbours(self: Hexagon, n: int) -> {(int, int)}:
    return {(self + a).coords for a in direction_vectors() if
            valid((self + a).coords, n)}


def valid(a: (int, int), n: int) -> bool:
    return a[0] in range(0, n) and a[1] in range(0, n)


def direction_vectors() -> List[Hexagon]:
    return [Hexagon(+1, 0), Hexagon(+1, -1), Hexagon(0, -1),
            Hexagon(-1, 0), Hexagon(-1, +1), Hexagon(0, +1)]


class Board:
    pieces: List[List[Hexagon]]

    def __init__(self, n: int):
        self.pieces = []
        for i in range(n):
            self.pieces.append([])
            for j in range(n):
                new_piece = Hexagon(i, j)
                self.pieces[i].append(new_piece)

    def __repr__(self):
        return f"{self.pieces}"


class Input:
    n: int
    board: List
    start: List[int]
    goal: List[int]

    def __init__(self, string):
        data = json.loads(string)
        self.__dict__ = data
