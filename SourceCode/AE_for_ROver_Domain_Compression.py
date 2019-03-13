import os

import torch
import torchvision
from torch import nn
from torch.autograd import Variable
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.datasets import MNIST
from torchvision.utils import save_image

if not os.path.exists('./autoencoder_img'):
    os.mkdir('./autoencoder_img')


def to_img(x):
    x = 0.5 * (x + 1)
    x = x.clamp(0, 1)
    x = x.view(x.size(0), 1, 28, 28)
    return x


num_epochs = 100
batch_size = 64
learning_rate = 1e-3
img_transform = transforms.Compose([
    transforms.ToTensor()
    #,    transforms.Normalize((0.5,), (0.5,))#-----------dont forget the commas, dont use normalization
])
dataset = MNIST('../data', transform=img_transform, download=True)
#print("dataset shape ",len(dataset))
import time
#time.sleep(111)
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)




class autoencoder_custom(nn.Module):
    def __init__(self):
        super(autoencoder_custom, self).__init__()
        self.encoder_linear1 = nn.Linear( 28 * 28, 512) #in features, out features
        self.encoder_relu1 = nn.LeakyReLU()
        self.encoder_linear2 = nn.Linear(512, 256)
        self.encoder_relu2 = nn.LeakyReLU()
        self.encoder_linear3 = nn.Linear(256, 128)
        self.encoder_relu3 = nn.LeakyReLU()
        self.encoder_linear_4 = nn.Linear(128, 64)
        self.encoder_relu4 = nn.LeakyReLU()


        self.encoder_linear5 = nn.Linear(64, 32)  # in features, out features
        self.encoder_relu5 = nn.LeakyReLU()



        self.decoder_linear1 = nn.Linear(32, 64)
        self.decoder_relu1 = nn.LeakyReLU()
        self.decoder_linear2  = nn.Linear(64,128)
        self.decoder_relu2 = nn.LeakyReLU()
        self.decoder_linear3 = nn.Linear(128,256)
        self.decoder_relu3 = nn.LeakyReLU()
        self.decoder_linear4 = nn.Linear(256, 512)
        self.decoder_relu4 = nn.LeakyReLU()
        self.decoder_linear_op = nn.Linear(512, 28 * 28)


    def forward(self, x):

        #Encoder part
        x = self.encoder_linear1(x)
        x= self.encoder_relu1(x)
        x = self.encoder_linear2(x)
        x = self.encoder_relu2(x)
        x = self.encoder_linear3(x)
        x = self.encoder_relu3(x)
        x= self.encoder_linear_4(x)
        x = self.encoder_relu4(x)
        x = self.encoder_linear5(x)
        x = self.encoder_relu5(x)

#-----------------------------------------------------may be we can put tolerance stuff on latent dimensions
        #decoder part
        x = self.decoder_linear1(x)
        x = self.decoder_relu1(x)
        x = self.decoder_linear2(x)
        x = self.decoder_relu2(x)
        x = self.decoder_linear3(x)
        x = self.decoder_relu3(x)
        x = self.decoder_linear4(x)
        x = self.decoder_relu4(x)
        x = self.decoder_linear_op(x)
        return x


model = autoencoder_custom().cuda()
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(
    model.parameters(), lr=learning_rate, weight_decay=1e-5)

for epoch in range(num_epochs):
    for data in dataloader:


        img, _ = data
        #
        img = img.view(img.size(0), -1)
        #print("img ",img.shape)

        img = Variable(img).cuda()
        # ===================forward=====================
        output = model(img)


        loss = criterion(output, img)
        # ===================backward====================
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    # ===================log========================
    print('epoch [{}/{}], loss:{:.4f}'
          .format(epoch + 1, num_epochs, loss.data.item()))
    # if epoch % 10 == 0:
    #     pic = to_img(output.cpu().data)
    #     save_image(pic, './mlp_img/image_{}.png'.format(epoch))

torch.save(model.state_dict(), './vanilla_autoencoder.pth')