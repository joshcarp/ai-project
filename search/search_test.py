import typing

import search


def testsquare():
    a: search.Input = search.Input("""{
  "n": 5,
  "board": [
      ["b", 1, 0],
      ["b", 1, 1],
      ["b", 1, 3],
      ["b", 3, 2]
  ],
  "start": [4, 2],
  "goal": [0, 0]
  }
""")
    print(a)

    b: search.Board = search.Board(a)
    print(b)
    print(b.pieces[3][2])
    print(search.direction_vectors()[0] + b.pieces[3][2])
    end = find_end(b)
    print(end)


def find_end(b: search.Board):
    current = b.start
    closed: typing.List[search.Hexagon] = []
    open: typing.List[search.Hexagon] = []
    current.path_cost = 0
    while current.coords != b.goal.coords:
        closed.append(current)
        for elem in search.neighbours(current, b):
            current_path_cost = current.path_cost + 1
            if elem.path_cost < current.path_cost:
                if elem in closed:
                    continue
                elif elem in open:
                    elem.path_cost = current_path_cost
                    current = elem
                    elem.previous = current
            if elem not in closed and elem not in open:
                elem.path_cost = current_path_cost
                open.append(elem)
    return current

# def testneighbours():
#     board: search.Board = search.Board(None)
#     board.n = 5
#     tests = [
#         {
#             "coord": (0, 0),
#             "neighbours": {(1, 0), (0, 1)}
#         },
#         {
#             "coord": (0, 1),
#             "neighbours": {(0, 0), (1, 0), (1, 1), (0, 2)}
#         },
#         {
#             "coord": (2, 2),
#             "neighbours": {(2, 1), (1, 2), (1, 3), (2, 3), (3, 2), (3, 1)}
#         },
#         {
#             "coord": (4, 4),
#             "neighbours": {(4, 3), (3, 4)}
#         },
#     ]
#
#     for elem in tests:
#         coord = elem["coord"]
#         neighbours = search.neighbours(search.Hexagon(coord[0], coord[1]), board)
#         assert elem["neighbours"] == neighbours
