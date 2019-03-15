import os

import torch
import torchvision
from torch import nn
from torch.autograd import Variable
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.datasets import MNIST
from torchvision.utils import save_image
import functools
import operator
import csv
import time
import numpy as np
import pandas as pd
import torch.utils.data as utils


if not os.path.exists('./autoencoder_img'):
    os.mkdir('./autoencoder_img')


num_epochs = 100
batch_size = 64
learning_rate = 1e-3
img_transform = transforms.Compose([transforms.ToTensor()])    #-------------------------------------we do not want to normalize


#------------------------Unroll the joint state list of lists into a single list
# joint_state_list_of_lists = []
# joint_state_list_of_lists = functools.reduce(operator.iconcat, joint_state_list_of_lists, [])
#
# size_of_input_dimension_of_joint_state = len(joint_state_list_of_lists)

#---------------------------get data

# with open("csv_for_joint_states.csv","r") as readfile:
#     reader = csv.reader(readfile)




myfilename = "../data/rover_domain_datasets/data_4_10_20.txt"
f=open(myfilename,'r')
line = f.readline()
line_cnt = 1
states=[]
temp_line=[]
while line:
    line = line.replace('[', "")
    line = line.replace('\n', "")
    line = line.replace(']', "")
    line = line.split()

    for item in line:
        temp_line.append(item)

    if line_cnt%7 == 0:
        states.append(temp_line)
        temp_line=[]

    line = f.readline()
    line_cnt += 1

#print(len(states[0]))
# for i in range(3333):
    # print(states[i])
    # time.sleep(2666)

#---------------------------------Write the joint state spaces into a CSV
#
# with open('csv_for_joint_states.csv', 'w', newline='') as csvfile: #-----------------index = False nagare feri index pani banaidinxa
#     writer = csv.writer(csvfile)
#     writer.writerows(states)
# reader = []

#
# data_without_index = states.to_csv('csv_for_joint_states_new.csv',mode = 'w', index=False)
#
# #----------------------------------Read the joint state spaces from the csv
# with open("csv_for_joint_states.csv_new","r") as readfile:
#     reader = csv.reader(readfile)
#
#     # for index,data in enumerate(reader):
#     #      print(index,data)
#     #      time.sleep(5)
#
# print(reader[0])
# time.sleep(5)
#
#training_dataset = pd.read_csv('csv_for_joint_states.csv')

##dataset = None #
#a = np.array(states)
#print(a[0])
#

# states = np.array(states)


states = np.array(states)
a = list(states)


my_x = [a] # a list of numpy arrays
my_y = [np.zeros(len(states))] # another list of numpy arrays (targets)

tensor_x = torch.stack([torch.Tensor(i) for i in a]) # transform to torch tensors
tensor_y = torch.stack([torch.Tensor(i) for i in my_y])
time.sleep(222)
my_dataset = utils.TensorDataset(tensor_x,tensor_y) # create your datset
my_dataloader = utils.DataLoader(my_dataset) # create your dataloader







# #time.sleep(44)
# # y_vals = np.zeros(len(states))
# x_in_dataset = []
# #y_in_dataset = []
# y_in_dataset[] = .append(np.array([0.], dtype = float))

for i in range(len(states)): # one lakh ota i

    x_in_dataset.append(np.array([states[i]], dtype= float))
    # print(x_in_dataset)
    # print("\n")
    # time.sleep(5)
    y_in_dataset.append(np.array([0.], dtype = float))

# my_x = [states] # a list of numpy arrays
# my_y = [np.array([4.]), np.array([2.])] # another list of numpy arrays (targets)


#print(len(x_in_dataset))
#time.sleep(222)
#x_in_dataset = [np.array([[1.0, 2], [3, 4]]), np.array([[5., 6], [7, 8]])] # a list of numpy arrays
#y_in_dataset = [np.array([4.]), np.array([2.])] # another list of numpy arrays (targets)
#print(torch.Tensor(x_in_dataset[2]))
#time.sleep(5)

# tensor_x = torch.stack([torch.Tensor(i) for i in x_in_dataset]) # transform to torch tensors
# time.sleep(5)
# tensor_y = torch.stack([torch.Tensor(i) for i in y_in_dataset])

print(x_in_dataset[2])
# tensor_x = torch.FloatTensor(x_in_dataset)
# tensor_y = torch.FloatTensor(y_in_dataset)
custom_dataset = utils.TensorDataset(tensor_x, tensor_y) # create your datset
time.sleep(5)
custom_dataloader = utils.DataLoader(dataset=custom_dataset,batch_size = 1,shuffle = True) # create your dataloader




