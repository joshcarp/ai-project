import math

import Team_Joshua_s.player as player
import Team_Joshua_s.search as search


# from pstats import SortKey


def testneighbours():
    board: search.Board = search.Board(5)
    tests = [
        {
            "coord": (0, 0),
            "neighbours": {(1, 0), (0, 1)}
        },
        {
            "coord": (0, 1),
            "neighbours": {(0, 0), (1, 0), (1, 1), (0, 2)}
        },
        {
            "coord": (2, 2),
            "neighbours": {(2, 1), (1, 2), (1, 3), (2, 3), (3, 2), (3, 1)}
        },
        {
            "coord": (4, 4),
            "neighbours": {(4, 3), (3, 4)}
        },
    ]

    for elem in tests:
        coord = elem["coord"]
        neighbours = board.neighbours(search.Hexagon(coord[0], coord[1]))
        assert elem["neighbours"] == {e.coords for e in neighbours}


def testplayer():
    pl = player.Player("red", 4)
    pl.turn("red", ("PLACE", 1, 0))
    print(pl.board)
    assert pl.board.piece(1, 0).color == "red"
    pl.turn("blue", ("STEAL",))
    assert pl.board.piece(1, 0).color == "blue"
    print(pl.board)
    pl.turn("blue", ("PLACE", 1, 1))
    pl.turn("red", ("PLACE", 0, 1))
    print(pl.board)
    pl.turn("red", ("PLACE", 2, 0))
    print(pl.board)
    assert pl.board.piece(0, 1).color == "red"
    assert pl.board.piece(2, 0).color == "red"
    assert pl.board.piece(1, 0).color == ""
    assert pl.board.piece(1, 1).color == ""
    # assert player.evaluate(pl.board, "red") == 2
    pl.turn("blue", ("PLACE", 1, 0))
    pl.turn("blue", ("PLACE", 1, 1))
    assert pl.board.piece(0, 1).color == ""
    assert pl.board.piece(2, 0).color == ""
    print(pl.board)
    # assert player.evaluate(pl.board, "red") == -2


# @profile

def testplayer2():

    # pr = cProfile.Profile()
    # pr.enable()
    pl = player.Player("red", 4, depth=2)
    pl2 = player.Player("blue", 4, depth=2)

    for i in range(6):
        if i == 3:
            print()
        act = pl.action()
        print(act)
        pl.turn(pl.player, act)
        pl2.turn(pl.player, act)
        print(pl.board)
        print("red: ", len(pl.board.filter_pieces(lambda x: x.color == "red")))
        print("blue: ",
              len(pl.board.filter_pieces(lambda x: x.color == "blue")))
        act = pl2.action()
        print(act)
        pl.turn(pl2.player, act)
        pl2.turn(pl2.player, act)
        print(pl.board)

        print("red: ", len(pl.board.filter_pieces(lambda x: x.color == "red")))
        print("blue: ",
              len(pl.board.filter_pieces(lambda x: x.color == "blue")))
        blank = pl.board.filter_pieces(lambda x: x.color == "")
        if len(blank) <= 2:
            break
        if i == 3:
            print()
        if pl.board.distance_to_win("blue")[1] == 0:
            print("blue is the winner")
            break
        if pl.board.distance_to_win("red")[1] == 0:
            print("red is the winner")
            break
        print(i)

    # pr.disable()
    # s = io.StringIO()
    # # sortby = SortKey.CUMULATIVE
    # ps = pstats.Stats(pr, stream=s)
    # # ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    # ps.print_stats()
    # print(s.getvalue())


def testtriangle():
    pl = player.Player("red", 4)
    pl.turn("red", ("PLACE", 1, 0))
    pl.turn("red", ("PLACE", 2, 0))
    pl.turn("red", ("PLACE", 1, 1))
    pl.turn("red", ("PLACE", 0, 2))
    pl.turn("red", ("PLACE", 1, 2))
    print(pl.board)
    print(pl.board.triangles("red"))


def testcapturable():
    pl = player.Player("red", 4)
    pl.turn("red", ("PLACE", 1, 0))
    pl.turn("blue", ("PLACE", 2, 0))
    pl.turn("red", ("PLACE", 1, 1))
    print(pl.board)
    print(pl.board.capturable("red"))
    print(pl.board.capturable("blue"))


def testdiamond():
    pl = player.Player("red", 4)
    pl.turn("red", ("PLACE", 1, 0))
    pl.turn("red", ("PLACE", 2, 0))
    pl.turn("red", ("PLACE", 1, 1))
    pl.turn("red", ("PLACE", 0, 1))

    pl.turn("red", ("PLACE", 1, 3))
    pl.turn("red", ("PLACE", 2, 2))
    pl.turn("red", ("PLACE", 2, 3))
    pl.turn("red", ("PLACE", 3, 2))
    print(pl.board)
    print(pl.board.diamonds("red"))


