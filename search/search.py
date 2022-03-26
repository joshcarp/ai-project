import json
from typing import List


class Color:
    name: str


class Hexagon:
    pass


class Hexagon:
    coords: (int, int)
    color: Color
    neighbours: List[Hexagon]

    def __init__(self, i, j):
        self.coords = (i, j)

    def __repr__(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True,
                          indent=4)

    def __add__(self, other):
        return Hexagon(self.coords[0] + other.coords[0],
                       self.coords[1] + other.coords[1])


def direction_vectors():
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
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True,
                          indent=4)


class Input:
    n: int
    board: List
    start: List[int]
    goal: List[int]

    def __init__(self, string):
        data = json.loads(string)
        self.__dict__ = data
