import copy
import time
import keras
from keras.models import Sequential, Input, Model
from keras.layers import Dense, Dropout, Flatten
from keras.layers.normalization import BatchNormalization
from keras.layers.advanced_activations import LeakyReLU
from sklearn.metrics import accuracy_score
import tensorflow as tf
import numpy as np


def standardize_dataset(X_train, X_test):

    means = []
    stds = []

    for x_i in X_train:
        means.append(np.mean(x_i))  # Computing the image mean
        stds.append(np.std(x_i))  # Computing the image standard deviation

    dataset_mean = np.mean(means)  # Computing the dataset mean
    dataset_std = np.mean(stds)  # Computing the dataset standard deviation

    X_train_norm = (X_train - dataset_mean) / dataset_std
    X_test_norm = (X_test - dataset_mean) / dataset_std

    return X_train_norm, X_test_norm


class Net:
    def __init__(self, inputSize, outputSize=1):

        # parameters
        # TODO: parameters can be parameterized instead of declaring them here
        self.inputSize = inputSize
        self.outputSize = outputSize
        self.hiddenSize = 3
        self.loss = keras.losses.binary_crossentropy
        self.optimizer = keras.optimizers.Adam()
        self.model = Sequential()
        # weights
        self.layer1 = Linear(self.inputSize, self.hiddenSize)
        self.relu = nn.ReLU()

        self.layer2 = nn.Linear(self.hiddenSize, self.outputSize)
        self.sigmoid = nn.Sigmoid()


    def save_model(self, path):
        torch.save(self.state_dict(), path)

    def load_model(self, path):
        self.load_state_dict(torch.load(path))
        self.eval()
