import Freecell_Game
import pandas as pd

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

    def EmulateOnce(self):
        self.game.RandomNewGameAndRecordCost(self)

    def EmulateUntilAmount(self, num):
        while self.train_data.shape[0] < num:
            self.EmulateOnce()
        return


if __name__ == "__main__":
    emulator = CostEmulator()
    emulator.EmulateUntilAmount(500)
    emulator.train_data.to_csv(r'./data/test.csv')
