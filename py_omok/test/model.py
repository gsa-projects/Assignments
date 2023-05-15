import torch
import os
import numpy as np
import re
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as d
datas = np.zeros((0, 15, 15), dtype=int)
for file_path in os.listdir('dataset'):
    with open('./dataset/'+file_path, 'r') as file:
        origin = np.array(list(map(int, re.compile(r'(\d+)\.').findall(file.read())))).reshape((15, 15))
        fliplr, flipud = np.fliplr(origin), np.flipud(origin)
        for mat in (origin, fliplr, flipud):
            datas = np.append(datas, mat.reshape((1, 15, 15)), axis=0)
            datas = np.append(datas, np.rot90(mat, 1).reshape((1, 15, 15)), axis=0)
            datas = np.append(datas, np.rot90(mat, 3).reshape((1, 15, 15)), axis=0)
            datas = np.append(datas, np.rot90(mat, 4).reshape((1, 15, 15)), axis=0)
x_train = torch.zeros((0, 15, 15))
y_train = torch.zeros((0, 15, 15))
for i, data in enumerate(datas):
    after = data.copy()
    after[after > 1] = 0
    for max_value in range(2, np.amax(data) + 1):
        before = after
        after = data.copy()
        after[after > max_value] = 0
        x_train = np.append(x_train, before.reshape((1, 15, 15)), axis=0)
        y_train = np.append(y_train, after.reshape((1, 15, 15)), axis=0)
        print(f'Board {i + 1}: {max_value:2d}/{np.amax(data):2d}')
x_train = torch.from_numpy(x_train).float().unsqueeze(1)
y_train = torch.from_numpy(y_train).float().unsqueeze(1)
dataset = d.TensorDataset(x_train, y_train)
dataloader = d.DataLoader(dataset, batch_size=32, shuffle=True)
model = nn.Sequential(nn.Conv2d(1, 64, kernel_size=3, padding=1), nn.ReLU(), nn.Conv2d(64, 128, kernel_size=3, padding=1), nn.ReLU(), nn.Conv2d(128, 256, kernel_size=3, padding=1), nn.ReLU(), nn.Conv2d(256, 1, kernel_size=1))
cost = nn.MSELoss()
optimizer = optim.Adam(model.parameters())
epochs = 5
for epoch in range(1, epochs + 1):
    run_loss = 0.
    loss_total = 0.
    for i, (x, y) in enumerate(dataloader):
        prediction = model(x)
        loss = cost(prediction, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        run_loss += loss.item() * x.size(0)
        print(f'epoch: {epoch:2d}/{epochs} {i}/{len(dataloader)} cost: {loss_total:.6f}')
torch.save(model, 'models/model.pt')