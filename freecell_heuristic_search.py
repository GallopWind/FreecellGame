#!python
from heuristic_search_algorithm import HeuristicSearch, BaseNode
import Freecell_Game


class Cost:
    def __init__(self, cost_start, cost_end):
        self.cost_start = cost_start
        self.cost_end = cost_end
        self.cost_combine = cost_end + cost_start

    def UpdateByCost(self, other):
        self.cost_start = other.cost_start
        self.cost_combine = self.cost_start + self.cost_end


class SearchTree:
    def __init__(self):
        self.root = None

    class SearchNode(BaseNode):
        def __init__(self):
            pass

    def NewGame(self):
        game = Freecell_Game.FreeCellGame()
        game.NewGame()
        self.root = game
