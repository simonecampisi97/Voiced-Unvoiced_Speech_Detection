import copy
import time
import keras
from keras.models import Sequential,Input,Model
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization
from keras.layers.advanced_activations import LeakyReLU
from sklearn.metrics import accuracy_score
import numpy as np
import torch
import torch.nn as nn


def standardize_dataset(X_train, X_test):
    means = []
    stds = []

    for x_i in X_train:
        means.append(np.mean(x_i))  # Computing the image mean
        stds.append(np.std(x_i))  # Computing the image standard deviation

    dataset_mean = np.mean(means)  # Computing the dataset mean
    dataset_std = np.mean(stds)  # Computing the dataset standard deviation

    X_train_norm = (X_train - dataset_mean) / dataset_std
    X_test_norm = (X_test - dataset_mean) / dataset_std

    return X_train_norm, X_test_norm


def train_model(model, dataloaders, dataset_sizes, criterion, optimizer, scheduler, num_epochs=25):
    since = time.time()

    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0

    for epoch in range(num_epochs):
        print('Epoch {}/{}'.format(epoch, num_epochs - 1))
        print('-' * 10)

        # Each epoch has a training and validation phase
        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()  # Set model to training mode
            else:
                model.eval()  # Set model to evaluate mode

            running_loss = 0.0
            running_corrects = 0
            # Iterate over data.
            for path, inputs, labels in dataloaders[phase]:

                device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
                # move to gpu
                inputs = inputs.clone().detach().to(device)
                labels = labels.clone().detach().to(device)

                # zero the parameter gradients
                optimizer.zero_grad()

                # forward
                # track history if only in train
                with torch.set_grad_enabled(phase == 'train'):
                    # Pass the input to the mode, what outputs are we expecting?
                    classes = model(inputs)

                    # Calculate each loss and combine them in the multitask loss
                    loss = criterion(classes, labels)

                    # backward + optimize only if in training phase
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                # statistics
                # TODO da sistemare
                running_loss += loss.item() * inputs.size(0)
                winners = classes.argmax(dim=1)
                running_corrects += torch.sum(winners == labels)

            if phase == 'train':
                scheduler.step()

            epoch_loss = running_loss / dataset_sizes[phase]
            epoch_acc = running_corrects.double() / dataset_sizes[phase]

            print('{}: Loss: {:.4f}  -  Acc(classification): {:.4f}'.format(phase,
                                                                            epoch_loss,
                                                                            epoch_acc))

            # deep copy the model
            if phase == 'val' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model_wts = copy.deepcopy(model.state_dict())
        print()

    time_elapsed = time.time() - since
    print('Training complete in {:.0f}m {:.0f}s'.format(
        time_elapsed // 60, time_elapsed % 60))
    print('Best val Acc: {:4f}'.format(best_acc))

    # load best model weights
    model.load_state_dict(best_model_wts)
    return model


class Net(nn.Module):
    def __init__(self, inputSize, outputSize=1):
        super(Net, self).__init__()
        # parameters
        # TODO: parameters can be parameterized instead of declaring them here
        self.inputSize = inputSize
        self.outputSize = outputSize
        self.hiddenSize = 3

        # weights
        self.layer1 = nn.Linear(self.inputSize, self.hiddenSize)
        self.relu = nn.ReLU()

        self.layer2 = nn.Linear(self.hiddenSize, self.outputSize)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # Layer 1
        out = self.layer1(x)
        out = self.relu(out)

        # Layer 2
        out = self.layer2(out)
        y = self.sigmoid(out)

        return y

    def save_model(self, path):
        torch.save(self.state_dict(), path)

    def load_model(self, path):
        self.load_state_dict(torch.load(path))
        self.eval()
