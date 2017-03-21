# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 10:32:07 2017

@author: SzMike
"""

import __init__
import os
import codecs, json
from cntk.ops import softmax
from cntk import load_model
from cntk.ops import combine
import skimage.io as io
from skimage import io
from skimage.transform import resize
from skimage import img_as_ubyte
import numpy as np

import file_helper

def create_cnn_features(image_list_file,output_dir,model_type):
    
    base_folder = r'd:\Projects\WISH'
    image_list_file=os.path.join(base_folder,'output','image_list.json')
    feature_file=os.path.join(base_folder,'output','features.json')
    model_type='ResNet_152'
    softmaxed=True
    
    # PARAMETERS
    base_folder = r'd:\Projects\WISH'
  
    if model_type=='ResNet_18':
        imgSize=224
        image_mean   = 128.0
        model_file  = os.path.join(base_folder,'models','IMAGENET','ResNet_18.model')
        node_name = "OutputNodes.z"
    elif model_type=='ResNet_152':
        imgSize=224
        image_mean   = 128.0
        model_file  = os.path.join(base_folder,'models','IMAGENET','ResNet_152.model')
        node_name = "OutputNodes.z"
    elif model_type=='AlexNetBS':
        imgSize=224
        image_mean   = 128.0
        model_file  = os.path.join(base_folder,'models','IMAGENET','AlexNetBS.model')
        node_name = "z"
        #node_name = "z.x._._"
    else:
        print('Unknown model')
        #return []
    
    # LOAD model -only once!
    cnn_model=load_model(model_file) 

    node_in_graph = cnn_model.find_by_name(node_name)
    feat_out  = combine([node_in_graph.owner])

    if softmaxed:
        feat_out = softmax(feat_out)
    
    
    # Image list must have two columns
    # ToDo: Check is file exsist
    with open(image_list_file, 'r') as fp:
        image_list = json.load(fp)
    # TODO: check if list
        
    # Creating features
    cnn_features={}
    for image_file in image_list:
              
        im=io.imread(image_file)
        # ToDo: check if valid image
        
        rgb_image=img_as_ubyte(resize(im,(imgSize,imgSize))).astype('float32')
        rgb_image  -= image_mean
        bgr_image = rgb_image[..., [2, 1, 0]]
        pic = np.ascontiguousarray(np.rollaxis(bgr_image, 2))
        ii=np.zeros(shape=(1,3,imgSize,imgSize),dtype=np.float32)
        ii[0,]=pic
          
        cnn_features[image_file]=(np.squeeze(feat_out.eval({cnn_model.arguments[0]:ii}))).tolist()
    
    # Write output
    with open(feature_file, 'w') as fp:
        json.dump(cnn_features,fp)

    

            

