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
from cntk.device import set_default_device, cpu
from cntk import load_model
from cntk.ops import combine
from PIL import Image

from sklearn.metrics import pairwise

import numpy as np

import cfg

def load_db_features(db_feature_file):
    with open(db_feature_file, 'r') as fp:
        db_features = json.load(fp)
    return db_features

class cnn_db_features:
    def __init__(self,model_type='ResNet_152'):
        set_default_device(cpu())

        base_folder = os.path.abspath(os.path.curdir)        
        # input, output, model directory
        
        self.param=cfg.param(model_type)
        
        self.image_list_file, feature_file, model_file = self.param.getDirs(base_folder=base_folder)
        
        self.cnf=cnn_features(self.param,model_file)
        
        self.db_feature_file=str.replace(feature_file,'features','db_features')
        
        self.db_features_dict=load_db_features(self.db_feature_file)
        self.db_files_list=list(self.db_features_dict.keys())
        self.db_features=np.array([v for k,v in self.db_features_dict.items()])
        
        
    def create_feature(self, img):
        feat=self.cnf.create_cnn_feature(img)
        return feat
    
    def compare_feature(self,feat,db_features):
        dist=pairwise.euclidean_distances(feat,db_features)
        return dist

class cnn_features:
    def __init__(self,param,model_file):
        #set_default_device(cpu())
        self.param=param
                        
        # LOAD model -only once!
        print('...loading model')
    
        self.cnn_model=load_model(model_file) 
        
        print('...cnn model is loaded')
        
        node_in_graph = self.cnn_model.find_by_name(self.param.node_name)
        self.feat_out  = combine([node_in_graph.owner])

        if self.param.softmaxed:
            self.feat_out = softmax(self.feat_out)
        
        
    def create_cnn_feature(self,img):
      
        #get rid of alpha channel
        if img.format=='PNG':
            bg = img.convert('RGB')
        else:
            bg=img
        bg=bg.resize([self.param.imgSize, self.param.imgSize], Image.ANTIALIAS)
        image_data   = np.array(bg, dtype=np.float32)
        image_data  -= self.param.image_mean
        bgr_image = image_data[..., [2, 1, 0]]
        pic = np.ascontiguousarray(np.rollaxis(bgr_image, 2))
        ii=np.zeros(shape=(1,3,self.param.imgSize,self.param.imgSize),dtype=np.float32)
        ii[0,]=pic
          
        cnn_feature=(np.squeeze(self.feat_out.eval({self.cnn_model.arguments[0]:ii}))).tolist()
        
        return cnn_feature

    def create_cnn_features(self,image_list):
                      
        # Creating features
        cnn_feat={}
        for image_file in image_list:
                     
            img=Image.open(image_file)
            print(image_file)
            cnn_feat[image_file]=self.create_cnn_feature(img)
        
        return cnn_feat
    
if __name__=='__main__':
# Initialize argument parse object
    parser = argparse.ArgumentParser()

    # This would be an argument you could pass in from command line
    parser.add_argument('-b', action='store', dest='b', type=str, required=False,
                    default=os.path.curdir)
    parser.add_argument('-m', action='store', dest='m', type=str, required=False,
                    default='ResNet_152')
   
# Parse the arguments
    inargs = parser.parse_args()

    base_folder = os.path.abspath(inargs.b)        
    # input, output, model directory
    
    model_type='AlexNetBS_2nd'

    param=cfg.param(model_type)
    
    image_list_file, feature_file, model_file =\
            param.getDirs(base_folder=base_folder)
   
    cnf=cnn_features(param,model_file)
    
    if os.path.isfile(image_list_file):
   
        while True:
        
            if os.path.isfile(image_list_file):
                print('...processing new image list')
                try:
                    with open(image_list_file, 'r') as fp:
                        image_list = json.load(fp)
                    cnn_feat=cnf.create_cnn_features(image_list)
                    with open(feature_file, 'w') as fp:
                        json.dump(cnn_feat,fp)
                    print('...features are created')    
                    os.remove(image_list_file)
                    break
                except:
                    break
    else:
        print('No images to process')                    
    
    sys.exit(1)
            

