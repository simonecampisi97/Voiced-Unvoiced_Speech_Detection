import time

import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import EarlyStopping

from DataLoader import DataLoader
from DataSet import DataSet
from Net import Net
from utils.saveVariable import save_var, load_var


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
    # dataset_dir = "C:\\Users\\simoc\\Documents\\SPEECH_DATA_ZIPPED\\SPEECH DATA"
    dataset_dir = "C:\\Users\\carot\\Documents\\SPEECH_DATA_ZIPPED\\SPEECH DATA"

    try:
        ds = load_var("./dataset.save")
    except FileNotFoundError:
        dl = DataLoader(dataset_dir)
        time.sleep(0.01)
        ds = DataSet(dl)
        save_var(ds, "./dataset.save")

    print()
    ds.info()

    X_train, X_test, y_train, y_test = train_test_split(ds.features, ds.labels, test_size=0.33, random_state=42)
    print('Train:', X_train.shape)
    print('Test: ', X_test.shape)

    nn = Net(ds.features.shape[1])
    nn.compile()

    # early stopping
    es_callback = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=5)

    start = time.time()
    history = nn.model.fit(X_train, y_train, batch_size=512, epochs=15, validation_data=(X_test, y_test),
                           verbose=2, callbacks=[es_callback])
    end = time.time()
    print("--- %s seconds ---" % (end - start))

    plot_history(history)

    weights = nn.model.get_weights()
    print(weights.shape)
    # print(weights)
