import torchvision.transforms as transforms
from librosa.core import load
from sklearn.model_selection import train_test_split

from DataLoader import DataLoader
from DataSet import DataSet
from ParametersExtraction import *

if __name__ == "__main__":
    dataset_dir = "C:\\Users\\simoc\\Documents\\SPEECH_DATA_ZIPPED\\SPEECH DATA"
    # dataset_dir = "C:\\Users\\carot\\Documents\\SPEECH_DATA_ZIPPED\\SPEECH DATA"

    transform = transforms.Compose(
        [transforms.ToTensor()])

    dl = DataLoader(dataset_dir)

    ds = DataSet(dl)
    ds.info()

    X_train, X_test, y_train, y_test = train_test_split(range(len(ds)), test_size=0.33, random_state=42)

    exit()

    _, feature, label = dl[0]

    print("Type feature:", type(feature))
    print("Type labels:", (type(label)))
    print()

    print("Size feature:", feature.shape)
    print("Size labels:", label.shape)
    print()

    print(type(label[0]), label[0])
