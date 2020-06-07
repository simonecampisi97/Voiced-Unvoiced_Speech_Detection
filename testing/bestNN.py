import time
import os
import numpy as np
from time import localtime, strftime

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import EarlyStopping
from tqdm import tqdm

from DataLoader import DataLoader
from DataSet import DataSet
from Net import Net
from utils.saveVariable import save_var, load_var
from utils import model_evaluation

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

    d

    config = tf.compat.v1.ConfigProto()
    config.gpu_options.allow_growth = True
    session = tf.compat.v1.Session(config=config)

    print()
    ds.info()

    X_train, X_val, y_train, y_val = train_test_split(ds.features, ds.labels, test_size=0.33, random_state=42)
    test_set, file_num, frame_num = model_evaluation.load_evaluation_data(
        "C:\\Users\\carot\\Documents\\SPEECH_DATA_ZIPPED\\TEST")
    print()
    print('Train:', X_train.shape)
    print('Val:  ', X_val.shape)
    print('Test: ', test_set.features.shape)
    print()

    size_hidden_layer = [15, 20, 25, 30, 35]

    accuracy_list = []
    h_size = 0

    # early stopping
    es_callback = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=5)

    for h_size in size_hidden_layer:
        print("Size:", h_size, "\n", flush=True)
        time.sleep(.01)

        l = []
        for _ in tqdm(range(10)):
            nn = Net(inputSize=ds.features.shape[1], hiddenSize=h_size)
            nn.compile()
            nn.model.fit(X_train, y_train, batch_size=512, epochs=20, validation_data=(X_val, y_val),
                         verbose=0, callbacks=[es_callback])

            acc, _ = model_evaluation.evaluate_model(nn.model, test_set, verbose=0)
            l.append(acc)
        accuracy_list.append(l)
        print("__________________________________________________")

    saveName = 'ANN_' + strftime("%Y%m%d_%H%M%S", localtime()) + '.txt'
    f = open(saveName, 'w')
    stats = []

    for i, l in enumerate(accuracy_list):
        stats.append([np.mean(l), np.max(l), np.min(l)])
        s = ("h_size={} Avg:{:.5f}  -  Max:{:.5f}  -  Min:{:.5f}".format(size_hidden_layer[i],
                                                                         np.mean(l), np.max(l), np.min(l)))
        print(s)
        f.write(s + "\n")

    stats = np.array(stats)
    best_mean = np.amax(stats[:, 0])
    best_max = np.amax(stats[:, 1])
    best_min = np.amax(stats[:, 2])

    f.write("\n\n"
            "Best mean:{}  size:{}\n"
            "Best max:{}   size:{}\n"
            "Best min:{}   size:{}\n".format(stats[best_mean, 0], best_mean, stats[best_max, 1], best_max,
                                             stats[best_min, 2], best_min))

    f.close()
