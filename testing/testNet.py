import time

import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import EarlyStopping

import numpy as np

from DataLoader import DataLoader
from DataSet import DataSet
from Net import Net
from utils.saveVariable import save_var, load_var
import tensorflow as tf
from utils.support_funcion import plot_model_prediction


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


def standardize_dataset(Xtr, Xte=None):
    dataset_mean = np.mean(Xtr, axis=0)  # Computing the dataset mean
    dataset_std = np.std(Xtr, axis=0)  # Computing the dataset standard deviation

    X_train_norm = (Xtr - dataset_mean) / dataset_std
    if Xte is not None:
        X_test_norm = (Xte - dataset_mean) / dataset_std
        return X_train_norm, X_test_norm
    else:
        return X_train_norm


if __name__ == "__main__":
    dataset_dir_simo = "C:\\Users\\simoc\\Documents\\SPEECH_DATA_ZIPPED\\SPEECH DATA"
    dataset_dir_ale = "C:\\Users\\carot\\Documents\\SPEECH_DATA_ZIPPED\\SPEECH DATA"

    try:
        ds = load_var("./dataset.save")
    except FileNotFoundError:
        try:
            dl = DataLoader(dataset_dir_ale)
        except FileNotFoundError:
            dl = DataLoader(dataset_dir_simo)
        time.sleep(0.01)
        ds = DataSet(dl)
        save_var(ds, "./dataset.save")

    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    session = tf.Session(config=config)

    print()
    ds.info()

    X_train, X_test, y_train, y_test = train_test_split(ds.features, ds.labels, test_size=0.33, random_state=42)
    # X_train, X_test = standardize_dataset(X_train, X_test)
    print('Train:', X_train.shape)
    print('Test: ', X_test.shape)

    nn = Net(ds.features.shape[1])
    start = time.time()

    try:
        nn.load_model()
        nn.load_weights()
        nn.compile()
    except FileNotFoundError:
        nn.compile()
        # early stopping
        es_callback = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=5)

        history = nn.model.fit(X_train, y_train, batch_size=512, epochs=15, validation_split=0.3,
                               verbose=2, callbacks=[es_callback])
        nn.serialize_model()
        nn.serialize_weights()

    end = time.time()
    print("--- %s seconds ---" % (end - start))

    # test_loss, test_acc = nn.model.evaluate(X_test, y_test, verbose=0)
    # print('Test accuracy: %.3f, Test loss: %.3f' % (test_acc, test_loss))

    # test on single file
    path_file = 'C:\\Users\\simoc\\SPR_Project\\TestData\\mic_M03_sa1.wav'
    #plot_model_prediction(path_file=path_file,data_root=dataset_dir_simo,model=nn.model)
