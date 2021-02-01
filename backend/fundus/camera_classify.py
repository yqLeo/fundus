"""
A prgram to detect fundus image's edge to classfy image by different camera. 
if the program fail to predict, it prints "cannot determine"
if there is no dege, it prints "no edge detected"
Otherwise, it prints the edge shape and corresponding camera

How to use: input the target image path in argument e.g. python camera_classify.py sample.jpeg
Also: input txt file path containing path of images. The program will output result to
result.csv. e.g. python camera_classify.py path.txt
"""
import sys
import cv2
import numpy as np
from matplotlib.patches import Circle
import os
import random
import paddle
import paddle.fluid as fluid
import numpy as np
from paddle.fluid.dygraph.nn import Conv2D, Pool2D, Linear
import pandas as pd


#Define the LeNet netork
class LeNet(fluid.dygraph.Layer):
    """
    initialize the network
    param:model,class number
    return:no return value
    """
    def __init__(self, num_classes=1):
        super(LeNet, self).__init__()

        # Sigmoid - 2x2 pooling
        self.conv1 = Conv2D(num_channels=3, num_filters=6, filter_size=5, act='sigmoid')
        self.pool1 = Pool2D(pool_size=2, pool_stride=2, pool_type='max')
        self.conv2 = Conv2D(num_channels=6, num_filters=16, filter_size=5, act='sigmoid')
        self.pool2 = Pool2D(pool_size=2, pool_stride=2, pool_type='max')
        # 3rd conv
        self.conv3 = Conv2D(num_channels=16, num_filters=120, filter_size=4, act='sigmoid')
        # fully connected layer 64 -num_classes
        self.fc1 = Linear(input_dim=300000, output_dim=64, act='sigmoid')
        self.fc2 = Linear(input_dim=64, output_dim=num_classes)

    def forward(self, x):
        """
        forward calculation
        param:model,input
        return:output
        """
        x = self.conv1(x)
        x = self.pool1(x)
        x = self.conv2(x)
        x = self.pool2(x)
        x = self.conv3(x)
        x = fluid.layers.reshape(x, [x.shape[0], -1])
        x = self.fc1(x)
        x = self.fc2(x)
        return x
    

#load the pretrained model
with fluid.dygraph.guard():
    model = LeNet(num_classes=4)
    model_state_dict, _ = fluid.load_dygraph("new")
    model.load_dict(model_state_dict)


def shape(img):
    """
    Crop the edge of the image
    param:image
    return: the edge of image
    """
    width = int(img.shape[1] * 0.3)
    height = int(img.shape[0] * 0.3)
    img = cv2.resize(img, (width, height))
    ret, cimg=cv2.threshold(img, 15, 255, cv2.THRESH_BINARY)   
    circles = maxcircle(cimg)
    cv2.circle(cimg, (int(circles[0]), int(circles[1])), int(circles[2]+3), (0, 0, 0),
               thickness=-1, lineType=8, shift=0)
    contours, _ = cv2.findContours(cimg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    # Find object with the biggest bounding box
    mx = (0, 0, 0, 0)      # biggest bounding box so far
    mx_area = 0
    for cont in contours:
        x, y, w, h = cv2.boundingRect(cont)
        area = w * h
        if area > mx_area:
            mx = x, y, w, h
            mx_area = area
    x, y, w, h = mx

    # Output to files
    roi=cimg[y: y + h, x: x + w]
    if(roi.size != 0):
        roi = cv2.cvtColor(roi, cv2.COLOR_GRAY2BGR)
    return roi

def maxcircle(cimg):
    """
    Findout the max radius of circle (This part is most time-consuming)
    param:image
    return:max radius and coordinate of center
    """
    widthCounts = np.bincount(np.nonzero(cimg)[0])
    heightCounts = np.bincount(np.nonzero(cimg)[1])
    maxWCount = np.argmax(widthCounts)
    maxHCount = np.argmax(heightCounts)
    maxWidth = 0
    maxHeight = 0
    xCoor = 0
    yCoor = 0
    for i in range(cimg.shape[1]):
        if(cimg[maxWCount][i] != 0):
            maxWidth += 1
            xCoor = i - maxWidth / 2
    for j in range(cimg.shape[0]):
        if(cimg[j][maxHCount] != 0):
            maxHeight += 1
            yCoor = j - maxHeight / 2
    if(maxHeight > maxWidth):
        return [xCoor, yCoor, maxHeight / 2]
    else:
        return [xCoor, yCoor, maxWidth / 2]

def transform_img(img):
    """
    resize the image to match the model
    param:image
    return: resized image
    """
    # 224x224
    img = cv2.resize(img, (224, 224))
    # [H, W, C]
    # [C, H, W]
    img = np.transpose(img, (2, 0, 1))
    img = img.astype('float32')
    # [-1.0, 1.0]
    img = img / 255.
    img = img * 2.0 - 1.0
    return img

def area(img):
    """
    area of filled part in image in percentage
    param: image
    return: area
    """
    return (img == 255).sum() / (img.size + 1)


def readImg(path):
    """
    read the image and decide
    param:path
    output:result
    """
    img = cv2.imread(path, 0)
    result = shape(img)
    a = area(result)
    if(result.size < 500):
        return "no edge detected"
    elif(result.size > 10000):
        return "cannot determine"
    elif(a < 0.2):
        return "cannot determine"
    else:
        with fluid.dygraph.guard():
            img = transform_img(result)
            img_a=[]
            img_a.append(img)
            img_a.append(img)
            imgs_array = np.array(img_a).astype('float32')
            imgs = fluid.dygraph.to_variable(imgs_array)
            logits = model(imgs)
            pred = fluid.layers.softmax(logits)
            if(np.argmax(pred) == 0):
                return "Rectangle edge detected, possibly topcon"
            elif(np.argmax(pred) == 1):
                return "Triangle edge detected, possibly syseye or drs"
            elif(np.argmax(pred) == 2):
                return "circle edge detected, possibly canon"
            elif(np.argmax(pred) == 3):
                return "bottom circle edge detected, possibly optovue"

#main program
if __name__ == '__main__':
    path = sys.argv[1]
    if(path.endswith(".txt")):
        print("printing the output to result.csv...")
        file1 = open(path, 'r') 
        Lines = file1.readlines()
        paths = []
        results = []
        for line in Lines: 
            line = line.strip()
            paths.append(line)
            print(line)
            results.append(readImg(line))
        df = pd.DataFrame({'path': paths, 'result': results})
        df.to_csv("result.csv", index=False, sep=',')
        print("done!")
    else:
        print(readImg(path))
