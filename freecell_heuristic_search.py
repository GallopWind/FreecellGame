#!python

# %%
from heuristic_search_algorithm import HeuristicSearch, BaseNode
import Freecell_Game
import torch
import numpy as np
import MLP
import copy


class Cost:
    def __init__(self, cost_start, cost_end):
        self.cost_start = cost_start
        self.cost_end = cost_end
        self.cost_combine = cost_end + cost_start

    def UpdateByCost(self, other):
        self.cost_start = other.cost_start
        self.cost_combine = self.cost_start + self.cost_end


class SearchTree:
    cost_model = MLP.MLP()

    def __init__(self):
        self.root = None
        SearchTree.cost_model.load_state_dict(torch.load("data/model"))
        SearchTree.cost_model.eval()

    class SearchNode(BaseNode):
        def __init__(self, game_state, parent, cost_start):
            self.game_state = game_state
            super().__init__(parent, self.GetCost(cost_start))

        def __eq__(self, other):
            for x in range(len(self.game_state.CARDS)):
                if (
                    self.game_state.CARDS[x].group_id
                    != other.game_state.CARDS[x].group_id
                    or self.game_state.CARDS[x].group_index
                    != other.game_state.CARDS[x].group_index
                ):
                    return False
            return True

        def __lt__(self, other):
            if self.cost.cost_combine < other.cost.cost_combine:
                return True
            else:
                return False

        def __cmp__(self, other):
            if self.cost.cost_combine < other.cost.cost_combine:
                return -1
            else:
                return 1

        def GetCost(self, cost_start):
            X = torch.tensor([self.game_state.ObserveForNet()], dtype=torch.float32)
            cost_end = float(SearchTree.cost_model(X)[0][0] * 100)
            return Cost(cost_start, cost_end)

        def GetNeighbors(self):
            res = []
            oprts = self.game_state.ValidOprts()
            for oprt in oprts:
                game = copy.deepcopy(self.game_state)
                game.Move(*oprt)
                if self.cost.cost_end > 50:
                    new_node = SearchTree.SearchNode(
                        game, self.game_state, self.cost.cost_start
                    )
                else:
                    new_node = SearchTree.SearchNode(
                        game, self.game_state, self.cost.cost_start + 1
                    )
                res.append(new_node)
            return res

        def CheckEnd(self):
            if self.game_state.CheckWinStrict():
                return True
            else:
                return False

        def UpdateByNode(self, other):
            if other.cost.cost_combine < self.cost.cost_combine:
                self.cost.UpdateByCost(other.cost)

    def NewGameAndSearch(self):
        game = Freecell_Game.FreeCellGame()
        game.NewGame()
        searcher = HeuristicSearch()
        searcher.SetRoot(SearchTree.SearchNode(game, None, 0))
        if searcher.Search(max_nodes=1000):
            print("Find! Steps: %d" % len(searcher.traversed_nodes))
        else:
            print("Fail!")


# %%
if __name__ == "__main__":
    # %%
    freecell_game_search = SearchTree()
    freecell_game_search.NewGameAndSearch()

# %%
