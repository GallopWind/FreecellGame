# %%
import random
import copy

# %%
MAX_SEARCH_DEPTH = 5
MAX_SEARCH_NODES = 1000
# %%
POINT = {1: 'A', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6',
         7: '7', 8: '8', 9: '9', 10: '10', 11: 'J', 12: 'Q', 13: 'K'}
COLOR = ['Heart', 'Diamond', 'Spade', 'Club']


class Card():
    global point

    def __init__(self, color, num):
        self.color = color
        self.num = num
        self.point = POINT[num]
        self.group_id = -1
        self.group_index = -1
        if color in ['Heart', 'Diamond']:
            self.rb = 'r'
        else:
            self.rb = 'b'


CARDS = [Card(c, n) for c in COLOR for n in range(1, 14)]
# %%
OPERATIONS = [(m, n) for m in range(0, 4) for n in range(8, 16)] \
             + [(m, n) for m in range(4, 8) for n in list(range(0, 4)) + list(range(8, 16))] \
             + [(m, n) if m > n else (m, n + 1)
                for m in range(8, 16) for n in range(0, 15)]


# %%


class PokerHeap:
    def __init__(self, heap_id):
        self.heap_list = []
        self.heap_id = heap_id

    def reset(self, cards):
        self.heap_list = cards

    def GetTop(self):
        if len(self.heap_list) == 0:
            return False
        else:
            return self.heap_list[-1]

    def PopTop(self):
        self.heap_list.pop()

    def PushTop(self, card, search=False):
        self.heap_list.append(card)
        if not search:
            card.group_id = self.heap_id
            card.group_index = len(self.heap_list) - 1


class ColorHeap(PokerHeap):
    def __init__(self, color, heap_id):
        super().__init__(heap_id)
        self.color = color

    def CheckMoveInto(self, card):
        if card.color != self.color:
            return False
        if (len(self.heap_list) == 0 and card.num == 1) or \
                (len(self.heap_list) != 0 and card.num == self.heap_list[-1].num + 1):
            return True
        else:
            return False


class FreeCell(PokerHeap):
    def __init__(self, heap_id):
        super().__init__(heap_id)

    def CheckMoveInto(self, card):
        if len(self.heap_list) == 0:
            return True
        else:
            return False


class CardHeap(PokerHeap):
    def __init__(self, heap_id):
        super().__init__(heap_id)

    def CheckMoveInto(self, card):
        if (len(self.heap_list) == 0) or \
                (card.rb != self.heap_list[-1].rb
                 and card.num == self.heap_list[-1].num - 1):
            return True
        else:
            return False


# %%


