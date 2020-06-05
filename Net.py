import numpy as np

from tensorflow.keras.layers import Dense, InputLayer
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import model_from_json

MODEL_PATH = "saved_model/model.json"
WEIGHTS_PATH = "saved_model/model.h5"


class Net:

    def __init__(self, inputSize=18, outputSize=1):
        self.hiddenSize = 3

        self.model = Sequential([InputLayer(input_shape=(inputSize,)),
                                 Dense(16, activation="relu", input_shape=(inputSize,)),
                                 Dense(outputSize, activation="sigmoid")])

    def compile(self, optimizer='adam', loss='binary_crossentropy', metrics=None):
        if metrics is None:
            metrics = ['accuracy']

        self.model.compile(optimizer, loss, metrics)

    def serialize_model(self):
        model_json = self.model.to_json()
        with open(MODEL_PATH, "w") as json_file:
            json_file.write(model_json)

    def serialize_weights(self):
        self.model.save_weights(WEIGHTS_PATH)
        print("Saved model to disk")

    def load_model(self):
        json_file = open(MODEL_PATH, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.model = model_from_json(loaded_model_json)

    def load_weights(self):
        self.model.load_weights(WEIGHTS_PATH)
        print("Loaded model from disk")
