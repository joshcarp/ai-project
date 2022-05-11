import math
import sys
from typing import Union


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

    previous: Union[Hexagon, None]

    custom_neighbours: []

    def __init__(self, i: int, j: int, color=None):
        self.custom_neighbours = None
        self.coords = (i, j)
        self.total_cost: Union[int, float] = math.inf
        self.previous = None
        if color is not None:
            self.color = color

    def incr_cost(self, player: str) -> float:
        """
        returns the incremental cost for player on current node.
        :param player:
        :return:
        """
        if self.color == player:
            return sys.float_info.epsilon
        if self.color == "":
            return 1
        return math.inf

    def reset_search(self):
        """
        resets the Hexagon's previous and total_cost attributes.
        """
        self.previous = None
        self.total_cost = math.inf

    def end_search(self):
        """
        used to reset search when modified a star algorithm is used.
        """
        self.reset_search()
        self.custom_neighbours = None

    def __repr__(self):
        return f"({self.coords[0]},{self.coords[1]})"

    def __key(self):
        return self.coords

    def __eq__(self, other):
        if not isinstance(other, Hexagon):
            return self.__key() == other
        return self.__key() == other.__key()

    def __hash__(self):
        return hash(self.__key())

    def __add__(self, other):
        return Hexagon(self.coords[0] + other[0],
                       self.coords[1] + other[1])

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
        dist = (abs(x) + abs(xy) + abs(y)) / 2
        return dist
