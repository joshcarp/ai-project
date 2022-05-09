import Team_Joshua_s.player as player
import Team_Joshua_s.search as search
import Team_Joshua_s.util as util
import cProfile
import pstats
import io
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
    #test 1
    pl = player.Player("red", 4)
    pl.turn("red", ("PLACE", 1, 0))
    assert pl.board.piece(1, 0).color == "red"
    print(pl.board.__repr__())

    #test 2
    pl.turn("blue", ("STEAL",))
    assert pl.board.piece(1, 0).color == "blue"
    print(pl.board.__repr__())

    #test 3
    pl.turn("blue", ("PLACE", 1, 1))
    pl.turn("red", ("PLACE", 0, 1))
    pl.turn("red", ("PLACE", 2, 0))
    assert pl.board.piece(0, 1).color == "red"
    assert pl.board.piece(2, 0).color == "red"
    assert pl.board.piece(1, 0).color == ""
    assert pl.board.piece(1, 1).color == ""
    assert player.evaluate(pl.board, "red") == 2
    print(pl.board.__repr__())

    #test 4
    pl.turn("blue", ("PLACE", 1, 0))
    pl.turn("blue", ("PLACE", 1, 1))
    assert pl.board.piece(0, 1).color == ""
    assert pl.board.piece(2, 0).color == ""
    # assert player.evaluate(pl.board, "blue") == 2
    print(pl.board.__repr__())

    #test 5
    # triangles test
    pl.turn("blue", ("PLACE", 0, 1))
    pl.turn("red", ("PLACE", 2, 0))
    assert player.evaluate(pl.board, "blue") == 8
    print(pl.board.__repr__())

    #test 6
    pl.turn("red", ("PLACE", 3, 0))
    pl.turn("red", ("PLACE", 3, 1))
    assert player.evaluate(pl.board, "red") == -4
    print(pl.board.__repr__())

    #test 7
    pl.turn("red", ("PLACE", 3, 2))
    assert player.evaluate(pl.board, "red") == -2
    print(pl.board.__repr__())



# @profile


# def testplayer2():
#     pr = cProfile.Profile()
#     pr.enable()
#     pl = player.Player("red", 4, depth=5)
#     pl2 = player.Player("blue", 4, dumb=True)
#
#     for i in range(6):
#         act = pl.action()
#         print(act)
#         pl.turn(pl.player, act)
#         pl2.turn(pl.player, act)
#         util.print_board(*pl.board.dict())
#         print("red: ", len(pl.board.filter_pieces(lambda x: x.color == "red")))
#         print("blue: ",
#               len(pl.board.filter_pieces(lambda x: x.color == "blue")))
#         act = pl2.action()
#         print(act)
#         pl.turn(pl2.player, act)
#         pl2.turn(pl2.player, act)
#         util.print_board(*pl.board.dict())
#
#         print("red: ", len(pl.board.filter_pieces(lambda x: x.color == "red")))
#         print("blue: ",
#               len(pl.board.filter_pieces(lambda x: x.color == "blue")))
#         if len(pl.board.filter_pieces(lambda x: x.color == "")) <= 2:
#             break
#     pr.disable()
#     s = io.StringIO()
#     sortby = SortKey.CUMULATIVE
#     # ps = pstats.Stats(pr, stream=s)
#     ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
#     ps.print_stats()
#     print(s.getvalue())

# if __name__ == '__main__':
#     testplayer2()
testplayer()