def testdouble_bridges():
    pl = player.Player("red", 4)
    # pl.turn("red", ("PLACE", 1, 0))
    pl.turn("red", ("PLACE", 2, 0))
    # pl.turn("red", ("PLACE", 1, 1))
    pl.turn("red", ("PLACE", 0, 1))

    print(pl.board)
    print(pl.board.diamonds("red", ""))


# if __name__ == '__main__':
#     testplayer2()


def test_a_star():
    board = search.Board(5)
    board = board.action(search.Action("blue", "PLACE", 1, 0))
    board = board.action(search.Action("blue", "PLACE", 1, 1))
    board = board.action(search.Action("blue", "PLACE", 1, 3))
    board = board.action(search.Action("blue", "PLACE", 3, 2))
    print(board)
    solution, cost = board.a_star("red", (4, 2), (0, 0))
    assert len(solution) == 8
    assert cost == 8

    solution, cost = board.a_star("red", (4, 2), (0, 0))
    assert len(solution) == 8
    assert cost == 8


def test_a_star_shortcut():
    board = search.Board(5)
    board = board.action(search.Action("blue", "PLACE", 1, 0))
    board = board.action(search.Action("blue", "PLACE", 1, 1))
    board = board.action(search.Action("blue", "PLACE", 1, 3))
    board = board.action(search.Action("blue", "PLACE", 3, 2))
    print(board)
    path1, cost = board.a_star("red", (4, 2), (0, 0))
    assert cost == 8
    for elem in path1:
        board = board.action(search.Action("red", "PLACE", *elem.coords))
    print(board)

    path2, cost = board.a_star("red", (4, 2), (0, 0))
    assert cost == 0

    assert path2 == path1


def test_defensive():
    pl = player.Player("red", 4, depth=2)
    # pl.turn("red", ("PLACE", 1, 3))
    pl.turn("blue", ("PLACE", 2, 0))
    pl.turn("blue", ("PLACE", 2, 1))
    pl.turn("red", ("PLACE", 1, 2))
    print(pl.board)
    print(player.evaluate(pl.board, "red", ""))
    b1 = pl.board.action(search.Action("red", "PLACE", 3, 3))
    print(b1)
    print("b1", player.evaluate(b1, "red", ""))

    b2 = pl.board.action(search.Action("red", "PLACE", 2, 2))
    print(b2)
    print("b2", player.evaluate(b2, "red", "blue"))

    # pl.turn("red", ("PLACE", 2, 1))
    # print(player.evaluate(pl.board, "red", ""))
    act = pl.action()
    pl.turn("red", act)
    print(pl.board)


def test_evaluate():
    pl = player.Player("red", 4, depth=1)
    pl.turn("blue", ("PLACE", 2, 0))
    pl.turn("blue", ("PLACE", 2, 1))
    pl.turn("blue", ("PLACE", 2, 2))
    print(pl.board)
    print(player.evaluate(pl.board, "red", ""))
    pl.turn("red", ("PLACE", 1, 3))
    print(pl.board)
    print(player.evaluate(pl.board, "red", ""))
    pl.turn("red", ("PLACE", 3, 3))
    print(pl.board)
    print(player.evaluate(pl.board, "red", ""))
    pl.turn("red", ("PLACE", 2, 3))
    print(pl.board)
    print(player.evaluate(pl.board, "red", ""))


def test_distance_to_win_2():
    pl = player.Player("red", 4, depth=1)
    path1, cost = pl.board.a_star("blue", (0, 0), (2, 2))

    for elem in path1:
        pl.board = pl.board.action(
            search.Action("blue", "PLACE", *elem.coords))
    print(pl.board)
    print(pl.board.distance_to_win("blue"))


def test_distance_to_win():
    board = search.Board(5)
    board = board.action(search.Action("blue", "PLACE", 1, 0))
    board = board.action(search.Action("blue", "PLACE", 1, 1))
    board = board.action(search.Action("blue", "PLACE", 1, 3))
    board = board.action(search.Action("blue", "PLACE", 3, 2))
    print(board)
    path2, cost = board.a_star("blue", (1, 0), (1, 4))
    print(path2, cost)
    path, dist = board.distance_to_win("blue")
    print(path, dist)
    assert dist == 2

    board = board.action(search.Action("red", "PLACE", 2, 1))
    print(board)
    path, dist = board.distance_to_win("red")
    print(path, dist)
    assert dist == 4

    board = board.action(search.Action("red", "PLACE", 1, 2))
    print(board)
    path, dist = board.a_star("red", (4, 2), (0, 0))
    print(path, dist)
    assert dist == 6

    path, dist = board.distance_to_win("red")
    print(path, dist)
    assert dist == 3

    board = board.action(search.Action("red", "PLACE", 0, 2))
    board = board.action(search.Action("red", "PLACE", 3, 1))
    board = board.action(search.Action("red", "PLACE", 4, 1))

    path, dist = board.distance_to_win("red")
    print(path, dist)
    assert dist == 0

    path, dist = board.distance_to_win("blue")
    print(path, dist)
    assert dist == math.inf
