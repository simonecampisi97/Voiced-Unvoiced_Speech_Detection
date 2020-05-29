from DataLoader import DataLoader


if __name__ == "__main__":

    dataset_dir = "C:\\Users\\simoc\\Documents\\SPEECH_DATA_ZIPPED_CUSTOM\\SPEECH DATA"
    dl = DataLoader(dataset_dir)

    for i in range(len(dl)):
        print(i)
        tmp = dl[i]
