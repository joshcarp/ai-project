import time

from Team_Joshua_s import evaluation, utils, hexagon, board, player


def testneighbours():
    brd: board.Board = board.Board(5)
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
        neighbours = brd.neighbours(hexagon.Hexagon(coord[0], coord[1]))
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


def testfoo():
    print("hello")
    pl = player.Player("red", 4, depth=1)
    pl.turn("red", ("PLACE", 0, 1))
    pl.turn("red", ("PLACE", 1, 1))
    pl.turn("red", ("PLACE", 2, 1))
    act = pl.action()
    pl.turn(pl.player, act)
    print(pl.board)


def testa_star():
    pl = player.Player("red", 15)
    start_line, end_line = utils.start_end_line(pl.board, pl.player)
    start = hexagon.Hexagon(-1, -1)
    start.custom_neighbours = start_line
    start.color = "red"
    end = hexagon.Hexagon(15, 15)
    start.color = "red"
    end.custom_neighbours = end_line

    for elem in end_line:
        elem.custom_neighbours = [end]

    s = pl.board.a_star("red", start, end)

    print(s)


def testplayer2():
    # pr = cProfile.Profile()
    # pr.enable()
    print("hello")
    pl = player.Player("red", 4)
    pl2 = player.Player("blue", 4, random=True)

    for i in range(6):
        if i == 3:
            print()
        start_time = time.time()
        act = pl.action()
        print(pl.board)
        print(pl.player, act)
        pl.turn(pl.player, act)
        pl2.turn(pl2.player, act)
        print(time.time() - start_time)
        act = pl2.action()
        print(pl.board)
        print(pl2.player, act)
        pl.turn(pl2.player, act)
        pl2.turn(pl2.player, act)

        # pl2.turn(pl.player, act)


# print("red: ", len(pl.board.filter_pieces(lambda x: x.color == "red")))
# print("blue: ",
#       len(pl.board.filter_pieces(lambda x: x.color == "blue")))
# act = pl2.action()
# print(act)
# pl.turn(pl2.player, act)
# pl2.turn(pl2.player, act)
# print(pl.board)

# print("red: ", len(pl.board.filter_pieces(lambda x: x.color == "red")))
# print("blue: ",
#       len(pl.board.filter_pieces(lambda x: x.color == "blue")))
# blank = pl.board.filter_pieces(lambda x: x.color == "")
# if len(blank) <= 2:
#     break
# if i == 3:
#     print()
# if pl.board.distance_to_win("blue")[1] == 0:
#     print("blue is the winner")
#     break
# if pl.board.distance_to_win("red")[1] == 0:
#     print("red is the winner")
#     break
# print(i)

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
    print(evaluation.triangles(pl.board, "red"))


def testcapturable():
    pl = player.Player("red", 4)
    pl.turn("red", ("PLACE", 1, 0))
    pl.turn("blue", ("PLACE", 2, 0))
    pl.turn("red", ("PLACE", 1, 1))
    print(pl.board)
    print(evaluation.capturable(pl.board, "red"))
    print(evaluation.capturable(pl.board, "blue"))


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
    print(evaluation.diamonds(pl.board, "red"))


def testdouble_bridges():
    pl = player.Player("red", 4)
    # pl.turn("red", ("PLACE", 1, 0))
    pl.turn("red", ("PLACE", 2, 0))
    # pl.turn("red", ("PLACE", 1, 1))
    pl.turn("red", ("PLACE", 0, 1))

    print(pl.board)
    print(evaluation.double_bridge(pl.board, "red"))


# if __name__ == '__main__':
#     testplayer2()


def test_a_star():
    brd = board.Board(5)
    brd = brd.action(utils.Action("blue", "PLACE", 1, 0))
    brd = brd.action(utils.Action("blue", "PLACE", 1, 1))
    brd = brd.action(utils.Action("blue", "PLACE", 1, 3))
    brd = brd.action(utils.Action("blue", "PLACE", 3, 2))
    print(brd)
    solution, cost = brd.a_star("red", brd.piece(4, 2), brd.piece(0, 0))
    assert len(solution) == 8
    assert cost == 8

    solution, cost = brd.a_star("red", brd.piece(4, 2), brd.piece(0, 0))
    assert len(solution) == 8
    assert cost == 8


def test_a_star_shortcut():
    brd = board.Board(5)
    brd = brd.action(utils.Action("blue", "PLACE", 1, 0))
    brd = brd.action(utils.Action("blue", "PLACE", 1, 1))
    brd = brd.action(utils.Action("blue", "PLACE", 1, 3))
    brd = brd.action(utils.Action("blue", "PLACE", 3, 2))
    print(brd)
    path1, cost = brd.a_star("red", brd.piece(4, 2), brd.piece(0, 0))
    assert cost == 8
    for elem in path1:
        brd = brd.action(utils.Action("red", "PLACE", *elem.coords))
    print(brd)

    path2, cost = brd.a_star("red", brd.piece(4, 2), brd.piece(0, 0))
    assert cost == 0

    assert path2 == path1


