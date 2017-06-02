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
import file_helper

from PIL import Image
%matplotlib qt5

onedrive_user='SzMike'
test_image_dir=r'c:\Users\\'+onedrive_user+'\OneDrive\WISH\TestImages_Praktiker'
image_list_indir=file_helper.imagelist_in_depth(test_image_dir,level=1)
for i,q_im in enumerate(image_list_indir):
    print(str(i)+' : '+q_im) 

dictionarySize = 20

BOW = cv2.BOWKMeansTrainer(dictionarySize)

orb = cv2.ORB_create()

for image_file in image_list_indir:                    
    img=Image.open(image_file)
    print(image_file)
    if img.format=='PNG':
        bg = img.convert('RGB')
    else:
        bg=img
    bg=bg.resize([300, 300], Image.ANTIALIAS)    #gray = cv2.cvtColor(image, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    image_data   = np.array(bg, dtype=np.uint8)
    # find the keypoints with ORB
    kp = orb.detect(image_data,None)

    # compute the descriptors with ORB
    kp, dsc = orb.compute(image_data, kp)
    BOW.add(dsc.astype('float32'))

#dictionary created
dictionary = BOW.cluster()


