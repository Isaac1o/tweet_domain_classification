import pandas as pd
import torch
from torch.utils.data import Dataset


class TweetDataset(Dataset):
    def __init__(self, data, vocab, max_len):
        self.data = data
        self.vocab = vocab
        self.max_len = max_len

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        row = self.data.iloc[idx]
        tokens = row['tokens']

        # Front paddings
        X = torch.zeros(self.max_len)
        for i, token in enumerate(tokens):
            X[self.max_len - len(tokens) + i] = self.vocab.get(token, 1)

        y = torch.tensor(row['label']).float()

        return X.long(), y