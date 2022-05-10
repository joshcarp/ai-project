import math
import sys
from collections import namedtuple
from copy import copy
from math import inf
from typing import List, Union, Callable

from Team_Joshua_s import util

Action = namedtuple('Action', 'player type r q')
Action.__new__.__defaults__ = (None,) * len(Action._fields)


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

    previous: Union[Hexagon, None] = None

    def __init__(self, i: int, j: int, color=None):
        self.coords = (i, j)
        self.total_cost: Union[int, float] = inf
        if color is not None:
            self.color = color

    def incr_cost(self, player: str) -> float:
        if self.color == player:
            return sys.float_info.epsilon
        if self.color == "":
            return 1
        return math.inf

    def reset_search(self):
        self.previous = None
        self.total_cost = math.inf

    def r(self):
        return self.coords[0]

    def q(self):
        return self.coords[1]

    def __repr__(self):
        return f"({self.coords[0]},{self.coords[1]})"

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(self.coords)

    def __add__(self, other):
        return Hexagon(self.coords[0] + other.coords[0],
                       self.coords[1] + other.coords[1])

    def get_path(self, start=None, player="") -> [List[Hexagon], int]:
        """
        get_path traverses from the end node back to the start node
        and returns an in order list of the path.
        """
        elems: List[Hexagon] = []
        current = self
        cost = 0
        while current is not None:
            elems.append(current)
            cost += current.incr_cost(player)
            current = current.previous
        elems.reverse()
        if start is not None and elems[0] != start:
            raise Exception
        return elems, cost

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

    # TODO: @joshcarp delete this
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
        d: {} = {}
        for list in self.pieces():
            for e in list:
                if e.color != "":
                    d[e.coords] = e.color
        return util.board_string(self.n, d)

    def filter_pieces(self,
                      filter: Callable[[Hexagon], bool] = lambda x: True):
        pieces = []
        for i in range(self.n):
            for j in range(self.n):
                hex = self.mutations[i][j][-1]
                if filter(hex):
                    pieces.append(hex)
        return pieces

    def piece(self, x: int, y: int) -> Hexagon:
        """
        piece returns the Hexagon at coordinates (x, y)
        """
        return self.mutations[x][y][-1]

    def valid(self, piece: Hexagon) -> bool:
        """
        valid returns True if the hexagon specified exists within the board
        and False otherwise.
        """
        return piece.coords[0] in range(0, self.n) and \
            piece.coords[1] in range(0, self.n)

    def capturable(self, color: str) -> int:
        return self.triangles(next_player(color), neigh_color=color)

    def triangles(self, color: str, neigh_color: str = None) -> int:
        """
        triangles returns the number of triangles of a particular color in
        the board counted in any orientation.
        :return:
        """
        if neigh_color is None:
            neigh_color = color

        def color_filter(x):
            return x.color == color

        def neigh_color_filter(x):
            return x.color == neigh_color

        count = 0
        for piece in self.filter_pieces(color_filter):
            pieceneighs = self.neighbours(piece, neigh_color_filter)
            for neigh in pieceneighs:
                neighneigh = set(self.neighbours(neigh, neigh_color_filter))
                if len(neighneigh.intersection(pieceneighs)) != 0:
                    count += 1
        # divide by 6 because for every triangle the increment will be 6
        if color == neigh_color:
            return count // 6
        return count // 2

    def diamonds(self, color: str, diag_color: str = None) -> int:
        """
        diamonds returns the number of diamonds of a particular color in
        the board
        :return:
        """
        if diag_color is None:
            diag_color = color

        def color_filter(x):
            return x.color == color

        def off_color_filter(x):
            return x.color == diag_color

        count = 0
        for piece in self.filter_pieces(color_filter):
            pieceneighs = self.neighbours(piece, off_color_filter)
            neighs = {frozenset({p, q}) for p in pieceneighs for q in
                      pieceneighs if p in self.neighbours(
                q, off_color_filter) and q in
                self.neighbours(p, off_color_filter)}

            def neighbours(one, two):
                intersection = set(self.neighbours(
                    one, color_filter)).intersection(
                    set(self.neighbours(
                        two, color_filter)))
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

    def start_end_line(self, color: str):
        if color == "red":
            bottom = [
                x for x in [
                    self.piece(
                        0,
                        i) for i in range(
                        0,
                        self.n)] if x.color != next_player(color)]
            top = [
                x for x in [
                    self.piece(
                        self.n - 1,
                        i) for i in range(
                        0,
                        self.n)] if x.color != next_player(color)]
            return top, bottom
        if color == "blue":
            left = [
                x for x in [
                    self.piece(
                        i,
                        0) for i in range(
                        0,
                        self.n)] if x.color != next_player(color)]
            right = [
                x for x in [
                    self.piece(
                        i,
                        self.n -
                        1) for i in range(
                        0,
                        self.n)] if x.color != next_player(color)]
            return left, right

    def distance_to_win(self, color: str) -> int:
        """
        returns the number of tiles color has to until a connection is made
        :return:
        """
        start_line, end_line = self.start_end_line(color)
        distances = []
        for start in start_line:
            for end in end_line:
                path, cost = self.a_star(color, start.coords, end.coords)
                distances.append((path, cost))
        if len(distances) == 0:
            return ([], math.inf)
        return min(distances, key=lambda x: x[1])

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
            x: x.color == "") -> [Hexagon]:
        """
        neighbours returns a list of Hexagons that exist within the board
        that don't already have a color.
        """
        # would use a set here but set values are copies and not references
        return [self.piece(*(piece + a).coords) for a in
                direction_vectors() if
                self.valid(piece + a) and
                filter(self.piece(*(piece + a).coords))]

    def a_star(
            self, player: str, start: (
                int, int), end: (
                int, int)) -> ([Hexagon], int):
        """
        a_star implements the a star algorithm and returns the path
        from start to end. the start Hexagon will be return[0] and
        the end hexagon will be return[-1].
        """
        self.filter_pieces(lambda x: x.reset_search())
        current = self.piece(*start)
        end = self.piece(*end)
        closed: List[Hexagon] = []
        opened: List[Hexagon] = [current]
        current.total_cost = current.incr_cost(player)
        while current.coords != end.coords:
            opened.sort(
                key=lambda x: x.distance(end) + x.total_cost,
                reverse=True
            )
            if len(opened) == 0:
                return [], math.inf
            current = opened.pop()
            closed.append(current)
            for neigh in self.neighbours(
                    current, lambda x: x.color != next_player(player)):
                # neigh_path_cost is the cost to get to the neighbour
                # from the current node
                neigh_path_cost = current.total_cost + \
                    neigh.incr_cost(player)
                # if the neighbours already existing cost is less than
                # the current node then the current nodes previous
                # becomes the neighbour
                if neigh.total_cost < neigh_path_cost and neigh in closed:
                    current.total_cost = neigh.total_cost + \
                        current.incr_cost(player)
                    current.previous = neigh
                # if the neighbours total existing cost is more than getting
                # to the neighbour through the current node then set
                # neighbours previous to the current node
                elif neigh.total_cost > \
                        neigh_path_cost and neigh in opened:
                    neigh.total_cost = neigh_path_cost
                    neigh.previous = current
                # if neighbour is not in open then we will add it to be
                # expanded next iteration
                if neigh not in closed and neigh not in opened:
                    neigh.total_cost = neigh_path_cost
                    neigh.previous = current
                    opened.append(neigh)
        # current at this point is goal, so traverse back to start and return
        # the list
        path: List[Hexagon] = []
        cost = 0
        while current is not None:
            path.append(current)
            cost += current.incr_cost(player)
            current = current.previous
        path.reverse()
        if start is not None and path[0] != start:
            raise Exception
        self.filter_pieces(lambda x: x.reset_search())
        return path, round(cost)

    def __copy__(self):
        newboard = Board(self.n)
        newboard.last_action = self.last_action
        for i in range(self.n):
            for j in range(self.n):
                newboard.mutations[i][j] = self.mutations[i][j].copy()
        return newboard


def next_player(current: str) -> str:
    if current == "red":
        return "blue"
    return "red"
