import numpy as np

from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import model_from_json

MODEL_PATH = "Model/model_nn.json"
WEIGHTS_PATH = "Model/model_weights.h5"


class Net:

    def __init__(self, inputSize, outputSize=1):
        self.hiddenSize = 3

        self.model = Sequential([Dense(30, activation="relu", input_shape=(inputSize,)),
                                 Dense(outputSize, activation="sigmoid")])

    def compile(self, optimizer='adam', loss='binary_crossentropy', metrics=None):
        if metrics is None:
            metrics = ['accuracy']

        self.model.compile(optimizer, loss, metrics)

    def serialize_model(self):
        model_json = self.model.to_json()
        with open("model.json", "w") as json_file:
            json_file.write(model_json)

    def serialize_weights(self):
        self.model.save_weights("model.h5")
        print("Saved model to disk")

    def load_model(self):
        json_file = open('model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.model = model_from_json(loaded_model_json)

    def load_weights(self):
        self.model.load_weights("model.h5")
        print("Loaded model from disk")
