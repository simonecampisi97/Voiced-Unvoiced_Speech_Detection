from DataLoader import DataLoader

if __name__ == "__main__":

    dataset_dir = "C:\\Users\\carot\\Documents\\SPEECH_DATA_ZIPPED\\SPEECH DATA"
    dl = DataLoader(dataset_dir)

    for i in range(len(dl)):
        print(i)
        tmp = dl[i]
