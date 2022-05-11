import math

import Team_Joshua_s.evaluation as evaluation
from Team_Joshua_s import utils, board


class Player:
    """
    Player is Team_Joshua_s player
    """
    player: str = ""
    brd: board.Board = None
    depth: int
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
        13: 1,
        14: 1,
        15: 1}

    def __init__(self, player: str, n: int, depth: int = 3):
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
        self.cache = {}

    def action(self):
        """
       Called at the beginning of your turn. Based on the current state
       of the game, select an action to play.
       """
        try:
            act = action(self.player, self.player, self.board, self.depth,
                         -math.inf, math.inf)
            if act[1] is None:
                raise Exception
            if self.board.piece(act[1].r, act[1].q).color != "":
                raise Exception
            return ("PLACE", act[1].r, act[1].q)
        except BaseException:
            simple = evaluation.distance_to_win(self.board, self.player)
            blank = [x for x in simple[0] if x.color == ""]
            return ("PLACE", *blank[0].coords)

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
    """
    recursivley searches board states in order to find the one that maximises
    our's evaluation.
    :param our: The players color.
    :param player: The player that who's turn it is.
    :param brd: a board.
    :param depth: depth to search.
    :param a: alpha for alpha beta pruning.
    :param b: beta for alpha beta pruning.
    :return: (best action to take, evaluation of deepest node)
    """
    utility = evaluation.evaluate(brd, our)
    if depth == 0 or utility in evaluation.special_values:
        return utility, None
    max_score, min_score = (None, None), (None, None)

    # get the minimum path for the current player.
    path, _ = evaluation.distance_to_win(brd, player)
    path = [e for e in path if e.color == ""]

    # get the minimum path for the next player
    path2, _ = evaluation.distance_to_win(brd, utils.next(player))
    path.extend([e for e in path2 if e.color == ""])
    # This iterates only over the paths that are in the minimum distances
    # for either side and doesn't expand anything else
    for pieces in path:
        if pieces.coords == (0, 2):
            a = 1
        act = utils.Action(player, "PLACE", *pieces.coords)
        newboard = brd.action(act)
        evaluate = action(our,
                          utils.next(player),
                          newboard,
                          depth - 1,
                          a,
                          b)
        evaluate = (evaluate[0], act)

        # minimax algorithm:
        # If we're the player then we want to maximise the score.
        if our == player:
            if max_score[0] is None:
                max_score = evaluate
            max_score = max(max_score, evaluate, key=lambda x: x[0])
            a = max(a, evaluate[0])
        # If the other player is playing then we want to minimise the score.
        else:
            if min_score[0] is None:
                min_score = evaluate
            min_score = min(min_score, evaluate, key=lambda x: x[0])
            b = min(b, evaluate[0])
        # alpha beta pruning, yay
        if b <= a:
            break
    if our == player:
        return max_score
    return min_score
