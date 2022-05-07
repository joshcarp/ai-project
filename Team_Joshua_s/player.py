from collections import namedtuple
from copy import deepcopy

import Team_Joshua_s.search as search

Action = namedtuple('Action', 'player type r q')
Action.__new__.__defaults__ = (None,) * len(Action._fields)


def other_piece(current_piece: str) -> str:
    return {"red": "blue", "blue": "red"}[current_piece]


class Player:
    player: str = ""
    board: search.Board = None
    plays: search.List[Action] = []
    depth: int = 2
    dumb: bool = False

    def __init__(self, player: str, n: int, depth: int = None, dumb=False):
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
        if depth != None:
            self.depth = depth
        self.dumb = dumb

    def action(self):
        """
       Called at the beginning of your turn. Based on the current state
       of the game, select an action to play.
       """
        if self.dumb:
            return ("PLACE", *self.board.filter_pieces(lambda x: x.color == "")[0].coords)
        act = action(self.player, self.player, self.plays, self.board, 0,
                     self.depth)
        if self.board.piece(act[0].r, act[0].q).color != "":
            raise Exception
        return act[0]

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
        if not isinstance(action, Action):
            action = Action(player, *action)
        turn(self.plays, self.board, action)


def action(our: str, player: str, plays: [], board: search.Board, depth: int,
           limit: int):
    first_moves = []
    if depth == limit:
        return None
    for pieces in board.filter_pieces(lambda x: x.color == ""):
        boardcpy = deepcopy(board)
        playscpy = deepcopy(plays)
        act = Action(player, "PLACE", *pieces.coords)
        turn(playscpy, boardcpy, act)
        terminal = action(our,
                         other_piece(player),
                         playscpy,
                         boardcpy,
                         depth + 1,
                         limit)
        if terminal is None:
            terminal = (act, boardcpy)
        else:
            terminal = (act, terminal[1])
        first_moves.append(terminal)
    ma = max(first_moves, key=lambda x: evaluate(x[1], our))
    mi = min(first_moves, key=lambda x: evaluate(x[1], our))
    scoremin = evaluate(mi[1], our)
    scoremax = evaluate(ma[1], our)
    print(our, scoremax, scoremin)
    if our == player:
        return ma
    print(our,scoremax,scoremin)
    return mi


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
    utility = len(
        [e for sub in board.pieces for e in sub if e.color == color]) - len(
        [e for sub in board.pieces for e in sub if
         e.color != color and e.color != ""])
    # if len([e for sub in board.pieces for e in sub if e.color == color]) > 2:
    #     print()
    return utility
