from typing_extensions import Required
import torch.nn as nn
import torch
import numpy as np
import torch.optim as opt
from Freecell_Game import FreeCellGame

# net param
NUM_i = 52*2
NUM_h1 = 1024
NUM_h2 = 512
NUM_h3 = 512
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

# relu


def Forward(x):
    x = x.view(-1, NUM_i)
    h1 = nn.LeakyReLU(x.mm(w1)+b1)
    h2 = nn.LeakyReLU(h1.mm(w2)+b2)
    h3 = nn.LeakyReLU(h2.mm(w3)+b3)
    o = nn.LeakyReLU(h3.mm(w4)+b4)
    return o


def
