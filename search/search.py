import json
from math import inf
from sys import argv
from typing import List, Union


class Hexagon:
    pass


class Hexagon:
    """
    Hexagon is an encapsulation of all piece related information and
    also serves as a linked list for defining the path from the end
    piece to the start
    """
    # coords is the coordinates of this current piece.
    coords: (int, int) = (-1, -1)
    # color represents the color that this node is as a string.
    color: str = ""
    # total_cost represents the current cost to get from the start node.
    # to this one
    total_cost: float = 0
    # incr_cost represents the incremental cost to take this node.
    incr_cost: float = 0
    # previous represents the previous node that was taken before this one
    # traversing this at the end of an algorithm will end back at the start
    # node.
    previous: Union[Hexagon, None] = None

    def __init__(self, i: int, j: int):
        self.coords = (i, j)
        self.incr_cost = 1
        self.total_cost: Union[int, float] = inf

    def __repr__(self):
        return f"({self.coords[0]},{self.coords[1]})"

    def distance(self, other) -> int:
        """
        distance returns the amount of places from the current hexagon to
        another hexagon.
        The algorithm was adapted from
        https://www.redblobgames.com/grids/hexagons/#distances
        Copyright © 2022 Red Blob Games.
        """
        return (abs(self.coords[0] - other.coords[0])
                + abs(self.coords[0] + self.coords[1] - other.coords[0] -
                      other.coords[1])
                + abs(self.coords[1] - other.coords[1])) / 2

    def get_path(self) -> List[Hexagon]:
        """
        get_path traverses from the end node back to the start node
        and returns an in order list of the path.
        """
        elems: List[Hexagon] = []
        current = self
        while current is not None:
            elems.append(current)
            current = current.previous
        elems.reverse()
        return elems

    def set_color(self, color: str):
        """
        set_color sets the current Hexagon's color to the input string
        """
        self.color = color
        self.incr_cost = inf

    def __add__(self, other):
        return Hexagon(self.coords[0] + other.coords[0],
                       self.coords[1] + other.coords[1])


def direction_vectors() -> List[Hexagon]:
    """
    direction_vectors returns vectors representing all the 6 ways one can move
    from a single piece to other pieces as other Hexagons.
    """
    return [Hexagon(+1, 0), Hexagon(+1, -1), Hexagon(0, -1),
            Hexagon(-1, 0), Hexagon(-1, +1), Hexagon(0, +1)]


class Input:
    """
    Input is the raw input which exists to strongly type
    the input json expected instead of operating on dictionaries.
    """
    n: int = 0
    board: List = []
    start: List[int] = []
    goal: List[int] = []

    def __init__(self, string):
        data = json.loads(string)
        self.__dict__ = data


class Board:
    """
    Board controls all the information about the state and implements the
    path finding algorithm
    """
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

    def __repr__(self):
        return f"{self.pieces}"

    def piece(self, x: int, y: int) -> Hexagon:
        """
        piece returns the Hexagon at coordinates (x, y)
        """
        return self.pieces[x][y]

    def piece_tuple(self, x: (int, int)) -> Hexagon:
        """
        piece_tuple returns the Hexagon at coordinates (x[0], x[1])
        """
        return self.pieces[x[0]][x[1]]

    def valid(self, piece: Hexagon) -> bool:
        """
        valid returns True if the hexagon specified exists within the board
        and False otherwise.
        """
        return piece.coords[0] in range(0, self.n) and \
            piece.coords[1] in range(0, self.n)

    def neighbours(self, piece: Hexagon) -> [Hexagon]:
        """
        neighbours returns a list of Hexagons that exist within the board
        that don't already have a color.
        """
        return [self.piece_tuple((piece + a).coords) for a in
                direction_vectors() if
                self.valid(piece + a) and
                self.piece_tuple((piece + a).coords).color == ""]

    def a_star(self) -> List[Hexagon]:
        """
        a_star implements the a star algorithm and returns the path
        from start to end. the start Hexagon will be return[0] and
        the end hexagon will be return[-1].
        """
        current = self.start
        closed: List[Hexagon] = []
        opened: List[Hexagon] = [current]
        current.total_cost = 0
        while current.coords != self.goal.coords:
            opened.sort(
                key=lambda x: x.distance(self.goal) + x.total_cost,
                reverse=True
            )
            current = opened.pop()
            closed.append(current)
            for neigh in self.neighbours(current):
                neigh_path_cost = current.total_cost + neigh.incr_cost
                if neigh.total_cost < neigh_path_cost and neigh in closed:
                    current.total_cost = neigh.total_cost + current.incr_cost
                    current.previous = neigh
                elif neigh.total_cost > neigh_path_cost and neigh in opened:
                    neigh.total_cost = neigh_path_cost + neigh.incr_cost
                    neigh.previous = current
                if neigh not in closed and neigh not in opened:
                    neigh.total_cost = neigh_path_cost
                    opened.append(neigh)
        return current.get_path()


def format_output(path: List[Hexagon]) -> str:
    """
    format_output takes a list of hexagon
    and returns the expected format string.
    """
    pathstr = "\n".join([x.__str__() for x in path])
    return f"{len(path)}\n{pathstr}"


def main(jsonstr: str) -> str:
    """
    main parses a json string and returns the result output as a string.
    """
    raw_input: Input = Input(jsonstr)
    board: Board = Board(raw_input)
    solution = board.a_star()
    return format_output(solution)


# parse os args and call main.
if __name__ == "__main__":
    if len(argv) != 2:
        print("must supply json file argument")
        exit(1)
    file = open(argv[1], "r")
    jsonstr = file.read()
    print(main(jsonstr))
