import os
#---------------------------------------works good
import torch
from torch import nn
from torch.autograd import Variable
from torch.utils.data import DataLoader
from torchvision import transforms
import time
import numpy as np
import torch.utils.data as utils


num_epochs = 100
batch_size = 64
learning_rate = 1e-3
img_transform = transforms.Compose([transforms.ToTensor()])    #-------------------------------------we do not want to normalize



myfilename = "../data/Training_Data.txt"
f=open(myfilename,'r')
line = f.readline()
line_cnt = 1
states=[]
temp_line=[]
temp_line_for_1_state = []
updating_string = []
count = 0

#---------------------------for ninja technique, we need this demo string
demo_string = "a"
updating_string.append(demo_string)


while line:

    demo_string = demo_string + line
    if ("]" in line):

        demo_string = demo_string.replace("[","") #-----------
        demo_string = demo_string.replace("\n","")
        demo_string = demo_string.replace("]","")
        demo_string = demo_string.replace("a","")

        updating_string[count] = demo_string.split()

        count = count + 1
        demo_string = "a"
        updating_string.append(demo_string)

    line = f.readline()

del updating_string[-1]     #removing the "a" added at the end of the loop above
states = updating_string


for i in range(len(states)):

    if(len(states[i]) != 40):
        #print(len(states[i]))
        print("Not all joint states have the same number of elements. Position ", i," has inconsistent data.")

#convert a list of lists into a list of numpy arrays

states_list_x_of_nparrays = []
states_list_y = []
for item in range(len(states)):

    states_list_x_of_nparrays.append(np.asarray(states[item], dtype=np.float32))

for item in range(len(states)):#-------------------------------------------------works as lable, need to provide to make a data set
    states_list_y.append(np.asarray([0], dtype=np.float32))


tensor_x = torch.stack([torch.Tensor(i) for i in states_list_x_of_nparrays]) # transform to torch tensors
tensor_y = torch.stack([torch.Tensor(i) for i in states_list_y])

#tensor_x is a list of lists.
#tensor_x[0] has a length of 40

custom_dataset = utils.TensorDataset(tensor_x, tensor_y) # create your datset
custom_dataloader = utils.DataLoader(dataset=custom_dataset,batch_size = batch_size,shuffle = True) # create your dataloader


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
                                     nn.LeakyReLU(),
                                     # nn.Linear(32, 16),
                                     # nn.LeakyReLU(),
                                     # nn.Linear(16, 10),
                                     # nn.LeakyReLU()

                                     #------------------------------------------Encoder ends here

                                     )

        # self.encoder = nn.Sequential(nn.Linear(len(states[0]),50),
        #                              nn.LeakyReLU(),
        #                              nn.Linear(50, 30),
        #                              nn.LeakyReLU(),
        #                              nn.Linear(30, 20),
        #                              nn.LeakyReLU(),
        #                              nn.Linear(20, 10),
        #                              nn.LeakyReLU(),
        #                              # nn.Linear(64, 32),
        #                              # nn.LeakyReLU()  # ------------------------------------------Encoder ends here
        #
        #                              )

        self.decoder = nn.Sequential(#nn.Linear(10, 16),
                                     #nn.LeakyReLU(),
                                     #nn.Linear(16, 32),
                                     #nn.LeakyReLU(),
                                     nn.Linear(32, 64),
                                     nn.LeakyReLU(),
                                     nn.Linear(64, 128),
                                     nn.LeakyReLU(),
                                     nn.Linear(128, 256),
                                     nn.LeakyReLU(),
                                     nn.Linear(256, 512),
                                     nn.LeakyReLU(),
                                     nn.Linear(512, len(states[0]))#------------------------------------------Decoder ends here


        )
        # self.decoder = nn.Sequential(nn.Linear(10, 20),
        #                              nn.LeakyReLU(),
        #                              nn.Linear(20, 30),
        #                              nn.LeakyReLU(),
        #                              nn.Linear(30, 50),
        #                              nn.LeakyReLU(),
        #                              nn.Linear(50, len(states[0])),
        #                              nn.LeakyReLU(),
        #                              # nn.Linear(512, len(states[0]))
        #                              # # ------------------------------------------Decoder ends here
        #
        #                              )

    def forward(self, x):

        x = self.encoder(x)
                                #------------------------may be we can put tolerance stuff on latent dimensions
        x = self.decoder(x)
        return x


model = AutoEncoder().cuda()
criterion = nn.L1Loss()#--------------Which loss to use, L1 or MSE, L1 loss makes more sense because we do not have outliers in our data
optimizer = torch.optim.Adam(model.parameters(),lr=learning_rate, weight_decay=1e-5)

#print(len(custom_dataloader.dataset))#-----------------102464
for epoch in range(num_epochs):
    for index,data in enumerate(custom_dataloader):
        features_of_a_batch, labels = data
        #print(len(features)) gives 64 which is the batch size
        #print(len(features[0])) gives 40 which is the dimension of the state space
        features_of_a_batch = Variable(features_of_a_batch).cuda()
        # ----------------------------------------------forward
        output = model(features_of_a_batch)
        #check how good the model was at the end of every epoch
        if(index == len(custom_dataloader)-1):
            print("In the original data, 1st element of the last batch: ",features_of_a_batch[1])
            print("Predicted Values to compare: ",output[1])


        loss = criterion(output, features_of_a_batch)#------------------take care of the order of the output and the sample

        # ----------------------------------------------backward
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    # ===================log========================

    #-----------------------------Check how good you are doing after every epoch

    print('epoch [{}/{}], loss:{:.4f}'.format(epoch + 1, num_epochs, loss.data.item()))

torch.save(model.state_dict(), './vanilla_autoencoder_for_rd.pth')