import copy
import time
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.models import model_from_json
from keras.layers.normalization import BatchNormalization
from keras.layers.advanced_activations import LeakyReLU
import tensorflow as tf
import numpy as np

MODEL_PATH = "Model/model_nn.json"
WEIGHTS_PATH = "Model/model_weights.h5"


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
    def __init__(self, inputSize, outputSize=1, model=Sequential(), ):
        # parameters
        # TODO: parameters can be parameterized instead of declaring them here
        self.inputSize = inputSize
        self.outputSize = outputSize
        self.hiddenSize = 3
        self.model = model

    def create_and_compile_model(self):
        self.model.add(Dense(units=32, activation='relu', input_dim=self.inputSize))
        self.model.add(Dense(units=1, activation='sigmoid'))
        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    def save_model(self):
        model_json = self.model.to_json()
        with open(MODEL_PATH, "w") as json_file:
            json_file.write(model_json)
        self.model.save_weights(WEIGHTS_PATH)

    def load_model(self):
        with open(MODEL_PATH, "r") as json_file:
            model_json = json_file.read()
        self.model = model_from_json(model_json)
        self.model.load_weights(WEIGHTS_PATH)
        print("Model loaded from disk")
