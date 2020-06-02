import time

from sklearn.model_selection import train_test_split

from DataLoader import DataLoader
from DataSet import DataSet
from utils.saveVariable import load_var, save_var

if __name__ == "__main__":
    # dataset_dir = "C:\\Users\\simoc\\Documents\\SPEECH_DATA_ZIPPED\\SPEECH DATA"
    dataset_dir = "C:\\Users\\carot\\Documents\\SPEECH_DATA_ZIPPED\\SPEECH DATA"

    try:
        ds = load_var("./dataset.save")
        print('Dataset loaded from a local file')
    except FileNotFoundError:
        print('Creating the dataset:', flush=True)
        dl = DataLoader(dataset_dir)
        print("\t-Found {} files".format(len(dl)))

        print("\t-Extracting features from row data...", flush=True)
        time.sleep(0.01)
        ds = DataSet(dl)
        save_var(ds, "./dataset.save")
        print("\t-Dataset saved as local file")

    print()
    ds.info()

    X_train, X_test, y_train, y_test = train_test_split(ds.features, ds.labels, test_size=0.33, random_state=42)

    print()
    print('Train: ', X_train.shape)
    print('Test: ', X_test.shape)
