import pandas as pd
import torch.nn as nn
import torch
import numpy as np
import sys
import torch.optim as opt
from Freecell_Game import FreeCellGame

import DEFINITION

# net param
NUM_i = 52 * 2
NUM_h1 = 256
NUM_h2 = 128
NUM_h3 = 64
NUM_o = 1

# train param
BATCH_SIZE = 256

# model
w1 = torch.tensor(np.random.normal(0, 0.01, (NUM_i, NUM_h1)),
                  dtype=torch.float32, requires_grad=True)
b1 = torch.zeros(NUM_h1, requires_grad=True)
w2 = torch.tensor(np.random.normal(0, 0.01, (NUM_h1, NUM_h2)),
                  dtype=torch.float32, requires_grad=True)
b2 = torch.zeros(NUM_h2, requires_grad=True)
w3 = torch.tensor(np.random.normal(0, 0.01, (NUM_h2, NUM_h3)),
                  dtype=torch.float32, requires_grad=True)
b3 = torch.zeros(NUM_h3, requires_grad=True)
w4 = torch.tensor(np.random.normal(0, 0.01, (NUM_h3, NUM_o)),
                  dtype=torch.float32, requires_grad=True)
b4 = torch.zeros(NUM_o, requires_grad=True)
params = [w1, b1, w2, b2, w3, b3, w4, b4]


def Forward(x):
    x = x.view(-1, NUM_i)
    h1 = nn.LeakyReLU(x.mm(w1) + b1)
    h2 = nn.LeakyReLU(h1.mm(w2) + b2)
    h3 = nn.LeakyReLU(h2.mm(w3) + b3)
    o = nn.LeakyReLU(h3.mm(w4) + b4)
    return o


loss_func = nn.MSELoss()


def main():
    train_data_path = r''
    train_data = pd.read_csv(train_data_path, dtype=DEFINITION.DTYPES, index_col=0)
    train_data_input = train_data.iloc[:, 1:105]
    train_data_output = train_data.loc[:, 'cost']


if __name__ == '__main__':
    main()
