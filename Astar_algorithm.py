import math
import numpy
import matplotlib.pyplot as plt
import random
from heuristic_search_algorithm import BaseNode, HeuristicSearch


class Cost:
    def __init__(self, cost_start, cost_end):
        self.cost_start = cost_start
        self.cost_end = cost_end
        self.cost_combine = cost_end + cost_start

    def UpdateByCost(self, other):
        self.cost_start = other.cost_start
        self.cost_combine = self.cost_start + cost.cost_end


class Map:
    x_range = None
    y_range = None
    start = None
    end = None
    cell_occupy = None

    def __init__(self, x_range, y_range):
        # define cell index
        # index = y*x_range+x
        Map.x_range = x_range
        Map.y_range = y_range
        Map.start = (1, 1)
        Map.end = (x_range, y_range)
        Map.cell_occupy = [0 for x in range(x_range * y_range)]

    # don't suggest use this method to implement singleton.
    # @staticmethod
    # def GetInstance():
    #     if not Map.Instance:
    #         Map.Instance = Map()
    #     return Map.Instance

    class Cell(BaseNode):
        def __init__(self, x, y, occupy, parent, cost_start, map_refer):
            self.x = x
            self.y = y
            self.occupy = occupy
            self.map_refer = map_refer
            super().__init__(parent, self.GetCost(cost_start))

        def __cmp__(self, other):
            if self.cost.cost_combine < other.cost.cost_combine:
                return -1
            else:
                return 1

        def __eq__(self, other):
            if self.x == other.x and self.y == other.y:
                return True
            else:
                return False

        def __lt__(self, other):
            if self.cost.cost_combine < other.cost.cost_combine:
                return 1
            else:
                return -1

        def GetCost(self, cost_start):
            return Cost(cost_start, math.hypot(self.map_refer.start[0] - self.x, self.map_refer.start[1] - self.y))

        def GetNeighbors(self):
            res = []
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    x = self.x + dx
                    y = self.y + dy
                    if x < 1 or x > self.map_refer.x_range or y < 1 or y > self.map_refer.y_range:
                        # out range
                        continue
                    occupy = self.map_refer.GetCellOccupy(x, y)
                    if occupy == 1:
                        # occupied
                        continue
                    if dx * dy != 0:
                        res.append(self.map_refer.Cell(x, y, occupy, self,
                                                       self.cost.cost_start + 1.414213, self.map_refer))
                    elif dx + dy == 0:
                        continue
                    else:
                        res.append(
                            self.map_refer.Cell(x, y, occupy, self, self.cost.cost_start + 1, self.map_refer))
            return res

        def CheckEnd(self):
            if self.x == self.map_refer.x_range and self.y == self.map_refer.y_range:
                return True
            else:
                return False

        def UpdateByNode(self, other):
            if other.cost.cost_combine < self.cost.cost_combine:
                self.cost.UpdateByCost(other.cost)

    def SetWallConfig(self, vertical_num, vertical_l, horizon_num, horizon_l):
        self.vertical_num = vertical_num
        self.vertical_l = vertical_l
        self.horizon_num = horizon_num
        self.horizon_l = horizon_l

    def RandomGenerate(self):
        res_X = []
        res_Y = []
        # vertical wall: 30
        random_X = numpy.random.choice(self.x_range, self.vertical_num, replace=False)
        random_Y = numpy.random.choice(self.y_range - self.vertical_l, self.vertical_num, replace=False)
        for x, y in zip(random_X, random_Y):
            wall_x = x + 1
            wall_y = y + 1
            for i in range(self.vertical_l):
                cell_y = wall_y + i
                self.SetCellOccupy(wall_x, cell_y, 1)
                res_X.append(wall_x)
                res_Y.append(cell_y)
        # horizon wall
        random_X = numpy.random.choice(self.x_range - self.horizon_l, self.horizon_num, replace=False)
        random_Y = numpy.random.choice(self.y_range, self.horizon_num, replace=False)
        for x, y in zip(random_X, random_Y):
            wall_x = x + 1
            wall_y = y + 1
            for i in range(self.horizon_l):
                cell_x = wall_x + i
                self.SetCellOccupy(cell_x, wall_y, 1)
                res_X.append(cell_x)
                res_Y.append(wall_y)
        return res_X, res_Y

    def GetCellOccupy(self, x, y):
        return self.cell_occupy[(y - 1) * self.x_range + (x - 1)]

    def SetCellOccupy(self, x, y, occupy):
        self.cell_occupy[(y - 1) * self.x_range + (x - 1)] = occupy

    def SearchPath(self):
        start_cell = Map.Cell(1, 1, 0, None, 0, self)
        searcher = HeuristicSearch()
        searcher.SetRoot(start_cell)
        searcher.Search()
        res_x = []
        res_y = []
        if searcher.cur_node.CheckEnd():
            # found
            tmp_node = searcher.cur_node
            while tmp_node:
                res_x.append(tmp_node.x)
                res_y.append(tmp_node.y)
                tmp_node = tmp_node.parent
        else:
            # not found
            pass
        return res_x, res_y


if __name__ == '__main__':
    grid_map = Map(100, 100)
    grid_map.SetWallConfig(3, 30, 3, 30)
    wall_X, wall_Y = grid_map.RandomGenerate()
    path_X, path_Y = grid_map.SearchPath()
    figure = plt.figure()
    ax1 = figure.add_subplot(1, 2, 1)
    ax1.plot(wall_X, wall_Y, 'bo')
    ax2 = figure.add_subplot(1, 2, 2)
    ax2.plot(wall_X, wall_Y, 'bx', alpha=0.5)
    ax2.plot(path_X, path_Y, 'rx', alpha=0.5)
    figure.show()
    input()
