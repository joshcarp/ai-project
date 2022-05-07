import json
from collections import namedtuple
from copy import copy
from math import inf
from sys import argv
from typing import List, Union, Callable

from Team_Joshua_s import util


class Hexagon:
    pass


Action = namedtuple('Action', 'player type r q')
Action.__new__.__defaults__ = (None,) * len(Action._fields)

Mutation = namedtuple('Mutation', 'color turn r q')


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

    def __init__(self, i: int, j: int, color=None):
        self.coords = (i, j)
        self.incr_cost = 1
        self.total_cost: Union[int, float] = inf
        if color is not None:
            self.color = color

    def __repr__(self):
        return f"({self.coords[0]},{self.coords[1]})"

    def distance(self, othr) -> int:
        """
        distance returns the amount of places from the current hexagon to
        another hexagon.
        The algorithm was adapted from
        https://www.redblobgames.com/grids/hexagons/#distances
        Copyright © 2022 Red Blob Games.
        """
        x = self.coords[0] - othr.coords[0]
        xy = (self.coords[0] + self.coords[1]) - \
             (othr.coords[0] + othr.coords[1])
        y = self.coords[1] - othr.coords[1]
        return (abs(x) + abs(xy) + abs(y)) / 2

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

    # def set_color(self, color: str):
    #     """
    #     set_color sets the current Hexagon's color to the input string and
    #     sets the incremental cost to infinity
    #     """
    #     self.color = color
    #     self.incr_cost = inf

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

    def __init__(self, string: Union[str, None] = None):
        if string is None:
            return
        data = json.loads(string)
        self.__dict__ = data


class Board:
    """
    Board controls all the information about the state and implements the
    path finding algorithm
    """
    mutations: List[List[List[Mutation]]]
    start: Hexagon
    goal: Hexagon
    n: int
    turn_num: int = 0
    last_action: Action = None

    def pieces(self) -> List[List[Hexagon]]:
        pieces: List[List[Hexagon]] = []
        for i in range(self.n):
            pieces.append([])
            for j in range(self.n):
                color = ""
                if len(self.mutations[i][j]) > 0:
                    color = self.mutations[i][j][-1].color
                pieces[i].append(Hexagon(i, j, color))
        return pieces

    def __init__(self, n):
        self.n = n
        self.mutations = []
        for i in range(n):
            self.mutations.append([])
            for j in range(n):
                self.mutations[i].append([])

    def __repr__(self):
        return util.board_string(*self.dict())

    def dict(self) -> (int, {}):
        d: {} = {}
        for list in self.pieces():
            for e in list:
                if e.color != "":
                    d[e.coords] = e.color
        return self.n, d

    def filter_pieces(self,
                      filter: Callable[[Hexagon], bool] = lambda x: True):
        return [e for sub in self.pieces() for e in sub if filter(e)]

    def piece(self, x: int, y: int) -> Hexagon:
        """
        piece returns the Hexagon at coordinates (x, y)
        """
        return self.pieces()[x][y]

    def piece_tuple(self, x: (int, int)) -> Hexagon:
        """
        piece_tuple returns the Hexagon at coordinates (x[0], x[1])
        """
        return self.pieces()[x[0]][x[1]]

    def valid(self, piece: Hexagon) -> bool:
        """
        valid returns True if the hexagon specified exists within the board
        and False otherwise.
        """
        return piece.coords[0] in range(0, self.n) and \
            piece.coords[1] in range(0, self.n)

    def process_action(b, action: Action, turn: int) -> List[Mutation]:
        coords = (action.r, action.q)
        changed = [Mutation(action.player, turn, action.r, action.q)]

        def filter1(x):
            return x.color != action.player and x.color != ""

        def filter2(x):
            return x.color == action.player and x.color != ""

        neighs = b.neighbours(b.piece(*coords), filter=filter1)
        seen: {Hexagon: Hexagon} = {}
        for elem in neighs:
            if elem.color == action.player or elem.color == "":
                continue
            if elem.coords == coords:
                continue
            neighneighs = b.neighbours(elem, filter=filter2)
            for elem2 in neighneighs:
                if elem2.coords in seen.keys(
                ) and seen[elem2.coords].color == elem.color:
                    changed.append(Mutation("", turn, *elem.coords))
                    changed.append(
                        Mutation("", turn, *seen[elem2.coords].coords))
                    return changed
                seen[elem2.coords] = elem
        return changed

    def action(self, action: Action):
        cpy: Board = copy(self)
        cpy.turn_num += 1
        changed = []
        if action.type == "STEAL":
            changed.append(
                Mutation(
                    action.player,
                    cpy.turn_num,
                    self.last_action.r,
                    self.last_action.q))
        elif action.type == "PLACE":
            changed.extend(cpy.process_action(action, cpy.turn_num))
            cpy.last_action = action
        for elem in changed:
            cpy.mutations[elem.r][elem.q].append(elem)
        return cpy

    def neighbours(self, piece: Hexagon, filter: Callable[[
            Hexagon], bool] = lambda
            x: x.color == "") -> [Hexagon]:
        """
        neighbours returns a list of Hexagons that exist within the board
        that don't already have a color.
        """
        return [self.piece_tuple((piece + a).coords) for a in
                direction_vectors() if
                self.valid(piece + a) and
                filter(self.piece_tuple((piece + a).coords))]

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
            if len(opened) == 0:
                return []
            current = opened.pop()
            closed.append(current)
            for neigh in self.neighbours(current):
                # neigh_path_cost is the cost to get to the neighbour
                # from the current node
                neigh_path_cost = current.total_cost + neigh.incr_cost
                # if the neighbours already existing cost is less than
                # the current node then the current nodes previous
                # becomes the neighbour
                if neigh.total_cost < neigh_path_cost and neigh in closed:
                    current.total_cost = neigh.total_cost + current.incr_cost
                    current.previous = neigh
                # if the neighbours total existing cost is more than getting
                # to the neighbour through the current node then set
                # neighbours previous to the current node
                elif neigh.total_cost > neigh_path_cost and neigh in opened:
                    neigh.total_cost = neigh_path_cost
                    neigh.previous = current
                # if neighbour is not in open then we will add it to be
                # expanded next iteration
                if neigh not in closed and neigh not in opened:
                    neigh.total_cost = neigh_path_cost
                    opened.append(neigh)
        # current at this point is goal, so traverse back to start and return
        # the list
        return current.get_path()

    def __copy__(self):
        newboard = Board(self.n)
        for i in range(self.n):
            for j in range(self.n):
                newboard.mutations[i][j] = self.mutations[i][j].copy()
        return newboard


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
