# -*- coding: utf-8 -*-
"""ai_model(1)

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10kFaZOP4q3OfXsp8vxHKHH8hqozeQhT5
"""

import os
import torch
import torchvision
from torch import nn
from torch.autograd import Variable
from torch.utils.data import Dataset, DataLoader
from torchtext import data
from torchtext.data import TabularDataset
import numpy as np
import pandas as pd

num_epochs = 60
batch_size = 30

learning_rate = 1e-3

#t1_data = pandas dataframe
t1_data = pd.read_csv('data.csv')

nb_users = int(max(t1_data.iloc[:,0])) + 1
nb_foods = int(max(t1_data.iloc[:,1])) + 1
print(nb_foods)

#pandas dataframe -> numpy
t1_data = t1_data.values

print(t1_data)
#numpy array -> pytorch tensor
def convert(data):
    new_data = []
    for id_users in range(0, nb_users):
        id_foods = data[:,1][data[:,0] == id_users]
        id_foods = id_foods.astype(int)
        id_ratings = data[:,2][data[:,0] == id_users]
        ratings = np.zeros(nb_foods)
        ratings[id_foods] = id_ratings
        ratings = ratings.astype(float)
        new_data.append(list(ratings))
    return new_data

t2_data = convert(t1_data)
t2_data = np.asarray(t2_data)

# Numpy array to Pytorch Tensor
tensor = torch.FloatTensor(t2_data)

class FoodDataset(Dataset):
    def __init__(self):
        pass

    def __len__(self):
        return len(tensor)

    def __getitem__(self, index):
        return tensor[index]

dataset = FoodDataset()

num_train_dataset = int(len(dataset) * 0.60)
num_test_dataset = len(dataset) - num_train_dataset
train_dataset, test_dataset = torch.utils.data.random_split(dataset, [num_train_dataset, num_test_dataset])

dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

class autoencoder(nn.Module):
  def __init__(self):
    super(autoencoder, self).__init__()
    self.encoder = nn.Sequential(
        nn.Linear(6, 4),
        nn.ReLU(True),
        nn.Linear(4, 2))
    self.decoder = nn.Sequential(
        nn.Linear(2, 4),
        nn.ReLU(True),
        nn.Linear(4, 6), nn.Tanh())
    
  def forward(self, x):
    x = self.encoder(x)
    x = self.decoder(x)
    return x

model = autoencoder()
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate, weight_decay=1e-3)

for epoch in range(num_epochs):
  for data in dataloader:
    output = model(data)
    loss = criterion(output, data)
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
  print('epoch [{}/{}], loss:{:.4f}'
       .format(epoch +1, num_epochs, loss.item()))