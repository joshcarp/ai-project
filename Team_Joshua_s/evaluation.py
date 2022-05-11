from Team_Joshua_s import utils, search, hexagon


def capturable(brd: search.Board, color: str) -> int:
    return triangles(brd, utils.next(color), neigh_color=color)


def triangles(brd: search.Board, color: str, neigh_color: str = None) -> int:
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


def double_bridge(brd: search.Board, color: str):
    return diamonds(brd, color, "")


def diamonds(brd: search.Board, color: str, diag_color: str = None) -> int:
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


def distance_to_win(brd: search.Board,
                    color: str) -> ([hexagon.Hexagon],
                                    int):
    """
    returns the number of tiles color has to until a connection is made
    :return:
    """
    last_eval = brd.distances_cache[color]
    if last_eval is not None:
        last_action = brd.last_action
        if last_action is not None and (
                last_action.r,
                last_action.q) not in last_eval[0]:
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