#dataloader = DataLoader(dataset=a, batch_size=1, shuffle=True)

for sample in custom_dataloader:

    print(sample)
    time.sleep(2222)


class AutoEncoder(nn.Module):
    def __init__(self):
        super(AutoEncoder, self).__init__()
        self.encoder = nn.Sequential(nn.Linear(len(states[0]), 512),
                                     nn.LeakyReLU(),
                                     nn.Linear(512, 256),
                                     nn.LeakyReLU(),
                                     nn.Linear(256, 128),
                                     nn.LeakyReLU(),
                                     nn.Linear(128, 64),
                                     nn.LeakyReLU(),
                                     nn.Linear(64, 32),
                                     nn.LeakyReLU()

                                     )

        # self.encoder_linear1 = nn.Linear(len(training_dataset[0]), 512) #in features, out features
        # self.encoder_relu1 = nn.LeakyReLU()
        # self.encoder_linear2 = nn.Linear(512, 256)
        # self.encoder_relu2 = nn.LeakyReLU()
        # self.encoder_linear3 = nn.Linear(256, 128)
        # self.encoder_relu3 = nn.LeakyReLU()
        # self.encoder_linear_4 = nn.Linear(128, 64)
        # self.encoder_relu4 = nn.LeakyReLU()
        # self.encoder_linear5 = nn.Linear(64, 32)
        # self.encoder_relu5 = nn.LeakyReLU()

        #------------------------------------------Encoder ends here

        self.decoder = nn.Sequential(nn.Linear(32, 64),
                                     nn.LeakyReLU(),
                                     nn.Linear(64, 128),
                                     nn.LeakyReLU(),
                                     nn.Linear(128, 256),
                                     nn.LeakyReLU(),
                                     nn.Linear(256, 512),
                                     nn.LeakyReLU(),
                                     nn.Linear(512, len(states[0]))


        )

        # self.decoder_linear1 = nn.Linear(32, 64)
        # self.decoder_relu1 = nn.LeakyReLU()
        # self.decoder_linear2  = nn.Linear(64,128)
        # self.decoder_relu2 = nn.LeakyReLU()
        # self.decoder_linear3 = nn.Linear(128,256)
        # self.decoder_relu3 = nn.LeakyReLU()
        # self.decoder_linear4 = nn.Linear(256, 512)
        # self.decoder_relu4 = nn.LeakyReLU()
        # self.decoder_linear_op = nn.Linear(512, len(training_dataset[0]))


    def forward(self, x):

        #Encoder part

        x = self.encoder(x)
        # x = self.encoder_linear1(x)
        # x= self.encoder_relu1(x)
        # x = self.encoder_linear2(x)
        # x = self.encoder_relu2(x)
        # x = self.encoder_linear3(x)
        # x = self.encoder_relu3(x)
        # x= self.encoder_linear_4(x)
        # x = self.encoder_relu4(x)
        # x = self.encoder_linear5(x)
        # x = self.encoder_relu5(x)

#-----------------------------------------------------may be we can put tolerance stuff on latent dimensions
        #decoder part


        x = self.decoder(x)


        # x = self.decoder_linear1(x)
        # x = self.decoder_relu1(x)
        # x = self.decoder_linear2(x)
        # x = self.decoder_relu2(x)
        # x = self.decoder_linear3(x)
        # x = self.decoder_relu3(x)
        # x = self.decoder_linear4(x)
        # x = self.decoder_relu4(x)
        # x = self.decoder_linear_op(x)
        return x


model = AutoEncoder().cuda()
criterion = nn.L1Loss()#-----------------------------------------------Which loss to use, L1 or MSE, L1 loss makes more sense because we do not have outliers in our data
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate, weight_decay=1e-5)

for epoch in range(num_epochs):
    for sample in dataloader:
        print(len(sample))
        #print(sample[39])
        time.sleep(5)
        sample = Variable(sample).cuda()
        # ----------------------------------------------forward
        output = model(sample)

        # print("original image ", sample)
        # print("output image", output)

        loss = criterion(output, sample)#------------------take care of the order of the sample and the output

        # ----------------------------------------------backward
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    # ===================log========================
    print('epoch [{}/{}], loss:{:.4f}'.format(epoch + 1, num_epochs, loss.data.item()))

torch.save(model.state_dict(), './vanilla_autoencoder_for_rd.pth')