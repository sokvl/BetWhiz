from .model import CNN_LSTM_Model

import os
import json
import torch
import torch.nn as nn
import torch.nn.functional as F
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

class ModelManager():
    def __init__(self, model_path, params_path, dict1_path, dict2_path):
        self.dict1 = self.load_dict(dict1_path)
        self.dict2 = self.load_dict(dict2_path)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = self.load_model(model_path, params_path)
        self.max_len = 50
        self.model.eval()  

    def load_model(self, model_path, params_path):
        with open(params_path, 'r') as f:
            model_params = json.load(f)

        vocab_size = len(self.dict2)
        embedding_dim = model_params['embedding_dim']
        lstm_hidden_dim = model_params['lstm_hidden_dim']
        num_classes = model_params['num_classes']
        team_vocab_size = model_params['team_vocab_size']
        self.max_len = model_params['max_len']
        
        model = CNN_LSTM_Model(
            vocab_size=vocab_size, 
            embedding_dim=embedding_dim, 
            lstm_hidden_dim=lstm_hidden_dim, 
            num_classes=num_classes, 
            team_vocab_size=team_vocab_size).to(self.device)

        model.load_state_dict(torch.load(model_path, map_location=self.device))
        print("[Manager]: Model successfully loaded.")
        return model

    def load_dict(self, dict_path):
        with open(dict_path, 'r') as f:
            data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError(f"Expected a dictionary in {dict_path}, but got {type(data)}")
            return data
        
    @staticmethod
    def clean_text(text):
        text = re.sub(r'http\S+', '', text)  
        text = re.sub(r'#\w+', '', text)    
        text = re.sub(r'@\w+', '', text)     
        text = re.sub(r'[^\w\s]', '', text)  
        text = re.sub(r'\n+', ' ', text)     
        text = re.sub(r'\s{2,}', ' ', text)  
        text = text.lower()                  
        return text

    @staticmethod
    def tokenize_and_pad(text, vocab, max_len):
        tokens = word_tokenize(text)
        tokens = [token for token in tokens if token not in stopwords.words('english')]
        encoded_tokens = [vocab.get(token, vocab['<unk>']) for token in tokens]
        padded_tokens = encoded_tokens[:max_len] + [vocab['<pad>']] * (max_len - len(encoded_tokens))
        return torch.tensor(padded_tokens, dtype=torch.long).unsqueeze(0)  
    
    def encode_team(self, team):
        if isinstance(team, dict):
            raise ValueError(f"Expected team to be a string, but got a dictionary: {team}")
        

        encoded_team = self.dict1.get(team, 0)
        
        return torch.tensor([encoded_team], dtype=torch.long).unsqueeze(0)  

    def predict(self, home_team, away_team, tweet):        
        processed_tweet = self.clean_text(tweet)
        processed_tweet = self.tokenize_and_pad(processed_tweet, self.dict2, self.max_len)
        
        input_away_team = self.encode_team(away_team)
        input_home_team = self.encode_team(home_team)

        input_home_team = input_home_team.expand(processed_tweet.size(0), -1)
        input_away_team = input_away_team.expand(processed_tweet.size(0), -1)
        
        processed_tweet = processed_tweet.to(self.device).long() 
        input_home_team = input_home_team.to(self.device).squeeze(1)
        input_away_team = input_away_team.to(self.device).squeeze(1)
        
        with torch.no_grad():
            output = self.model(processed_tweet, input_home_team, input_away_team)
            _, predicted = torch.max(output, 1)
            return predicted.item()

base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, 'model_data', 'cnn_lstm_model.pth')
params_path = os.path.join(base_dir, 'model_data', 'model_params.json')
dict1_path = os.path.join(base_dir, 'model_data', 'team_vocab.json')
dict2_path = os.path.join(base_dir, 'model_data', 'vocab.json')

model_manager = ModelManager(model_path, params_path, dict1_path, dict2_path)