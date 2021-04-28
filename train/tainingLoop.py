import glob
import random
import numpy as np
import pandas as pd

import helpers
from LSTM_model import LSTM_model
from video_dataset import video_dataset

import torch
torch.cuda.empty_cache()

from torch import nn
from torchvision import transforms
from torch.utils.data import DataLoader

checkpoint_path = '/home/cypher/2ndSet/checkpoint.pt'
file_names = glob.glob('/home/cypher/2ndSet/*/*.mp4')
random.shuffle(file_names)
labels = pd.read_csv('/home/cypher/2ndSet/metadata.csv', header = None, names = ['file', 'label'])

train_vids = file_names[:int(0.9 * len(file_names))]
valid_vids = file_names[int(0.9 * len(file_names)):]

mean = [0.485, 0.456, 0.406]
std = [0.229, 0.224, 0.225]

IMG_WIDTH = IMG_HEIGHT = 112
batch_size = 1
sequence_length = 60

train_transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((IMG_WIDTH, IMG_HEIGHT)),
    transforms.ToTensor(),
    transforms.Normalize(mean,std)
])

valid_transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((IMG_WIDTH, IMG_HEIGHT)),
    transforms.ToTensor(),
    transforms.Normalize(mean,std)
])

train_data = video_dataset(train_vids, labels, sequence_length = sequence_length, transform = train_transform)
valid_data = video_dataset(valid_vids, labels, sequence_length = sequence_length, transform = valid_transform)

train_loader = DataLoader(train_data, batch_size = batch_size, shuffle = True)
valid_loader = DataLoader(valid_data, batch_size = batch_size, shuffle = True)

if torch.cuda.is_available():
    model = LSTM_model(2).cuda()
    a, b = model(torch.from_numpy(np.empty((1, sequence_length, IMG_WIDTH, IMG_HEIGHT, 3))).type(torch.cuda.FloatTensor))
else:
    model = LSTM_model(2)
    a, b = model(torch.from_numpy(np.empty((1, sequence_length, IMG_WIDTH, IMG_HEIGHT, 3))).type(torch.FloatTensor))

model = helpers.load_model(model, checkpoint_path)

criterion = nn.CrossEntropyLoss().cuda()
optimizer = torch.optim.Adam(model.parameters(), lr = 1e-5,weight_decay = 1e-5)


num_epochs = 20

train_loss_avg = []
train_accuracy = []
test_loss_avg = []
test_accuracy = []

for epoch in range(1, num_epochs + 1):
    l, acc = helpers.train(epoch, num_epochs, train_loader, model, criterion, optimizer, checkpoint_path)
    
    train_loss_avg.append(l)
    train_accuracy.append(acc)

    true, pred, tl, tacc = helpers.test(epoch, model, valid_loader, criterion)

    test_loss_avg.append(tl)
    test_accuracy.append(tacc)