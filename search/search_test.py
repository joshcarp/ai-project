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


def testneighbours():
    n = 5
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
        neighbours = search.neighbours(search.Hexagon(coord[0], coord[1]), n)
        assert elem["neighbours"] == neighbours
