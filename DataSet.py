import sys

import numpy as np
from tqdm import tqdm
import utils.support_funcion as sf
from DataLoader import DataLoader


class DataSet:

    def __init__(self, data_loader: DataLoader):
        self.labels = []
        self.features = []
        self.size = 0

        # standardization data
        self.mean = 1
        self.std  = 1

        sys.stdout.flush()

        for i in tqdm(range(len(data_loader))):
            _, feature, label = data_loader[i]

            self.labels.append(label)  # np.concatenate((self.labels, label))
            self.features.append(feature)

        self.labels = np.expand_dims(np.concatenate(self.labels), axis=1)
        self.features = np.concatenate(self.features)

        self.size = len(self.labels)

    def __len__(self):
        return self.size

    def __getitem__(self, item):
        return self.features[item], self.labels[item]

    def info(self):
        print("Dataset info:")
        print("\t-Number of frames:", len(self))

        print("\t-Label shape:  ", self.labels.shape)
        print("\t-Feature shape:", self.features.shape)

    def standardize(self):
        self.features, mean, std = sf.standardize_dataset(self.features)
        self.mean = mean
        self.std = std
