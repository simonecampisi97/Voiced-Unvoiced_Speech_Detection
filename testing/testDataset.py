import torchvision.transforms as transforms
from tqdm import tqdm

from DataLoader import DataLoader
from DataSet import DataSet

if __name__ == "__main__":
    dataset_dir = "C:\\Users\\simoc\\Documents\\SPEECH_DATA_ZIPPED\\SPEECH DATA"
    # dataset_dir = "C:\\Users\\carot\\Documents\\SPEECH_DATA_ZIPPED\\SPEECH DATA"

    transform = transforms.Compose(
        [transforms.ToTensor()])

    dl = DataLoader(dataset_dir)
    print("Found {} files...".format(len(dl)))

    print("\nCreating dataset from row data...", flush=True)
    ds = DataSet(dl)
    ds.info()

    for i in tqdm(range(len(ds))):
        tmp = ds[i]
