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

    b: search.Board = search.Board(a.n)
    print(b)
