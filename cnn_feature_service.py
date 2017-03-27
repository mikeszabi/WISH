# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 10:32:07 2017

@author: SzMike
"""

#import __init__
import os
import sys
import argparse
import json

from cntk.ops import softmax
from cntk import load_model
from cntk.ops import combine
from PIL import Image

import numpy as np

import cfg

def create_cnn_features(param,image_list,cnn_model):
      
        
    # Creating features
    cnn_features={}
    for image_file in image_list:
              
#        im=io.imread(image_file)
#        # ToDo: check if valid image
#        with warnings.catch_warnings():
#            warnings.simplefilter("ignore")
#            rgb_image=img_as_ubyte(resize(im,(param.imgSize,param.imgSize))).astype('float32')
#        rgb_image  -= param.image_mean
#        bgr_image = rgb_image[..., [2, 1, 0]]
#        pic = np.ascontiguousarray(np.rollaxis(bgr_image, 2))
        img=Image.open(image_file)
        #get rid of alpha channel
        if img.format=='PNG':
            bg = img.convert('RGB')
#            Image.new("RGBA", img.size, (255,255,255,255))
#            bg.paste(img,(0,0),img)
        else:
            bg=img
        bg=bg.resize([param.imgSize, param.imgSize], Image.ANTIALIAS)
        #bg.resize((param.imgSize,param.imgSize),resample=Image.ANTIALIAS)
        image_data   = np.array(bg, dtype=np.float32)
        image_data  -= param.image_mean
        bgr_image = image_data[..., [2, 1, 0]]
        pic = np.ascontiguousarray(np.rollaxis(bgr_image, 2))
        ii=np.zeros(shape=(1,3,param.imgSize,param.imgSize),dtype=np.float32)
        ii[0,]=pic
          
        cnn_features[image_file]=(np.squeeze(feat_out.eval({cnn_model.arguments[0]:ii}))).tolist()
    
    return cnn_features
    
if __name__=='__main__':
# Initialize argument parse object
    parser = argparse.ArgumentParser()

    # This would be an argument you could pass in from command line
    parser.add_argument('-b', action='store', dest='b', type=str, required=False,
                    default=r'e:\WISH')
    parser.add_argument('-m', action='store', dest='m', type=str, required=False,
                    default='ResNet_152')
   
# Parse the arguments
    inargs = parser.parse_args()

    base_folder = os.path.abspath(inargs.b)        
    # input, output, model directory
    
    model_type='ResNet_152'
    softmaxed=True
    
    param=cfg.param(model_type)
    
    image_list_file, feature_file, model_file = param.getDirs(base_folder=base_folder)
    
    # LOAD model -only once!
    print('...loading model')

    cnn_model=load_model(model_file) 

    node_in_graph = cnn_model.find_by_name(param.node_name)
    feat_out  = combine([node_in_graph.owner])

    if softmaxed:
        feat_out = softmax(feat_out)
   
    # DO
    # Image list must have two columns
    # ToDo: Check is file exsist
    
    with open(image_list_file, 'r') as fp:
        image_list = json.load(fp)
    # TODO: check if list    
        
    cnn_features=create_cnn_features(param,image_list,cnn_model)

     # Write output
    with open(feature_file, 'w') as fp:
        json.dump(cnn_features,fp)
    print('...features are created')    
    sys.exit(1)
            

