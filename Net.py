import torch
import torch.nn as nn
import copy
import time


def train_model(model, dataloaders, criterion, optimizer, scheduler, num_epochs=25):
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
                model.eval()   # Set model to evaluate mode

            running_loss = 0.0
            running_corrects = 0
            # Iterate over data.
            for path,inputs, labels,b in dataloaders[phase]:
               
                device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
                #move to gpu
                inputs = inputs.clone().detach().to(device)
                labels = labels.clone().detach().to(device)
                b = b.clone().detach().requires_grad_(True).to(device)
                
                # zero the parameter gradients
                optimizer.zero_grad()

                # forward
                # track history if only in train
                with torch.set_grad_enabled(phase == 'train'):
                    ##Pass the input to the mode, what outputs are we expecting?
                    classes, boxes = model(inputs)                 
                    
                    ##Calculate each loss and combine them in the multitask loss
                    loss = criterion(classes, labels)

                    # backward + optimize only if in training phase
                    if phase == 'train':
                        loss.backward()                        
                        optimizer.step()
                    
                # statistics
                #Assess the accuracy of the localization (hint: use mean iou) and of the classification
                running_loss += loss.item() * inputs.size(0)
                winners = classes.argmax(dim=1)
                running_corrects += torch.sum(winners == labels)
                
            if phase == 'train':
                scheduler.step()
            
            epoch_loss = running_loss / dataset_sizes[phase]
            epoch_acc = running_corrects.double() / dataset_sizes[phase]
            
            print('{}: Loss: {:.4f}  -  Acc(classification): {:.4f}'.format(
                                                                            phase,
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


class Neural_Network(nn.Module):
    def __init__(self, ):
        super(Neural_Network, self).__init__()
        # parameters
        # TODO: parameters can be parameterized instead of declaring them here
        self.inputSize = 15
        self.outputSize = 1
        self.hiddenSize = 3

        # weights
        self.layer1 = nn.Linear(self.inputSize, self.hiddenSize)
        self.layer2 = nn.Linear(self.hiddenSize, self.outputSize)

    def forward(self, X):
        x = self.layer1(x)
        x = nn.ReLU(x)
        x = self.layer2(X)
        x = nn.Sigmoid(x)
        return x

    def train(self, X, y):
        o = self.forward(X)
        self.backward(X, y, o)

    def saveWeights(self, model):
        # we will use the PyTorch internal storage functions
        torch.save(model, "NN")
        # you can reload model with all the weights and so forth with:
        # torch.load("NN")

    def predict(self):
        print("Predicted data based on trained weights: ")
        print("Input (scaled): \n" + str("TO IMPLEMENT"))
        # print("Output: \n" + str(self.forward("TO IMPLEMENT")))


