import json
from math import inf
from sys import argv
from typing import List, Union


class Hexagon:
    pass


class Hexagon:
    coords: (int, int) = (-1, -1)
    color: str = ""
    previous: Union[Hexagon, None] = None
    path_cost: Union[int, float] = 0
    piece_value: Union[int, float] = 0

    def __init__(self, i: int, j: int):
        self.coords = (i, j)
        self.piece_value = 1
        self.path_cost: Union[int, float] = inf

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


def direction_vectors() -> List[Hexagon]:
    return [Hexagon(+1, 0), Hexagon(+1, -1), Hexagon(0, -1),
            Hexagon(-1, 0), Hexagon(-1, +1), Hexagon(0, +1)]


class Input:
    n: int = 0
    board: List = []
    start: List[int] = []
    goal: List[int] = []

    def __init__(self, string):
        data = json.loads(string)
        self.__dict__ = data


class Board:
    pieces: List[List[Hexagon]]
    start: Hexagon
    goal: Hexagon
    n: int

    def __init__(self, input: Union[Input, None]):
        self.pieces = []
        if input is None:
            return
        self.n = input.n
        for i in range(input.n):
            self.pieces.append([])
            for j in range(input.n):
                new_piece = Hexagon(i, j)
                self.pieces[i].append(new_piece)
        if len(input.start) >= 2:
            self.start = self.piece(input.start[0], input.start[1])
        if len(input.goal) >= 2:
            self.goal = self.piece(input.goal[0], input.goal[1])
        for elem in input.board:
            self.piece(elem[1], elem[2]).set_color(elem[0])

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

    def valid(self, piece: Hexagon) -> bool:
        return piece.coords[0] in range(0, self.n) and piece.coords[
            1] in range(0, self.n)

    def neighbours(self, piece: Hexagon) -> [Hexagon]:
        return [self.piece_tuple((piece + a).coords) for a in
                direction_vectors()
                if self.valid(piece + a)
                and self.piece((piece + a).coords[0],
                               (piece + a).coords[1]).color == ""]

    def a_star(self) -> List[Hexagon]:
        current = self.start
        closed: List[Hexagon] = []
        opened: List[Hexagon] = [current]
        current.path_cost = 0
        while current.coords != self.goal.coords:
            opened.sort(
                key=lambda x: x.distance(self.goal) + x.path_cost,
                reverse=True
            )
            current = opened.pop()
            closed.append(current)
            for neigh in self.neighbours(current):
                neighbour_path_cost = current.path_cost + neigh.piece_value
                if neigh.path_cost < neighbour_path_cost and neigh in closed:
                    current.path_cost = neigh.path_cost + current.piece_value
                    current.previous = neigh
                elif neigh.path_cost > neighbour_path_cost and neigh in opened:
                    neigh.path_cost = neighbour_path_cost + neigh.piece_value
                    neigh.previous = current
                if neigh not in closed and neigh not in opened:
                    neigh.path_cost = neighbour_path_cost
                    opened.append(neigh)
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
    if len(argv) != 2:
        print("must supply json file argument")
        exit(1)
    file = open(argv[1], "r")
    jsonstr = file.read()
    print(main(jsonstr))
