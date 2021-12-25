# %%
import pandas as pd
import torch.nn as nn
import torch
import numpy as np
import sys
import torch.optim as opt
from torch.utils.data import DataLoader, Dataset
from Freecell_Game import FreeCellGame
import DEFINITION

# %%
# config
# net param
NUM_i = 52 * 2
NUM_h1 = 256
NUM_h2 = 128
NUM_h3 = 64
NUM_o = 1

# train param
BATCH_SIZE = 1024
EPOCH = 3

# %%
# utils


class CostDataset(Dataset):
    def __init__(self, csv_path):
        super(CostDataset, self).__init__()
        self.data = pd.read_csv(
            csv_path, dtype=DEFINITION.P_DTYPES, usecols=DEFINITION.COLUMNS[1:]
        )

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        input_data = torch.tensor(
            self.data.iloc[item, 0:-1].values, dtype=torch.float32
        )
        target_data = torch.tensor([self.data.iloc[item, -1]], dtype=torch.float32)
        return input_data, target_data


# %%
# model


class MLP(nn.Module):
    def __init__(self):
        super(MLP, self).__init__()
        self.flatten = nn.Flatten()
        self.layers = nn.Sequential(
            nn.Linear(NUM_i, NUM_h1),
            nn.LeakyReLU(),
            nn.Dropout(0.5),
            nn.Linear(NUM_h1, NUM_h2),
            nn.LeakyReLU(),
            nn.Dropout(0.5),
            nn.Linear(NUM_h2, NUM_h3),
            nn.LeakyReLU(),
            nn.Dropout(0.5),
            nn.Linear(NUM_h3, NUM_o),
        )

    def forward(self, x):
        x = self.flatten(x)
        output = self.layers(x)
        return output


# %%
# train model


def train(model, device, data_loader):
    loss_func = nn.MSELoss()
    optimizer = opt.SGD(model.parameters(), lr=1e-3)
    size = len(data_loader.dataset)
    model.train()  # !!!
    for batch, (x, y) in enumerate(data_loader):
        x, y = x.to(device), y.to(device)
        # compute model error
        model_output = model(x)
        model_output_error = loss_func(model_output, y).to(device)
        # backpropagation
        optimizer.zero_grad()  # !!!
        model_output_error.backward()
        optimizer.step()
        # print loss
        if batch % 100 == 0:
            loss, current = model_output_error.item(), batch * len(x)
            print("loss: %.5f, current: %d/%d" % (loss, current, size))


# evaluate model
def evaluate(model, device, data_loader):
    loss_func = nn.MSELoss()
    size = len(data_loader.dataset)
    num_batch = len(data_loader)
    model.eval()
    model_output_error, current = 0, 0
    with torch.no_grad():
        for x, y in data_loader:
            x, y = x.to(device), y.to(device)
            model_output = model(x)
            model_output_error += loss_func(model_output, y).item()
    model_output_error /= num_batch
    print("average test loss: %.7f" % model_output_error)


if __name__ == "__main__":
    # %%
    # config device
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # read and process tata
    data_path = r"data/10-27-data-p.csv"
    cost_dataset = CostDataset(data_path)
    train_data_num = int(0.9 * len(cost_dataset))
    test_data_num = len(cost_dataset) - train_data_num
    train_dataset, test_dataset = torch.utils.data.random_split(
        dataset=cost_dataset,
        lengths=[train_data_num, test_data_num],
        generator=torch.Generator().manual_seed(13),
    )
    train_data_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    test_data_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=True)
    # build model
    model = MLP().to(device=device)
    # %%
    # train and evaluate
    for i in range(EPOCH):
        print("Epoch: %d" % i)
        train(model, device, train_data_loader)
        evaluate(model, device, test_data_loader)

    # Save model
    torch.save(model.state_dict(), "data/model")
    print("Done")

    # %%
    iter = iter(train_data_loader)
    tmp = next(iter)
    # %%
    tmp[0][1]
    # %%
