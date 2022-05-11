import math

import Team_Joshua_s.evaluation as evaluation
from Team_Joshua_s import utils, board


class Player:
    player: str = ""
    brd: board.Board = None
    depth: int
    random: bool
    depth_map = {
        3: 3,
        4: 3,
        5: 3,
        6: 3,
        7: 3,
        8: 2,
        9: 2,
        10: 2,
        11: 2,
        12: 2,
        13: 2,
        14: 2,
        15: 1}

    def __init__(self, player: str, n: int, depth: int = 3, random=False):
        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.

        The parameter player is the string "red" if your player will
        play as Red, or the string "blue" if your player will play
        as Blue.
        """
        self.board = board.Board(n)
        self.player = player
        self.depth = self.depth_map[n]
        self.random = random
        self.cache = {}

    def action(self):
        """
       Called at the beginning of your turn. Based on the current state
       of the game, select an action to play.
       """
        if self.random:
            valid_moves = self.board.filter_pieces(lambda x: x.color == "")
            return (
                "PLACE",
                *valid_moves[1].coords)
        act = action(self.player, self.player, self.board, self.depth,
                     -math.inf, math.inf)
        if act[1] is None:
            raise Exception
        if self.board.piece(act[1].r, act[1].q).color != "":
            raise Exception
        return ("PLACE", act[1].r, act[1].q)

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


def action(
        our: str,
        player: str,
        brd: board.Board,
        depth: int,
        a: float,
        b: float):
    utility = evaluation.evaluate(brd, our, player)
    if depth == 0 or utility == 100000000 or utility == -100000000:
        return utility, None
    max_score, min_score = (None, None), (None, None)
    pp, err = evaluation.distance_to_win(brd, player)
    pp = [e for e in pp if e.color == ""]
    pp2, err = evaluation.distance_to_win(brd, utils.next(player))
    pp.extend([e for e in pp2 if e.color == ""])
    for pieces in pp:
        if pieces.coords == (0, 2):
            a = 1
        act = utils.Action(player, "PLACE", *pieces.coords)
        newboard = brd.action(act)
        terminal = action(our,
                          utils.next(player),
                          newboard,
                          depth - 1,
                          a,
                          b)
        terminal = (terminal[0], act)
        if our == player:
            if max_score[0] is None:
                max_score = terminal
            max_score = max(max_score, terminal, key=lambda x: x[0])
            a = max(a, terminal[0])
        else:
            if min_score[0] is None:
                min_score = terminal
            min_score = min(min_score, terminal, key=lambda x: x[0])
            b = min(b, terminal[0])
        if b <= a:
            break
    if our == player:
        return max_score
    return min_score
