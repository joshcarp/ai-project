import json
from typing import List


class Hexagon:
    pass


class Hexagon:
    coords: (int, int)
    color: str
    previous: Hexagon
    path_cost: int

    def __init__(self, i: int, j: int):
        self.coords = (i, j)
        self.color = ""
        self.path_cost = 10000000000
        self.previous: Hexagon = None

    def __repr__(self):
        return f"{self.coords} {self.color}"

    def distance(self, other):
        return (abs(self.coords[0] - other.coords[0])
                + abs(self.coords[0] + self.coords[1] - other.coords[0] -
                      other.coords[1])
                + abs(self.coords[1] - other.coords[1])) / 2

    def __add__(self, other):
        return Hexagon(self.coords[0] + other.coords[0],
                       self.coords[1] + other.coords[1])


# function axial_distance(a, b):
#     return (abs(a.q - b.q)
#           + abs(a.q + a.r - b.q - b.r)
#           + abs(a.r - b.r)) / 2
def valid(a: (int, int), n: int) -> bool:
    return a[0] in range(0, n) and a[1] in range(0, n)


def direction_vectors() -> List[Hexagon]:
    return [Hexagon(+1, 0), Hexagon(+1, -1), Hexagon(0, -1),
            Hexagon(-1, 0), Hexagon(-1, +1), Hexagon(0, +1)]


class Input:
    n: int
    board: List
    start: List[int]
    goal: List[int]

    def __init__(self, string):
        data = json.loads(string)
        self.__dict__ = data


class Board:
    pieces: List[List[Hexagon]]
    start: Hexagon
    goal: Hexagon
    taken: {Hexagon}
    n: int

    def __init__(self, input: Input):
        if input is None:
            return
        self.n = input.n
        self.pieces = []
        for i in range(input.n):
            self.pieces.append([])
            for j in range(input.n):
                new_piece = Hexagon(i, j)
                self.pieces[i].append(new_piece)
        self.start = self.piece(input.start[0], input.start[1])
        self.goal = self.piece(input.goal[0], input.goal[1])

        for elem in input.board:
            self.piece(elem[1], elem[2]).color = elem[0]

    def copy(self):
        a: Board = Board(None)
        a.__dict__ = self.__dict__
        return a

    def __repr__(self):
        return f"{self.pieces}"

    def piece(self, x: int, y: int) -> Hexagon:
        return self.pieces[x][y]

    def piece_tuple(self, x: (int, int)) -> Hexagon:
        return self.pieces[x[0]][x[1]]

    def color(self, loc: (str, int, int)):
        self.pieces[loc[1]][loc[2]].color = loc[0]


def neighbours(self: Hexagon, board: Board) -> [Hexagon]:
    return [board.piece_tuple((self + a).coords) for a in direction_vectors()
            if
            valid((self + a).coords, board.n)
            and
            board.piece((self + a).coords[0], (self + a).coords[1]).color == ""
            ]
