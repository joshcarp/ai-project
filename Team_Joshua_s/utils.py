"""
COMP30024 Artificial Intelligence, Semester 1, 2022
Project Part B

This module contains some helper functions for printing actions and boards.
Feel free to use and/or modify them to help you develop your program.
"""
from collections import namedtuple


# Action is a convenience and is more self documenting than using raw tuples.
Action = namedtuple('Action', 'player type r q')
Action.__new__.__defaults__ = (None,) * len(Action._fields)


def next(current: str) -> str:
    """
    returns the player that will play next
    :param current:
    :return:
    """
    if current == "red":
        return "blue"
    return "red"


def direction_vectors() -> [(int, int)]:
    """
    direction_vectors returns vectors representing all the 6 ways one can move
    from a single piece to other pieces as other Hexagons.
    """
    return [(+1, 0), (+1, -1), (0, -1), (-1, 0), (-1, +1), (0, +1)]


def start_end_line(self, color: str):
    """
    returns the start and end line for a particular color.
    for red it will be the top and bottom, for blue it will be left and right.
    """
    if color == "red":
        def start_f(x): return self.piece(0, x)
        def end_f(x): return self.piece(self.n - 1, x)
    else:
        def start_f(x): return self.piece(x, 0)
        def end_f(x): return self.piece(x, self.n - 1)

    start = [x for x in [start_f(i) for i in range(0, self.n)] if
             x.color != next(color)]
    end = [x for x in [end_f(i) for i in range(0, self.n)] if
           x.color != next(color)]
    return start, end
