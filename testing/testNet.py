import time

from sklearn.model_selection import train_test_split

from DataLoader import DataLoader
from DataSet import DataSet
from Net import Net
from utils.saveVariable import save_var, load_var

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
    print('Train: ', X_train.shape)
    print('Test: ', X_test.shape)

    nn = Net(ds.features.shape[1])
    nn.compile()
    nn.model.fit(X_train, y_train, batch_size=64, epochs=15, validation_data=(X_test, y_test))
