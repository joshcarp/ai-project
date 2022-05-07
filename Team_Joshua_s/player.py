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
        self.board = search.Board(n)
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
            return ("PLACE",
                    *self.board.filter_pieces(lambda x: x.color == "")[
                        0].coords)
        act = action(self.player, self.player, self.board, 0, self.depth)
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
        self.board = self.board.action(action)


def action(our: str, player: str, board: search.Board, depth: int,
           limit: int):
    first_moves = []
    if depth == limit:
        return None
    for pieces in board.filter_pieces(lambda x: x.color == ""):
        act = Action(player, "PLACE", *pieces.coords)
        newboard = board.action(act)
        terminal = action(our,
                          other_piece(player),
                          newboard,
                          depth + 1,
                          limit)
        if terminal is None:
            terminal = (act, newboard)
        else:
            terminal = (act, terminal[1])
        first_moves.append(terminal)
    if our == player:
        return max(first_moves, key=lambda x: evaluate(x[1], our))
    return min(first_moves, key=lambda x: evaluate(x[1], our))


def evaluate(board: search.Board, color: str) -> int:
    utility = len(
        [e for sub in board.pieces() for e in sub if e.color == color]) - len(
        [e for sub in board.pieces() for e in sub if
         e.color != color and e.color != ""])
    # if len([e for sub in board.pieces for e in sub if e.color == color]) > 2:
    #     print()
    return utility
