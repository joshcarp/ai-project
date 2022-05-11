"""
evaluation.py contains functions dedicated to calculating the
evaluation of a particular board state
"""
from Team_Joshua_s import utils, board, hexagon


def capturable(brd: board.Board, color: str) -> int:
    """
    caapturable returns the number of immediately capture-able pieces by color.
    :param brd: bard
    :param color: color player making the capture
    :return: number of capturable plays
    """
    return triangles(brd, utils.next(color), neigh_color=color)


def triangles(brd: board.Board, color: str, neigh_color: str = None) -> int:
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
    for piece in brd.filter_pieces(color_filter):
        pieceneighs = brd.neighbours(piece, neigh_color_filter)
        for neigh in pieceneighs:
            neighneigh = set(brd.neighbours(neigh, neigh_color_filter))
            if len(neighneigh.intersection(pieceneighs)) != 0:
                count += 1
    # divide by 6 because for every triangle the increment will be 6
    if color == neigh_color:
        return count // 6
    return count // 2


def double_bridge(brd: board.Board, color: str):
    """
    counts the number of double bridge plays for color
    :param brd: a board
    :param color: the color making the play
    :return: number of double bridge plays for color
    """
    return diamonds(brd, color, "")


def diamonds(brd: board.Board, color: str, diag_color: str = None) -> int:
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
    for piece in brd.filter_pieces(color_filter):
        pieceneighs = brd.neighbours(piece, off_color_filter)
        neighs = {frozenset({p, q}) for p in pieceneighs for q in
                  pieceneighs if
                  p.color == diag_color and q.color == diag_color and
                  p.distance(
                      q) == 1}

        def neighbours(one, two):
            intersection = set(brd.neighbours(
                one, color_filter)).intersection(
                set(brd.neighbours(
                    two, color_filter)))
            if piece in intersection:
                intersection.remove(piece)
            return intersection

        s = [
            x for x in [neighbours(a, b) for (a, b) in neighs] if
            len(x) > 0]
        count += len(s)

    # divide by 4 because for every diamond the increment will be 4
    return count // 2


def distance_to_win(brd: board.Board,
                    color: str) -> ([hexagon.Hexagon],
                                    int):
    """
    returns the number of tiles color has to until a win is made
    :return:
    :param brd: a board
    :param color: a color
    :return: the path of shortest win, path cost
    """
    last_eval = brd.distances_cache[color]
    if last_eval is not None:
        last_action = brd.last_action
        if last_action is not None and (
                last_action.r,
                last_action.q) not in last_eval[0]:
            last_eval = ([brd.piece(*x.coords)
                          for x in last_eval[0]], last_eval[1])
            brd.distances_cache[color] = last_eval
            return last_eval

    start_line, end_line = utils.start_end_line(brd, color)
    if color == "red":
        start = hexagon.Hexagon(brd.n, brd.n // 2)
        end = hexagon.Hexagon(-1, brd.n // 2)
    else:
        start = hexagon.Hexagon(brd.n // 2, -1)
        end = hexagon.Hexagon(brd.n // 2, brd.n)

    start.custom_neighbours = start_line
    start.color = color
    end.color = color
    end.custom_neighbours = end_line

    for elem in end_line:
        elem.custom_neighbours = [end]
    res = brd.a_star(color, start, end)
    res = (res[0][1:-1], res[1])
    brd.distances_cache[color] = res
    return res


# win_one_away indicates that the win is one away.
win_one_away = 10000000

# win_one_away indicates that the board is already in a winning state.
win_immediate = 100000000

# indicates either a win for the player or a win for the opponent.
special_values = [x * win_immediate for x in [1, -1]]


def distance_score(brd: board.Board, our: str) -> float:
    """
    distance of score for a particular color
    :param brd: a board
    :param our: the color that the player is
    :return: a distance score of how important this piece is
    """
    score = 0
    foo, distance = distance_to_win(brd, our)
    if distance == 1:
        return win_one_away
    if distance == 0:
        return win_immediate
    else:
        score = 1 / distance

    foo, distance = distance_to_win(brd, utils.next(our))
    if distance == 1:
        return - win_one_away
    if distance == 0:
        return - win_immediate
    else:
        score -= 1 / distance

    return score


def evaluate(brd: board.Board, color: str) -> float:
    """
    returns the evaluation score of this board for a color.
    :param brd: a Board
    :param color: color to ealuate for
    :return: a evaluation score of how desirable the state is.
    """
    distance = distance_score(brd, color)
    if distance in special_values:
        return distance
    triangle = triangles(brd, color) - \
        triangles(brd, utils.next(color))
    double_pat = double_bridge(brd, color) - \
        double_bridge(brd, utils.next(color))
    capture = capturable(brd, color) - \
        capturable(brd, utils.next(color))
    return 10 * distance + 0.1 * triangle + 0.05 * double_pat + 0.4 * capture
