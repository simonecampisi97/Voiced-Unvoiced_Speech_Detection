import torchvision.transforms as transforms
from librosa.core import load
from sklearn.model_selection import train_test_split
from utils.saveVariable import *

from DataLoader import DataLoader
from DataSet import DataSet
from ParametersExtraction import *

if __name__ == "__main__":
    dataset_dir = "C:\\Users\\simoc\\Documents\\SPEECH_DATA_ZIPPED\\SPEECH DATA"
    # dataset_dir = "C:\\Users\\carot\\Documents\\SPEECH_DATA_ZIPPED\\SPEECH DATA"

    try:
        ds = load_var("Model/dataset")
        print('Load dataset from binary file...')
    except FileNotFoundError:
        print('creating dataset')
        dl = DataLoader(dataset_dir)
        ds = DataSet(dl)
        save_var(ds, "Model/dataset")

    ds.info()

    print('feature. ', ds.features.shape)

    X_train, X_test, y_train, y_test = train_test_split(ds.features, ds.labels, test_size=0.33, random_state=42)

    print('Train: ', X_train.shape)
    print('Test: ', X_test.shape)