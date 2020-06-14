import time
import os
import numpy as np
import csv

from utils.support_funcion import standardize_dataset

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

    X_train, mean, std = standardize_dataset(X_train)
    X_test = standardize_dataset(X_test, mean, std)

    if not os.path.exists('std'):
        os.mkdir('std')
        print('Directory std created')
    else:
        print('Directory std already exists')

    with open('std/mean.csv', 'w') as csv_file:
        file_writer = csv.writer(csv_file, delimiter=',',
                                 quotechar='|', quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(mean)

    with open('std/std.csv', 'w') as csv_file:
        file_writer = csv.writer(csv_file, delimiter=',',
                                 quotechar='|', quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(std)

    nn = Net(inputSize=ds.features.shape[1])
    start = time.time()

    try:

        nn.load_weights()
        nn.compile()
    except (FileNotFoundError, OSError):
        nn.compile()
        # early stopping
        es_callback = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=5)

        history = nn.model.fit(X_train, y_train, batch_size=512, epochs=20, validation_split=0.3,
                               verbose=2, callbacks=[es_callback])

        if not os.path.exists('saved_model'):
            os.mkdir('saved_model')
            print('Directory saved_model created')
        else:
            print('Directory saved_model already exists')

        nn.serialize_model()
        nn.serialize_weights()

    end = time.time()
    print("--- %s seconds ---" % (end - start))

    test_loss, test_acc = nn.model.evaluate(X_test, y_test, verbose=0)
    print('Test accuracy: %.3f, Test loss: %.3f' % (test_acc, test_loss))
