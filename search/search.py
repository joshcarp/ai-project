import json
from typing import List


class Color:
    name: str


class Square:
    pass


class Square:
    color: Color
    neighbours: List[Square]

    def __init__(self):
        pass


class Board:
    pieces: List[List[Square]]


class Input:
    n: int
    board: List
    start: List[int]
    goal: List[int]
    def __init__(self, string):
        data = json.loads(string)
        self.__dict__ = data


