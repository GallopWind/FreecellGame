import queue
import heapq
import math
from abc import ABC, abstractmethod, ABCMeta
import numpy as np


class BaseNode(ABC):
    def __init__(self, parent, cost):
        self.parent = parent
        self.cost = cost

    @abstractmethod
    def __cmp__(self, other):
        pass

    @abstractmethod
    def __lt__(self, other):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def GetNeighbors(self):
        """
        :return: return neighbor nodes of self.
        """
        pass

    @abstractmethod
    def CheckEnd(self):
        pass

    @abstractmethod
    def GetCost(self):
        pass

    @abstractmethod
    def UpdateByNode(self, other):
        pass


class HeuristicSearch:
    def __init__(self):
        self.root_node = None
        self.cur_node = None
        self.traversed_nodes = []
        self.to_traverse_nodes = []

    def SetRoot(self, node):
        self.root_node = node

    def Search(self, mode="HeuristicSearch", max_nodes=10000):
        with open("data/search_record", "w") as f:
            if mode == "HeuristicSearch":
                self.cur_node = self.root_node
                while (
                    not self.cur_node.CheckEnd()
                    and len(self.traversed_nodes) < max_nodes
                ):
                    print(self.cur_node.game_state.ObserveForHuman(), file=f)
                    self.traversed_nodes.append(self.cur_node)
                    neighbor_nodes = self.cur_node.GetNeighbors()
                    for node in neighbor_nodes:
                        # danger code.
                        # if node in self.traversed_nodes:
                        #     # update heuristic can be done in 'in' by overwrite __eq__.
                        #     pass
                        # else:
                        #     heapq.heappush(self.to_traverse_nodes, node)
                        found = False
                        for elem_node in self.traversed_nodes:
                            if elem_node == node:
                                found = True
                                elem_node.UpdateByNode(node)
                                break
                        if found:
                            # traversed node
                            pass
                        else:
                            heapq.heappush(self.to_traverse_nodes, node)
                    if self.to_traverse_nodes:
                        self.cur_node = heapq.heappop(self.to_traverse_nodes)
                    else:
                        break
                if self.cur_node.CheckEnd():
                    return True
                else:
                    return False
