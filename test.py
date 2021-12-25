#!python

# %%
import random
import pandas as pd
import numpy as np
import torch
import Freecell_Game
import MLP

# %%
model = MLP.MLP()
model.load_state_dict(torch.load("data/model"))
# %%
game = Freecell_Game.FreeCellGame()
game.NewGame()
# %%
X = torch.tensor([game.ObserveForNet()], dtype=torch.float32)
# %%
model.eval()
Y = model(X)

# %%
int(Y[0][0] * 100)
# %%
