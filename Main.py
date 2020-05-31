from frontend.GUI import App
import os

import torch
import torchvision.transforms as transforms

from DataLoader import DataLoader


def load_data(data_dir):
    data_transforms = {
        'train': transforms.Compose([
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor()
        ]),
        'val': transforms.Compose([
            transforms.ToTensor()
        ]),
    }

    image_datasets = {x: DataLoader(os.path.join(data_dir, x), data_transforms[x])
                      for x in ['train', 'val']}

    dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=256,
                                                  shuffle=True, num_workers=4)
                   for x in ['train', 'val']}

    dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'val']}

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(dataset_sizes)


if __name__ == "__main__":
    dataDir = ""
    dataLoader = load_data(dataDir)
    pass
