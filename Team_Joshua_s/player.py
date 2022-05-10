import math

import Team_Joshua_s.search as search


class Player:
    player: str = ""
    board: search.Board = None
    plays: search.List[search.Action] = []
    depth: int = 4
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
        if depth is not None:
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
        act = action(self.player, self.player, self.board, self.depth,
                     -math.inf, math.inf)
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
        if not isinstance(action, search.Action):
            action = search.Action(player, *action)
        self.board = self.board.action(action)


def action(our: str, player: str, board: search.Board, depth: int, a: float,
           b: float):
    if depth == 0:
        utility = evaluate(board, our, player)
        print(utility)
        return utility, None
    max_score, min_score = (-math.inf, None), (math.inf, None)
    for pieces in board.filter_pieces(lambda x: x.color == ""):
        act = search.Action(player, "PLACE", *pieces.coords)
        newboard = board.action(act)
        if act.r == 2 and act.q == 2 and player == "red":
            print()
        terminal = action(our,
                          search.next_player(player),
                          newboard,
                          depth - 1,
                          a,
                          b)
        terminal = (terminal[0], act)
        if our == player:
            if max_score[0] == -math.inf:
                max_score = terminal
            max_score = max(max_score, terminal, key=lambda x: x[0])
            a = max(a, terminal[0])
        else:
            if min_score == math.inf:
                min_score = terminal
            min_score = min(min_score, terminal, key=lambda x: x[0])
            b = min(b, terminal[0])
        if b <= a:
            break
    if our == player:
        return max_score
    return min_score


def evaluate(board: search.Board, our: str, player: str) -> float:
    score = 0
    _, distance = board.distance_to_win(our)
    if distance == 1 and our == player:
        score = math.inf
    if distance == 0:
        score = math.inf
    else:
        score = 1/distance

    _, distance = board.distance_to_win(search.next_player(our))
    if distance == 1 and our != player:
        score -= math.inf
    if distance == 0:
        score -= math.inf
    else:
        score -= 1 / distance
    return score





