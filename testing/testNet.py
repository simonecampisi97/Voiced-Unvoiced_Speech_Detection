import time
import os
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import EarlyStopping

from DataLoader import DataLoader
from DataSet import DataSet
from Net import Net
from utils.saveVariable import save_var, load_var
import utils.VisualizeNN as VisNN


def plot_history(history):
    plt.figure(figsize=(20, 5))

    # Plot training & validation accuracy values
    plt.subplot(211)
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Val'], loc='upper left')
    # plt.show()

    # Plot training & validation loss values
    plt.subplot(212)
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Val'], loc='upper left')
    plt.show()


def visualizeNN(model, input_shape):
    network_structure = [[input_shape]]

    for layer in model.layers:
        network_structure.append([layer.output_shape[1]])

    network_structure = np.concatenate(network_structure)

    weights_list = []
    for layer in model.layers:
        weights = layer.get_weights()[0]
        curr_max = np.max(np.abs(np.array(weights)))
        for i in range(len(weights)):
            for j in range(len(weights[i])):
                weights[i][j] = weights[i][j] / curr_max
        weights_list.append(weights)

    network = VisNN.DrawNN(network_structure, weights_list)
    network.draw()


if __name__ == "__main__":
    dataset_dir_simo = "C:\\Users\\simoc\\Documents\\SPEECH_DATA_ZIPPED\\SPEECH DATA"
    dataset_dir_ale = "C:\\Users\\carot\\Documents\\SPEECH_DATA_ZIPPED\\SPEECH DATA"

    try:
        ds = load_var("dataset.save")
    except FileNotFoundError:
        try:
            dl = DataLoader(dataset_dir_ale)
        except FileNotFoundError:
            dl = DataLoader(dataset_dir_simo)
        time.sleep(0.01)
        ds = DataSet(dl)
        save_var(ds, "dataset.save")

    config = tf.compat.v1.ConfigProto()
    config.gpu_options.allow_growth = True
    session = tf.compat.v1.Session(config=config)

    print()
    ds.info()

    X_train, X_test, y_train, y_test = train_test_split(ds.features, ds.labels, test_size=0.33, random_state=42)
    # X_train, X_test = standardize_dataset(X_train, X_test)
    print('Train:', X_train.shape)
    print('Test: ', X_test.shape)

    nn = Net(inputSize=ds.features.shape[1])
    start = time.time()

    try:
        nn.load_model()
        nn.load_weights()
        nn.compile()
    except FileNotFoundError:
        nn.compile()
        # early stopping
        es_callback = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=5)

        history = nn.model.fit(X_train, y_train, batch_size=512, epochs=5, validation_split=0.3,
                               verbose=2, callbacks=[es_callback])
        nn.serialize_model()
        nn.serialize_weights()

    end = time.time()
    print("--- %s seconds ---" % (end - start))

    # test_loss, test_acc = nn.model.evaluate(X_test, y_test, verbose=0)
    # print('Test accuracy: %.3f, Test loss: %.3f' % (test_acc, test_loss))

    # test on single file

    # ---------------------------------
    # VISUALIZE NN
    visualizeNN(nn.model, 18)
