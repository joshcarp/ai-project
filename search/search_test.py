import search


def testsquare():
    rawinput: search.Input = search.Input("""{
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
    expected = """8
(4,2)
(4,1)
(3,1)
(2,1)
(1,2)
(0,2)
(0,1)
(0,0)"""
    board: search.Board = search.Board(rawinput)
    solution = board.a_star()
    output = search.format_output(solution)
    assert output == expected


def testsquare2():
    rawinput: search.Input = search.Input(
        """{"n":5,"board":[["b",1,0],["b",1,1],["b",1,3],["b",3,2],["b",3,3],
        ["b",1,2],["b",2,0],["b",3,0],["b",4,0]],"start":[4,2],
        "goal":[0,0]}""")
    expected = """10
(4,2)
(4,3)
(3,4)
(2,4)
(1,4)
(0,4)
(0,3)
(0,2)
(0,1)
(0,0)"""
    board: search.Board = search.Board(rawinput)
    solution = board.a_star()
    output = search.format_output(solution)
    assert output == expected


def testneighbours():
    input = search.Input("{}")
    input.n = 5
    board: search.Board = search.Board(input)
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