class FreeCellGame:
    def __init__(self, game=None):
        if not game:
            # color heap 0~3, freecell 4~7, cardheap 8~15
            self.all_cards = [ColorHeap(COLOR[x], x) for x in range(4)] \
                             + [FreeCell(x + 4) for x in range(4)] \
                             + [CardHeap(x + 8) for x in range(8)]
        else:
            # self.all_cards = copy.deepcopy(game.all_cards)
            self.all_cards = copy.copy(game.all_cards)
            for x in range(len(self.all_cards)):
                self.all_cards[x] = copy.copy(game.all_cards[x])
                self.all_cards[x].heap_list = copy.copy(
                    game.all_cards[x].heap_list)

    def CheckMove(self, come, to):
        move_card = self.all_cards[come].GetTop()
        if move_card != False:
            if self.all_cards[to].CheckMoveInto(move_card):
                return True
            else:
                return False
        else:
            return False

    def CheckReverse(self, come, to):
        move_card = self.all_cards[come].GetTop()
        if move_card != False:
            # check reverse
            come_flag = False
            self.all_cards[come].PopTop()
            if self.all_cards[come].CheckMoveInto(move_card):
                come_flag = True
            self.all_cards[come].PushTop(move_card)
            to_flag = False
            if to < 8:
                if self.all_cards[to].CheckMoveInto(move_card):
                    to_flag = True
            else:
                to_flag = True
            if come_flag and to_flag:
                return True
            else:
                return False
        else:
            return False

    # if move for search, don't not change card attr.
    def Move(self, come, to, search=False):
        move_card = self.all_cards[come].GetTop()
        self.all_cards[come].PopTop()
        self.all_cards[to].PushTop(move_card, search)

    @staticmethod
    def ObserveForNet(self):
        res = [(-1, -1) for x in range(52)]
        for x in range(52):
            res[x] = (CARDS[x].group_id, CARDS[x].group_index)
        return res

    @staticmethod
    def ObserveForData():
        res = []
        hash_index = ''
        for x in range(52):
            res.append(CARDS[x].group_id)
            res.append(CARDS[x].group_index)
            hash_index = hash_index + ('%02d' % CARDS[x].group_id) + ('%02d' % CARDS[x].group_index)
        return hash_index, res

    def ParseDataObserve(self, res):
        # clear all heap.
        # no need
        # for poker_heap in self.all_cards:
        #     poker_heap.reset([])
        # no need to clear cards.
        heap_size = [0 for x in range(16)]
        for i in range(len(res) // 2):
            CARDS[i].group_id = res[2 * i]
            CARDS[i].group_index = res[2 * i + 1]
            if heap_size[CARDS[i].group_id] < CARDS[i].group_index + 1:
                heap_size[CARDS[i].group_id] = CARDS[i].group_index + 1
        for i in range(16):
            self.all_cards[i].heap_list = [0 for x in range(heap_size[i])]
        for card in CARDS:
            self.all_cards[card.group_id].heap_list[card.group_index] = card

    def ObserveForHuman(self):
        res = []
        for group in self.all_cards:
            tmp = ['ID:' + (str(group.heap_id) if (group.heap_id > 9)
                            else (str(group.heap_id) + ' '))]
            if hasattr(group, 'color'):
                tmp.append('color:' + group.color[0])
            for card in group.heap_list:
                tmp.append(
                    card.color[0] + (card.point if card.point == '10' else card.point + ' '))
            res.append(tmp)
        return res

    def CheckWin(self):
        for x in range(8, 16):
            heap_l = self.all_cards[x].heap_list
            if len(heap_l) == 0:
                continue
            else:
                for i in range(len(heap_l)):
                    if i > 0 and heap_l[i].num > heap_l[i - 1].num:
                        return False
        return True

    def NewGame(self):
        # clear all heap
        for x in self.all_cards:
            x.reset([])
        # init color heap
        for card in CARDS:
            group_id = COLOR.index(card.color)
            self.all_cards[group_id].PushTop(card)
        # use reverse method to generate new game
        while 1:
            init_flag = True
            for x in range(8):
                if self.all_cards[x].heap_list:
                    init_flag = False
                    break
            for x in range(8, 16):
                if len(self.all_cards[x].heap_list) < 5:
                    init_flag = False
                    break
            if init_flag:
                break
            oprts = self.ValidReverseOprts()
            if not oprts:
                return False
            index = random.randint(0, len(oprts) - 1)
            oprt = oprts[index]
            self.Move(oprt[0], oprt[1])
        return True

    def RandomNewGameAndRecordCost(self, train_data):
        # output string + cost
        # string: (group_id + index) *52
        # clear all heap
        for x in self.all_cards:
            x.reset([])
        # init color heap
        for card in CARDS:
            group_id = COLOR.index(card.color)
            self.all_cards[group_id].PushTop(card)
        # use reverse method to generate new game
        # check oscillation.
        step_cost = 0
        oscillate_count = 0
        last_oprt = None
        llast_oprt = None
        while 1:
            oprts = self.ValidReverseOprts()
            if not oprts:
                break
            index = random.randint(0, len(oprts) - 1)
            oprt = oprts[index]
            self.Move(oprt[0], oprt[1])
            # check oscillate
            if oprt == llast_oprt:
                oscillate_count = oscillate_count + 1
                if oscillate_count == 5:
                    break
            llast_oprt = last_oprt
            last_oprt = oprt
            # record data.
            step_cost = step_cost + 1
            if step_cost > 20:
                train_data.Add(*self.ObserveForData(), step_cost)
        return

    def ValidOperations(self):
        res = []
        for op in OPERATIONS:
            if self.CheckMove(op[0], op[1]):
                res.append(op)
        return res

    def ValidReverseOprts(self):
        res = []
        for op in OPERATIONS:
            if self.CheckReverse(op[0], op[1]):
                res.append(op)
        return res

    def Score(self):
        res = 0
        for x in range(4):
            res = res + len(self.all_cards[x].heap_list)
        return res


# %%


class SearchNode:
    def __init__(self, oprt, game):
        self.oprt = oprt
        self.child = []
        # attention! game: FreecellGame
        self.state = game


class SearchTree:
    def __init__(self, node):
        self.root = node
        self.depth = 1
        self.nodes = 1
        self.max_depth = MAX_SEARCH_DEPTH
        self.max_nodes = MAX_SEARCH_NODES

    def reset(self, node):
        self.depth = 1
        self.root = node

    def GenerateChild(self, node):
        oprts = node.state.ValidOperations()
        if not oprts:
            return False
        for oprt in oprts:
            game = FreeCellGame(node.state)
            game.Move(oprt[0], oprt[1], True)
            node.child.append(SearchNode(oprt, game))
            self.nodes = self.nodes + 1
        return True

    # need to be rewrite.
    # think about how to design return.
    def Traversal(self, node, func):
        if not node.child:
            return func(node)
        else:
            for n in node.child:
                self.Traversal(n, func)
            return True  # how to return.

    # attention. Grow doesn't always success.
    def TreeGrow(self):
        if self.Traversal(self.root, self.GenerateChild):
            self.depth = self.depth + 1
            return True
        else:
            # root has no child and generate failed.
            return False

    def TreeUpdate(self):
        while self.depth < self.max_depth and self.nodes < self.max_nodes:
            if not self.TreeGrow():
                return False  # TreeGrow fail.

    def RootDeep(self, oprt):
        for n in self.root.child:
            if n.oprt == oprt:
                self.nodes = self.nodes // len(self.root.child)
                self.depth = self.depth - 1
                self.root = n
                return True
        return False

    def Score(self, node):
        return node.state.Score()

    def MaxScore(self, node):
        max_score = 0

        def Score(node):
            nonlocal max_score
            score = node.state.Score()
            if score > max_score:
                max_score = score

        self.Traversal(node, Score)
        return max_score


# %%
if __name__ == '__main__':
    pass
# # %%
# game = FreeCellGame()
# # %%
# while not game.NewGame():
#     pass
# # %%
# observe = game.ObserveForHuman()
# observe
# # %%
# game.Move(8, 2)

# observe = game.ObserveForHuman()
# observe
# # %%
# tmp = game.all_cards[10].heap_list.pop(0)
# game.all_cards[2].MoveInto(tmp)
# # %%
# game.CheckWin()

# %%
# game = FreeCellGame()
# while not game.NewGame():
#     pass
# print(*game.ObserveForHuman(), sep='\n')
# print("\n\n")
# new_game = FreeCellGame(game)
# print(*new_game.ObserveForHuman(), sep='\n')
# print("\n\n")
# st = SearchTree(SearchNode(None, new_game))
# st.TreeUpdate()
# # %%
# res = []
# for x in st.root.child:
#     res.append(st.MaxScore(x))
# print(*res)
# st.RootDeep(st.root.child[res.index(max(res))].oprt)
# st.TreeUpdate()
# # %%
# st.root.state.CheckWin()
# # %%
# st.root.state.ObserveForHuman()
#
# # %%
