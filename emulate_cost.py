#!python

import Freecell_Game
import pandas as pd
import sys

COLUMN = []
for card_id in range(len(Freecell_Game.CARDS)):
    # card_id + group+id/index
    COLUMN.append(('%02d' % card_id) + 'id')
    COLUMN.append(('%02d' % card_id) + 'index')
COLUMN.append('cost')


class CostEmulator:
    def __init__(self):
        self.game = Freecell_Game.FreeCellGame()
        self.train_data = pd.DataFrame(columns=COLUMN, dtype='uint8')

    def Add(self, hash_index, observe, cost):
        try:
            # to optimize, here index twice.
            if self.train_data.loc[hash_index, 'cost'] > cost:
                self.train_data.loc[hash_index, 'cost'] = cost
        except KeyError:
            self.train_data.loc[hash_index] = observe + [cost]

    def EmulateOnce(self, mode):
        self.game.RandomNewGameAndRecordCost(self, mode)

    def Emulate(self, num, mode):
        while self.train_data.shape[0] < num:
            self.EmulateOnce(mode)
        return


if __name__ == "__main__":
    amount = sys.argv[1]
    data_bag_name = sys.argv[2]
    mode = sys.argv[3]
    emulator = CostEmulator()
    emulator.Emulate(amount, mode)
    emulator.train_data.to_csv('data/' + data_bag_name)
