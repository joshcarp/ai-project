from Team_Joshua_s.search import *

Action = namedtuple('Action', 'player type r q')
Action.__new__.__defaults__ = (None,) * len(Action._fields)

class Player:
    player: str = ""
    board: Board = None
    plays: List[Action] = []

    def __init__(self, player: str, n: int):
        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.

        The parameter player is the string "red" if your player will
        play as Red, or the string "blue" if your player will play
        as Blue.
        """
        inp: Input = Input()
        inp.n = n
        self.board = Board(inp)
        self.color = player

    def action(self):
        """
       Called at the beginning of your turn. Based on the current state
       of the game, select an action to play.
       """
        pass

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
        if type(action) == str:
            action = (action,)
        action = Action(player, *action)
        self.plays.append(action)
        if action.type == "STEAL":
            prev = self.plays[-2]
            self.board.piece(prev.r, prev.q).set_color(action.player)
        if action.type == "PLACE":
            capture(self.board, action)
            self.board.piece(action.r, action.q).set_color(action.player)


def capture(b: Board, action: Action):
    coords = (action.r, action.q)
    filter1 = lambda x: x.color != action.player and x.color != ""
    filter2 = lambda x: x.color == action.player and x.color != ""
    neighs = b.neighbours(b.piece(*coords), filter=filter1)
    seen: {Hexagon: Hexagon} = {}
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
