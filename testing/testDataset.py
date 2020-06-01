import torchvision.transforms as transforms

from DataLoader import DataLoader

if __name__ == "__main__":
    dataset_dir = "C:\\Users\\simoc\\Documents\\SPEECH_DATA_ZIPPED\\SPEECH DATA"
    # dataset_dir = "C:\\Users\\carot\\Documents\\SPEECH_DATA_ZIPPED\\SPEECH DATA"

    transform = transforms.Compose(
        [transforms.ToTensor()])

    dl = DataLoader(dataset_dir, transform)

    _, feature, label = dl[0]

    print("Type feature:", type(feature))
    print("Type labels:", (type(label)))
    print()

    print("Size feature:", feature.shape)
    print("Size labels:", label.shape)
    print()

    print(type(label[0]), label[0])
