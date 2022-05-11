import math
from copy import copy
from typing import List, Callable

from Team_Joshua_s import util, utils, hexagon


class Board:
    """
    Board controls all the information about the state and implements the
    path finding algorithm
    """
    mutations: List[List[List[hexagon.Hexagon]]]
    n: int
    last_action: utils.Action
    distances_cache: {}
    distances_cache3: {}
    colors = ["red", "blue"]

    def __init__(self, n, copy=False):
        if copy:
            return
        self.last_action = None
        self.n = n
        self.mutations = []
        self.distances_cache = {"red": None, "blue": None}
        if copy:
            return
        for i in range(n):
            self.mutations.append([])
            for j in range(n):
                h = hexagon.Hexagon(i, j)
                self.mutations[i].append([h])

    def __repr__(self):
        d = {}
        for e in self.filter_pieces():
            if e.color != "":
                d[e.coords] = f"{e.color[0]}"
        return util.board_string(self.n, d)

    def filter_pieces(self,
                      filter: Callable[[hexagon.Hexagon],
                                       bool] = lambda x: True):
        pieces = []
        for i in range(self.n):
            for j in range(self.n):
                hex = self.mutations[i][j][-1]
                if filter(hex):
                    pieces.append(hex)
        return pieces

    def piece(self, x: int, y: int) -> hexagon.Hexagon:
        """
        piece returns the hexagon.Hexagon at coordinates (x, y)
        """
        if (x >= self.n and y >= self.n) or (x < 0 and y < 0):
            return hexagon.Hexagon(x, y)
        return self.mutations[x][y][-1]

    def valid(self, piece: (int, int)) -> bool:
        """
        valid returns True if the hexagon.Hexagon specified
        exists within the board and False otherwise.
        """
        return piece[0] in range(0, self.n) and \
            piece[1] in range(0, self.n)

    def process_action(b, action: utils.Action) -> List[hexagon.Hexagon]:
        """
        process_action will process an action and will mutate the state of the
        board to reflect the new board state.
        :param action:
        :return:
        """
        coords = (action.r, action.q)
        changed = [hexagon.Hexagon(action.r, action.q, action.player)]

        def filter1(x):
            return x.color != action.player and x.color != ""

        def filter2(x):
            return x.color == action.player and x.color != ""

        neighs = b.neighbours(b.piece(*coords), filter=filter1)
        seen: {hexagon.Hexagon: hexagon.Hexagon} = {}
        for elem in neighs:
            if elem.color == action.player or elem.color == "":
                continue
            if elem.coords == coords:
                continue
            neighneighs = b.neighbours(elem, filter=filter2)
            for elem2 in neighneighs:
                if elem2.coords in seen.keys(
                ) and seen[elem2.coords].color == elem.color:
                    changed.append(hexagon.Hexagon(*elem.coords))
                    changed.append(
                        hexagon.Hexagon(*seen[elem2.coords].coords))
                    return changed
                seen[elem2.coords] = elem
        return changed

    def action(self, action: utils.Action):
        """
        action taked in an Action and returns the new board state without
        mutating the old one
        :param action:
        :return:
        """
        cpy: Board = copy(self)
        changed = []
        if action.type == "STEAL":
            changed.append(
                hexagon.Hexagon(
                    self.last_action.r,
                    self.last_action.q,
                    action.player))
        elif action.type == "PLACE":
            changed.extend(cpy.process_action(action))
            cpy.last_action = action
        for elem in changed:
            cpy.mutations[elem.coords[0]][elem.coords[1]].append(elem)

        return cpy

    def neighbours(self, piece: hexagon.Hexagon,
                   filter=lambda x: x.color == "") -> [hexagon.Hexagon]:
        """
        neighbours returns a list of hexagon.Hexagons that
        exist within the board that don't already have a color.
        """
        # would use a set here but set values are copies and not references
        neighs = []
        for a in utils.direction_vectors():
            coord = (piece + a).coords
            if not self.valid(coord):
                continue
            neighb = self.piece(*coord)
            if not filter(neighb):
                continue
            neighs.append(neighb)

        if piece.custom_neighbours is not None and len(
                piece.custom_neighbours) != 0:
            return piece.custom_neighbours
        return neighs

    def a_star(self, player: str, start: hexagon.Hexagon,
               end: hexagon.Hexagon) -> ([hexagon.Hexagon], int):
        """
        a_star implements the a star algorithm and returns the path
        from start to end. the start hexagon.Hexagon will be return[0] and
        the end hexagon.Hexagon will be return[-1].
        """
        nodes_explored = 0
        self.filter_pieces(lambda x: x.reset_search())
        current = start
        closed: List[hexagon.Hexagon] = []
        opened: List[hexagon.Hexagon] = [current]
        current.total_cost = current.incr_cost(player)
        while current.coords != end.coords:
            nodes_explored += 1
            opened.sort(
                key=lambda x: x.distance(end) + x.total_cost,
                reverse=True
            )
            if len(opened) == 0:
                return [], math.inf
            current = opened.pop()
            closed.append(current)
            for neigh in self.neighbours(
                    current, lambda x: x.color != utils.next(player)):
                nodes_explored += 1
                # neigh_path_cost is the cost to get to the neighbour
                # from the current node
                neigh_path_cost = current.total_cost + \
                    neigh.incr_cost(player)
                # if the neighbours already existing cost is less than
                # the current node then the current nodes previous
                # becomes the neighbour
                # neigh_in_open = neigh in opened
                if neigh.total_cost < neigh_path_cost and neigh in closed:
                    current.total_cost = neigh.total_cost + \
                        current.incr_cost(player)
                    current.previous = neigh
                # if the neighbours total existing cost is more than getting
                # to the neighbour through the current node then set
                # neighbours previous to the current node
                elif neigh.total_cost > \
                        neigh_path_cost and neigh in opened:
                    neigh.total_cost = neigh_path_cost
                    neigh.previous = current
                # if neighbour is not in open then we will add it to be
                # expanded next iteration
                if neigh not in closed and neigh not in opened:
                    neigh.total_cost = neigh_path_cost
                    neigh.previous = current
                    opened.append(neigh)
        # current at this point is goal, so traverse back to start and return
        # the list
        path: List[hexagon.Hexagon] = []
        cost = 0
        while current is not None:
            path.append(current)
            cost += current.incr_cost(player)
            current = current.previous
        path.reverse()
        if start is not None and path[0] != start:
            raise Exception
        if cost == math.inf:
            return path, cost
        self.filter_pieces(lambda x: x.end_search())
        if cost == math.inf:
            return path, cost
        return path, round(cost)

    def __copy__(self):
        newboard = Board(self.n, True)
        newboard.last_action = self.last_action
        newboard.mutations = []
        newboard.n = self.n
        newboard.distances_cache = {
            k: v for (k, v) in self.distances_cache.items()}
        for i in range(self.n):
            newboard.mutations.append([])
            for j in range(self.n):
                newboard.mutations[i].append(self.mutations[i][j].copy())
        return newboard
