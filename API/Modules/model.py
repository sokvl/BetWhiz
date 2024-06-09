import torch
import torch.nn as nn
import torch.nn.functional as F

class CNN_LSTM_Model(nn.Module):
    def __init__(self, vocab_size, embedding_dim, lstm_hidden_dim, num_classes, team_vocab_size):
        super(CNN_LSTM_Model, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        self.team_embedding = nn.Embedding(team_vocab_size, embedding_dim)

        self.conv1 = nn.Conv2d(1, 128, (3, embedding_dim))
        self.conv2 = nn.Conv2d(1, 128, (4, embedding_dim))
        self.conv3 = nn.Conv2d(1, 128, (5, embedding_dim))
        self.lstm = nn.LSTM(128 * 3, lstm_hidden_dim, batch_first=True, bidirectional=True)

        self.dropout = nn.Dropout(0.5)
        self.fc1 = nn.Linear(lstm_hidden_dim * 2 + embedding_dim * 2, 256)
        self.fc2 = nn.Linear(256, num_classes)

    def forward(self, x_text, x_home, x_away):
        x_text = self.embedding(x_text).unsqueeze(1) 

        x1 = F.relu(self.conv1(x_text)).squeeze(3)
        x1 = F.max_pool1d(x1, x1.size(2)).squeeze(2)

        x2 = F.relu(self.conv2(x_text)).squeeze(3)
        x2 = F.max_pool1d(x2, x2.size(2)).squeeze(2)

        x3 = F.relu(self.conv3(x_text)).squeeze(3)
        x3 = F.max_pool1d(x3, x3.size(2)).squeeze(2)

        x_text = torch.cat((x1, x2, x3), 1).unsqueeze(1) 
        
        lstm_out, _ = self.lstm(x_text)
        lstm_out = lstm_out[:, -1, :]  
        
        x_home = self.team_embedding(x_home)
        x_away = self.team_embedding(x_away)
        x = torch.cat((lstm_out, x_home, x_away), 1)
        x = self.dropout(x)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        return self.fc2(x)