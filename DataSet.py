import sys

import numpy as np
from tqdm import tqdm

from DataLoader import DataLoader


class DataSet:

    def __init__(self, data_loader: DataLoader):
        self.labels = []
        self.features = []
        self.size = 0

        sys.stdout.flush()

        for i in tqdm(range(len(data_loader))):
            _, feature, label = data_loader[i]

            self.labels.append(label)  # np.concatenate((self.labels, label))
            self.features.append(feature)

        self.size = len(self.labels)

        self.labels = np.concatenate(self.labels)
        self.features = np.concatenate(self.features)

    def __len__(self):
        return self.size

    def __getitem__(self, item):
        return self.features[item], self.labels[item]

    def info(self):
        print("Number of frames:", len(self))
        print()

        print("Label length:", len(self.labels))
        print("Feature length:", len(self.features))
