from keras.models import model_from_json


def serialize_model(self):
    model_json = self.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)


def serialize_weights(self):
    self.save_weights("model.h5")
    print("Saved model to disk")


def load_model(self):
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    self.model = model_from_json(loaded_model_json)


def load_weights(self):
    self.model.load_weights("model.h5")
    print("Loaded model from disk")
