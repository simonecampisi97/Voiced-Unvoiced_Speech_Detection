import time

from tensorflow.keras import Sequential

from DataLoader import DataLoader
from DataSet import DataSet
import utils.support_funcion as sf


def load_evaluation_data(evaluate_data_dir: str):
    dl = DataLoader(evaluate_data_dir)

    time.sleep(0.01)
    ds = DataSet(dl)

    file_num = len(dl)
    frame_num = len(ds)

    return ds, file_num, frame_num


def evaluate_model(model: Sequential, testSet: DataSet, verbose=2):
    mean, std = sf.read_std_from_csv('std')
    test_std = sf.standardize_dataset(testSet.features, mean, std)
    results = model.evaluate(x=test_std, y=testSet.labels, batch_size=128, verbose=verbose)

    accuracy = results[-1]
    loss = results[0]

    return accuracy, loss