def test_defensive():
    pl = player.Player("red", 4, depth=2)
    # pl.turn("red", ("PLACE", 1, 3))
    pl.turn("blue", ("PLACE", 2, 0))
    pl.turn("blue", ("PLACE", 2, 1))
    pl.turn("red", ("PLACE", 1, 2))
    print(pl.board)
    print(evaluation.evaluate(pl.board, "red", ""))
    b1 = pl.board.action(utils.Action("red", "PLACE", 3, 3))
    print(b1)
    print("b1", evaluation.evaluate(b1, "red", ""))

    b2 = pl.board.action(utils.Action("red", "PLACE", 2, 2))
    print(b2)
    print("b2", evaluation.evaluate(b2, "red", "blue"))

    # pl.turn("red", ("PLACE", 2, 1))
    # print(player.evaluate(pl.board, "red", ""))
    act = pl.action()
    pl.turn("red", act)
    print(pl.board)


def test_defensive2():
    pl = player.Player("red", 4, depth=2)
    # pl.turn("red", ("PLACE", 1, 3))
    pl.turn("blue", ("PLACE", 2, 0))
    pl.turn("blue", ("PLACE", 2, 1))
    pl.turn("red", ("PLACE", 1, 2))
    pl.turn("red", ("PLACE", 2, 2))
    pl.turn("red", ("PLACE", 0, 2))
    print(pl.board)
    print(evaluation.distance_to_win(pl.board, "red"))
    print(evaluation.evaluate(pl.board, "red", "red"))
    print(pl.action())
    # pl.turn("red", ("PLACE", 3, 1))
    # print(pl.board)
    # print(evaluation.distance_to_win(pl.board, "red"))
    # print(evaluation.evaluate(pl.board, "red", "red"))

    # act = pl.action()
    # pl.turn("red", act)
    # print(act)
    # print(pl.board)


def test_evaluate():
    pl = player.Player("red", 4, depth=1)
    pl.turn("blue", ("PLACE", 2, 0))
    pl.turn("blue", ("PLACE", 2, 1))
    pl.turn("blue", ("PLACE", 2, 2))
    print(pl.board)
    print(evaluation.evaluate(pl.board, "red", ""))
    pl.turn("red", ("PLACE", 1, 3))
    print(pl.board)
    print(evaluation.evaluate(pl.board, "red", ""))
    pl.turn("red", ("PLACE", 3, 3))
    print(pl.board)
    print(evaluation.evaluate(pl.board, "red", ""))
    pl.turn("red", ("PLACE", 2, 3))
    print(pl.board)
    print(evaluation.evaluate(pl.board, "red", ""))


def test_distance_to_win_2():
    pl = player.Player("red", 4, depth=1)
    path1, cost = pl.board.a_star(
        "blue", pl.board.piece(0, 0), pl.board.piece(2, 2))

    for elem in path1:
        pl.board = pl.board.action(
            utils.Action("blue", "PLACE", *elem.coords))
    print(pl.board)
    print(evaluation.distance_to_win(pl.board, "blue"))


# def test_distance_to_win():
#     board = board.Board(5)
#     board = board.action(utils.Action("blue", "PLACE", 1, 0))
#     board = board.action(utils.Action("blue", "PLACE", 1, 1))
#     board = board.action(utils.Action("blue", "PLACE", 1, 3))
#     board = board.action(utils.Action("blue", "PLACE", 3, 2))
#     print(board)
#     path2, cost = board.a_star("blue", (1, 0), (1, 4))
#     print(path2, cost)
#     path, dist = board.distance_to_win("blue")
#     print(path, dist)
#     assert dist == 2
#
#     board = board.action(utils.Action("red", "PLACE", 2, 1))
#     print(board)
#     path, dist = board.distance_to_win("red")
#     print(path, dist)
#     assert dist == 4
#
#     board = board.action(utils.Action("red", "PLACE", 1, 2))
#     print(board)
#     path, dist = board.a_star("red", (4, 2), (0, 0))
#     print(path, dist)
#     assert dist == 6
#
#     path, dist = board.distance_to_win("red")
#     print(path, dist)
#     assert dist == 3
#     assert dist == board.min_dist_2("red")
#
#     board = board.action(utils.Action("red", "PLACE", 0, 2))
#     board = board.action(utils.Action("red", "PLACE", 3, 1))
#     board = board.action(utils.Action("red", "PLACE", 4, 1))
#
#     path, dist = board.distance_to_win("red")
#     print(path, dist)
#     assert dist == 0
#
#     path, dist = board.distance_to_win("blue")
#     print(path, dist)
#     assert dist == math.inf
#     assert dist == board.min_dist_2("blue")


def test_new_distance():
    brd = board.Board(2)
    # board.foo("red")
    a = evaluation.distance_to_win(brd, "red")
    print(brd)
    print(a)
    brd = brd.action(utils.Action("blue", "PLACE", 1, 0))
    brd = brd.action(utils.Action("blue", "PLACE", 1, 0))
    brd = brd.action(utils.Action("blue", "PLACE", 1, 0))
    print(brd)
    a = evaluation.distance_to_win(brd, "red")
    print(brd)
    print(a)


def test_distance_1():
    brd = board.Board(3)
    brd = brd.action(utils.Action("red", "PLACE", 0, 1))
    brd = brd.action(utils.Action("red", "PLACE", 1, 1))
    # brd = brd.action(utils.Action("red", "PLACE", 2, 1))
    dist = evaluation.distance_to_win(brd, "red")
    print(brd)
    print(dist)
