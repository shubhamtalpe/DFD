import torch
from torch import nn
from torchvision import models

class LSTM_model(nn.Module):

    def __init__(self, num_classes, latent_dim = 2048, lstm_layers = 1, hidden_dim = 2048, bidirectional = False):

        super(LSTM_model, self).__init__()

        model = models.resnext50_32x4d(pretrained = True)

        self.model = nn.Sequential(*list(model.children())[:-2])
        self.lstm = nn.LSTM(latent_dim, hidden_dim, lstm_layers, bidirectional)
        self.relu = nn.LeakyReLU()
        self.dp = nn.Dropout(0.4)
        self.linear1 = nn.Linear(2048, num_classes)
        self.avgpool = nn.AdaptiveAvgPool2d(1)

    def forward(self, x):
        if len(x.shape) == 5:
            batch_size, seq_length, h, w, c = x.shape
        else:
            batch_size = 1
            seq_length, h, w, c = x.shape

        x = x.view(batch_size * seq_length, c, h, w)
        
        fmap = self.model(x)
        
        x = self.avgpool(fmap)
        
        x = x.view(batch_size, seq_length, 2048)
        
        x_lstm, _ = self.lstm(x, None)
        
        return fmap, self.drop(self.linear1(torch.mean(x_lstm, dim = 1)))