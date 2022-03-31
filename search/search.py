import json
import os
import sys
import typing
from math import inf
from typing import List
from typing import Union


class Hexagon:
    pass


class Hexagon:
    coords: (int, int)
    color: str
    previous: Hexagon
    path_cost: Union[int, float]
    piece_value: int

    def __init__(self, i: int, j: int):
        self.coords = (i, j)
        self.color = ""
        self.piece_value = 1
        self.path_cost: Union[int, float] = inf
        self.previous: Union[Hexagon, None] = None

    def __repr__(self):
        return f"({self.coords[0]},{self.coords[1]})"

    def distance(self, other) -> int:
        return (abs(self.coords[0] - other.coords[0])
                + abs(self.coords[0] + self.coords[1] - other.coords[0] -
                      other.coords[1])
                + abs(self.coords[1] - other.coords[1])) / 2

    def get_path(self) -> List[Hexagon]:
        elems: List[Hexagon] = []
        current = self
        while current is not None:
            elems.append(current)
            current = current.previous
        elems.reverse()
        return elems

    def set_color(self, color: str):
        self.color = color
        self.piece_value = inf

    def __add__(self, other):
        return Hexagon(self.coords[0] + other.coords[0],
                       self.coords[1] + other.coords[1])


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

    def __init__(self, input: Union[Input, None]):
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
        self.pieces[loc[1]][loc[2]].set_color(loc[0])

    def neighbours(self, piece: Hexagon) -> [Hexagon]:
        return [self.piece_tuple((piece + a).coords) for a in
                direction_vectors()
                if
                valid((piece + a).coords, self.n)
                and
                self.piece((piece + a).coords[0],
                           (piece + a).coords[1]).color == ""
                ]

    def a_star(self) -> List[Hexagon]:
        current: Hexagon = self.start
        closed_nodes: typing.List[Hexagon] = []
        open_nodes: typing.List[Hexagon] = [current]
        current.path_cost = 0
        while current.coords != self.goal.coords:
            open_nodes.sort(
                key=lambda x: x.distance(self.goal) + x.path_cost,
                reverse=True
            )
            current = open_nodes.pop()
            closed_nodes.append(current)
            for elem in self.neighbours(current):
                current_path_cost = current.path_cost + elem.piece_value
                if elem.path_cost < current_path_cost and elem in closed_nodes:
                    current.path_cost = elem.path_cost + elem.piece_value
                    current.previous = elem
                elif elem.path_cost < current_path_cost and elem in open_nodes:
                    elem.path_cost = current_path_cost + elem.piece_value
                    elem.previous = current
                if elem not in closed_nodes and elem not in open_nodes:
                    elem.path_cost = current_path_cost
                    open_nodes.append(elem)
        return current.get_path()


def format_output(path: List[Hexagon]) -> str:
    pathstr = "\n".join([x.__str__() for x in path])
    return f"{len(path)}\n{pathstr}"


def main(jsonstr: str) -> str:
    raw_input: Input = Input(jsonstr)
    board: Board = Board(raw_input)
    solution = board.a_star()
    return format_output(solution)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("must supply json file argument")
        exit(1)
    file = open(sys.argv[1], "r")
    jsonstr = file.read()
    print(main(jsonstr))
