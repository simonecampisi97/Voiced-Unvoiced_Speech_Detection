import torchvision.transforms as transforms

from DataLoader import DataLoader

if __name__ == "__main__":
    #    dataset_dir = "C:\\Users\\simoc\\Documents\\SPEECH_DATA_ZIPPED_CUSTOM\\SPEECH DATA"
    dataset_dir = "C:\\Users\\carot\\Documents\\SPEECH_DATA_ZIPPED\\SPEECH DATA"

    transform = transforms.Compose(
        [transforms.ToTensor()])

    dl = DataLoader(dataset_dir, transform)

    feature, label = dl[0]

    print("type feature", type(feature))
    print("type labels", (type(label)))

    print("size feature", feature.shape)
    print("size labels", label.shape)

    print(type(label[0]), label[0])
