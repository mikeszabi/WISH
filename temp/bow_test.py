# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 18:30:40 2017

@author: SzMike
"""
import os
import numpy as np
from PIL import Image
import cv2
import cfg
import json

base_folder = os.path.curdir     
    # input, output, model directory
    
model_type='dummy'

param=cfg.param(model_type)

image_list_file, feature_file, model_file =\
        param.getDirs(base_folder=base_folder)
with open(image_list_file, 'r') as fp:
    image_list = json.load(fp)   

dictionarySize = 5

BOW = cv2.BOWKMeansTrainer(dictionarySize)

orb = orb = cv2.ORB_create()

for image_file in image_list:                    
    img=Image.open(image_file)
    print(image_file)
    if img.format=='PNG':
        bg = img.convert('RGB')
    else:
        bg=img
    bg=bg.resize([param.imgSize, param.imgSize], Image.ANTIALIAS)    #gray = cv2.cvtColor(image, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    image_data   = np.array(bg, dtype=np.uint8)
    # find the keypoints with ORB
    kp = orb.detect(image_data,None)

    # compute the descriptors with ORB
    kp, dsc = orb.compute(image_data, kp)
    BOW.add(dsc.astype('float32'))

#dictionary created
dictionary = BOW.cluster()