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


def testsquareimpossible():
    rawinput: search.Input = search.Input(
        """{"n":5,"board":[["b",1,0],["b",1,1],["b",1,3],["b",3,2],
        ["b",2,4],["b",2,0],["b",1,2],["b",1,4]],
        "start":[4,2],"goal":[0,0]}""")
    expected = """0
"""
    board: search.Board = search.Board(rawinput)
    solution = board.a_star()
    output = search.format_output(solution)
    assert output == expected


def testsquareimpossible2():
    rawinput: search.Input = search.Input(
        """{"n":5,"board":[["b",3,1],["b",2,2],
        ["b",1,3],["b",0,4]],"start":[4,4],"goal":[0,0]}""")
    board: search.Board = search.Board(rawinput)
    solutionbfs = bfs(board)
    outputbfs = search.format_output(solutionbfs)

    board2: search.Board = search.Board(rawinput)
    solutionastar = board2.a_star()
    outputastar = search.format_output(solutionastar)
    assert outputbfs == outputastar


def testsquare3():
    rawinput: search.Input = search.Input(
        """{"n":5,"board":[["b",2,2],["b",1,3],
        ["b",0,4],["b",3,1],["b",2,0],["b",1,0]],
        "start":[4,2],"goal":[0,0]}""")
    board: search.Board = search.Board(rawinput)
    solutionbfs = bfs(board)
    outputbfs = search.format_output(solutionbfs)

    board2: search.Board = search.Board(rawinput)
    solutionastar = board2.a_star()
    outputastar = search.format_output(solutionastar)
    assert outputbfs == outputastar


def testsquare4():
    rawinput: search.Input = search.Input(
        """{"n":5,"board":[["b",4,0],["b",4,2],["b",2,1],["b",2,3],
        ["b",0,1],["b",0,3],["b",1,2],
        ["b",4,3]],"start":[4,4],"goal":[0,0]}""")
    board: search.Board = search.Board(rawinput)
    solutionbfs = bfs(board)
    outputbfs = search.format_output(solutionbfs)

    board2: search.Board = search.Board(rawinput)
    solutionastar = board2.a_star()
    outputastar = search.format_output(solutionastar)
    assert outputbfs == outputastar


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


def bfs(self: search.Board):
    queue = [self.start]
    visited = {self.start}
    while len(queue) != 0:
        current = queue.pop(0)
        if current.coords == self.goal.coords:
            break
        for neig in self.neighbours(current):
            if neig in visited:
                continue
            neig.previous = current
            queue.append(neig)
            visited.add(neig)
    return self.goal.get_path()
