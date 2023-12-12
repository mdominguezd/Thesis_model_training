import subprocess
import os
from Dataset.ReadyToTrain_DS import Img_Dataset
from Dataset.ReadyToTrain_DS import get_DataLoaders
from Dataset import Transforms
from Dataset import Unzip_DS
from Training.Train_DomainOnly import *

from Models import FocalLoss

# Once datasets have been downloaded (Using DS_Download.sh) you can unzip them
Unzip_DS.UnzipFolders("Tanzania")
Unzip_DS.UnzipFolders("IvoryCoast")

# Build Dataset class
train_loader, val_loader, test_loader = get_DataLoaders('TanzaniaSplit1')

n_channels = next(enumerate(train_loader))[1][0].shape[1]
n_classes = 2

# Hyperparameters
number_epochs = 4
learning_rate = 0.1
starter_channels = 8
momentum = 0
bilinear = True
loss_function = FocalLoss(gamma = 1.5)
device = get_training_device()

# Define the network
network = UNet(n_channels, n_classes,  bilinear, starter_channels, up_layer = 4)

# Train the model
f1_val, network_trained = training_loop(network, train_loader, val_loader, learning_rate, starter_channels, momentum, number_epochs, loss_function)

# Evaluate the model
f1_test, loss_test = evaluate(network_trained, test_loader, loss_function, BinaryF1Score(), Love = False)



