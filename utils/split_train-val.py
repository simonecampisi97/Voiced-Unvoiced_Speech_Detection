import os
import random
import shutil

import numpy as np


def create_tree_directory(root, t="", val_size=0.33, data_dirs=[]):
    os.mkdir(os.path.join(root, "..", "train", t))
    os.mkdir(os.path.join(root, "..", "val", t))

    for folder in os.listdir(os.path.join(root, t)):
        if os.path.isdir(os.path.join(root, t, folder)):
            data_dirs = create_tree_directory(root, os.path.join(t, folder), val_size=val_size, data_dirs=data_dirs)
        else:
            data_dirs.append(os.path.join(root, t))
            break

    return data_dirs


def split_data(root, data_folder, splitting_val):
    train_files = os.listdir(os.path.join(root, data_folder))
    total_size = np.sum([os.path.getsize(file) for file in os.listdir(os.path.join(root, data_folders))])

    id_val_files = []
    curr_val_size = 0
    val_size = total_size * splitting_val

    while True:
        idx = random.randrange(len(train_files))
        idx_size = os.path.getsize(os.path.join(root, data_folder, train_files[idx]))
        if val_size > curr_val_size + idx_size:
            break
        del train_files[idx]
        curr_val_size = curr_val_size + idx_size
        id_val_files.append(idx)

    return id_val_files


def move_data(root, list_of_folder, split_val=0.33):
    for folders in list_of_folder:
        pos_val_files = split_data(root, folders[1], split_val)

        for data_folder in folders:
            train_files = os.listdir(os.path.join(root, data_folder))
            val_files = []

            for el in pos_val_files:
                val_files.append(train_files.pop(el))

            for file in train_files:
                shutil.copyfile(os.path.join(root, data_folder, file),
                                os.path.join(root, "..", "train", data_folder, file))

            for file in val_files:
                shutil.copyfile(os.path.join(root, data_folder, file),
                                os.path.join(root, "..", "val", data_folder, file))

    pass


if __name__ == "__main__":
    data_dir = "C:\\Users\\carot\\Documents\\SPEECH_DATA_ZIPPED\\SPEECH DATA"
    split = 0.3

    print("creating tree directory for training and validation...")
    data_folders = create_tree_directory(data_dir, val_size=split)

    test = []
    for folder in data_folders:
        print(folder)
        speaker = folder.split("\\")[-1]
        ls = [i for i in data_folders if speaker in i]
        for s in ls:
            data_folders.remove(s)
        test.append(ls)
