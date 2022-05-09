from collections import namedtuple
from copy import copy
from math import inf
from typing import List, Union, Callable

from Team_Joshua_s import util

Action = namedtuple('Action', 'player type r q')
Action.__new__.__defaults__ = (None,) * len(Action._fields)


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

    def __init__(self, i: int, j: int, color=None):
        self.coords = (i, j)
        self.incr_cost = 1
        self.total_cost: Union[int, float] = inf
        if color is not None:
            self.color = color

    def r(self):
        return self.coords[0]

    def q(self):
        return self.coords[1]

    def __repr__(self):
        return f"({self.coords[0]},{self.coords[1]})"

    def __eq__(self, other):
        return self.coords == other.coords and self.color == other.color

    def __hash__(self):
        return hash(self.coords)

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


class Board:
    """
    Board controls all the information about the state and implements the
    path finding algorithm
    """
    mutations: List[List[List[Hexagon]]]
    n: int
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
                self.mutations[i].append([Hexagon(i, j)])

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
        pieces = []
        for i in range(self.n):
            for j in range(self.n):
                hex = Hexagon(i, j, self.mutations[i][j][-1].color)
                if filter(hex):
                    pieces.append(hex)
        return pieces

    def piece(self, x: int, y: int) -> Hexagon:
        """
        piece returns the Hexagon at coordinates (x, y)
        """
        return Hexagon(x, y, self.mutations[x][y][-1].color)

    def valid(self, piece: Hexagon) -> bool:
        """
        valid returns True if the hexagon specified exists within the board
        and False otherwise.
        """
        return piece.coords[0] in range(0, self.n) and \
            piece.coords[1] in range(0, self.n)

    def triangles(self, color: str) -> int:
        """
        triangles returns the number of triangles of a particular color in
        the board counted in any orientation.
        :return:
        """

        def color_filter(x):
            return x.color == color

        count = 0
        for piece in self.filter_pieces(color_filter):
            pieceneighs = self.neighbours(piece, color_filter)
            for neigh in pieceneighs:
                neighneigh = self.neighbours(neigh, color_filter)
                if len(neighneigh.intersection(pieceneighs)) != 0:
                    count += 1
        # divide by 6 because for every triangle the increment will be 6
        return count // 6

    def diamonds(self, color: str) -> int:
        """
        diamonds returns the number of diamonds of a particular color in
        the board
        :return:
        """

        def color_filter(x):
            return x.color == color

        count = 0
        for piece in self.filter_pieces(color_filter):
            pieceneighs = self.neighbours(piece, color_filter)
            neighs = {frozenset({p, q}) for p in pieceneighs for q in
                      pieceneighs if p in self.neighbours(
                q, color_filter) and q in self.neighbours(p, color_filter)}

            def neighbours(one, two):
                intersection = self.neighbours(
                    one, color_filter).intersection(
                    self.neighbours(
                        two, color_filter))
                if piece in intersection:
                    intersection.remove(piece)
                return intersection

            s = [
                x for x in [
                    neighbours(
                        a,
                        b) for (
                        a,
                        b) in neighs] if len(x) > 0]
            count += len(s)

        # divide by 4 because for every diamond the increment will be 4
        return count // 2

    def process_action(b, action: Action) -> List[Hexagon]:
        coords = (action.r, action.q)
        changed = [Hexagon(action.r, action.q, action.player)]

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
                    changed.append(Hexagon(*elem.coords))
                    changed.append(
                        Hexagon(*seen[elem2.coords].coords))
                    return changed
                seen[elem2.coords] = elem
        return changed

    def action(self, action: Action):
        cpy: Board = copy(self)
        changed = []
        if action.type == "STEAL":
            changed.append(
                Hexagon(
                    self.last_action.r,
                    self.last_action.q,
                    action.player))
        elif action.type == "PLACE":
            changed.extend(cpy.process_action(action))
            cpy.last_action = action
        for elem in changed:
            cpy.mutations[elem.r()][elem.q()].append(elem)
        return cpy

    def neighbours(self, piece: Hexagon, filter: Callable[[
            Hexagon], bool] = lambda
            x: x.color == "") -> {Hexagon}:
        """
        neighbours returns a list of Hexagons that exist within the board
        that don't already have a color.
        """
        return {self.piece(*(piece + a).coords) for a in
                direction_vectors() if
                self.valid(piece + a) and
                filter(self.piece(*(piece + a).coords))}

    def __copy__(self):
        newboard = Board(self.n)
        newboard.last_action = self.last_action
        for i in range(self.n):
            for j in range(self.n):
                newboard.mutations[i][j] = self.mutations[i][j].copy()
        return newboard
