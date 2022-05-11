from collections import namedtuple

Action = namedtuple('Action', 'player type r q')
Action.__new__.__defaults__ = (None,) * len(Action._fields)


def next(current: str) -> str:
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
