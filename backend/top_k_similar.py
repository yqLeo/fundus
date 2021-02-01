import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
import torch
import torch.nn as nn
import random
from PIL import Image
import PIL.ImageOps    
import torchvision.transforms as transforms
import torch.nn.functional as F
import torchvision
import numpy as np
from torch.autograd import Variable
from scipy import spatial
import sys
class SiameseNetwork(nn.Module):
    def __init__(self):
        super(SiameseNetwork, self).__init__()
        self.cnn1 = nn.Sequential(
            nn.ReflectionPad2d(1),
            nn.Conv2d(1, 4, kernel_size=3),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(4),
            
            nn.ReflectionPad2d(1),
            nn.Conv2d(4, 8, kernel_size=3),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(8),


            nn.ReflectionPad2d(1),
            nn.Conv2d(8, 8, kernel_size=3),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(8),


        )

        self.fc1 = nn.Sequential(
            nn.Linear(8*256*256, 500),
            nn.ReLU(inplace=True),

            nn.Linear(500, 500),
            nn.ReLU(inplace=True),

            nn.Linear(500, 5))

    def forward_once(self, x):
        output = self.cnn1(x)
        output = output.view(output.size()[0], -1)
        output = self.fc1(output)
        return output

    def forward(self, input1, input2):
        output1 = self.forward_once(input1)
        output2 = self.forward_once(input2)
        return output1, output2

net=torch.load("shangyan_300")
def find_vector(image1):
    transform=transforms.Compose([transforms.Resize((256,256)), transforms.ToTensor()])
    image1 = image1.convert("L")
    image1 = transform(image1)
    image1.unsqueeze_(1)
    output1,output2 = net(Variable(image1).cuda(),Variable(image1).cuda())
    return (output1.cpu().detach().numpy()[0]*10).astype(int)


if __name__ == '__main__':
    path = sys.argv[1]
    k = sys.argv[2]
    try:
        image = Image.open(path)    
        vect = find_vector(image).tolist() 
        target = (np.array(vect)*100).astype(int)
    except IOError:
        vecs.append([0])
        print("image not exist")
    import pymongo
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient["mia_data"]
    mycol = mydb["new_sim_feature"]
    cursor = mycol.find(
         {},
         no_cursor_timeout=True
    )
    aa = []
    bb = []
    for x in cursor:
        if(len(x["vec"])!=128):
            continue
        aa.append(x["path"])
        bb.append(x["vec"])

    data = (np.array(bb)*100).astype(int)
    from ctypes import *
    import ctypes
    program = CDLL('./most_similar.so')
    INPUT = c_double * 20
    datas = INPUT()
    program.most_similar.restype = POINTER(c_int)
    res_int = program.most_similar(20,data.shape[0],ctypes.c_void_p(data.ctypes.data),ctypes.c_void_p(target.ctypes.data),datas)
    output = []
    for x in range(5):
        output.append(aa[res_int[x]])
    print(output)