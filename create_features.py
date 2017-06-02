# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 16:14:39 2017

@author: SzMike
"""

import os
import cfg
import cnn_feature_service
import json


base_folder = os.path.curdir       
    # input, output, model directory
    
model_type='VGG19'

param=cfg.param(model_type)


image_list_file, feature_file, model_file =\
            param.getDirs(base_folder=base_folder)

cnn_f=cnn_feature_service.cnn_features(param,model_file=model_file)

with open(image_list_file, 'r') as fp:
    image_list = json.load(fp)
cnn_feat=cnn_f.create_cnn_features(image_list)
with open(feature_file, 'w') as fp:
    json.dump(cnn_feat,fp)    
   
   