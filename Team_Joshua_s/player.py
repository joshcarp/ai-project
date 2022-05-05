from collections import namedtuple
from copy import deepcopy

import Team_Joshua_s.search as search

Action = namedtuple('Action', 'player type r q')
Action.__new__.__defaults__ = (None,) * len(Action._fields)


class Player:
    player: str = ""
    board: search.Board = None
    plays: search.List[Action] = []

    def __init__(self, player: str, n: int):
        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.

        The parameter player is the string "red" if your player will
        play as Red, or the string "blue" if your player will play
        as Blue.
        """
        inp: search.Input = search.Input()
        inp.n = n
        self.board = search.Board(inp)
        self.player = player

    def action(self):
        """
       Called at the beginning of your turn. Based on the current state
       of the game, select an action to play.
       """
        return action(self.player, self.plays, self.board)

    def turn(self, player, action):
        """
        Called at the end of each player's turn to inform this player of
        their chosen action. Update your internal representation of the
        game state based on this. The parameter action is the chosen
        action itself.

        Note: At the end of your player's turn, the action parameter is
        the same as what your player returned from the action method
        above. However, the referee has validated it at this point.
        """
        if isinstance(action, str):
            action = (action,)
        action = Action(player, *action)
        turn(self.plays, self.board, action)


def action(player: str, plays: [], board: search.Board):
    first_moves = []
    for pieces in board.filter_pieces(lambda x: x.color == ""):
        boardcpy = deepcopy(board)
        playscpy = deepcopy(plays)
        action = Action(player, "PLACE", *pieces.coords)
        turn(playscpy, boardcpy, action)
        first_moves.append(
            (boardcpy, playscpy, action, evaluate(boardcpy, player)))
    return max(first_moves, key=lambda x: x[3])[2]


def turn(plays: [], board: search.Board, action: Action):
    plays.append(action)
    if action.type == "STEAL":
        prev = plays[-2]
        board.piece(prev.r, prev.q).set_color(action.player)
    if action.type == "PLACE":
        capture(board, action)
        board.piece(action.r, action.q).set_color(action.player)


def capture(b: search.Board, action: Action):
    coords = (action.r, action.q)

    def filter1(x):
        return x.color != action.player and x.color != ""

    def filter2(x):
        return x.color == action.player and x.color != ""

    neighs = b.neighbours(b.piece(*coords), filter=filter1)
    seen: {search.Hexagon: search.Hexagon} = {}
    for elem in neighs:
        if elem.color == action.player or elem.color == "":
            continue
        if elem.coords == coords:
            continue
        neighneighs = b.neighbours(elem, filter=filter2)
        for elem2 in neighneighs:
            if elem2 in seen.keys() and seen[elem2].color == elem.color:
                b.piece(*elem.coords).set_color("")
                b.piece(*seen[elem2].coords).set_color("")
                b.piece(*coords).set_color(action.player)
                return b
            seen[elem2] = elem
    return


def evaluate(board: search.Board, color: str) -> int:
    return len(
        [e for sub in board.pieces for e in sub if e.color == color]) - len(
        [e for sub in board.pieces for e in sub if
         e.color != color and e.color != ""])
