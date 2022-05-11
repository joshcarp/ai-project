"""
randplayer.py contains code for a random Player class to play a game of cachex
by randomly choosing available moves.
"""
import random

from Team_Joshua_s import board, utils


class Player:
    """
    Player is a random player
    """
    player: str = ""
    brd: board.Board = None

    def __init__(self, player: str, n: int):
        self.board = board.Board(n)
        self.player = player

    def action(self):
        """
       Called at the beginning of your turn. Based on the current state
       of the game, select an action to play.
       """
        valid_moves = self.board.filter_pieces(lambda x: x.color == "")
        return (
            "PLACE", *valid_moves[random.randint(0, self.board.n - 1)].coords)

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
        if not isinstance(action, utils.Action):
            action = utils.Action(player, *action)
        self.board = self.board.action(action)
