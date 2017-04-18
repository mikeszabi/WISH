# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 17:46:08 2017

@author: SzMike
"""

import file_helper
import os
import json
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import cnn_feature_service
import object_detection

onedrive_use='SzMike'

#base_folder = r'd:\Projects\WISH'
base_folder = os.path.curdir

test_image_dir=r'c:\Users\SzMike\OneDrive\WISH\TestImages_praktiker'
#image_dir=r'e:\WISH\data\classification'
db_category_file=r'C:\Users\SzMike\OneDrive\WISH\ProductImages\image_category.json'

cnn_f=cnn_feature_service.cnn_db_features()

with open(db_category_file, 'r', encoding='utf-16') as fp:
    db_categories = json.load(fp)

# query images
image_list_indir=file_helper.imagelist_in_depth(test_image_dir,level=1)
query_category={}

for images in image_list_indir:
    cont_dir=images.split('\\')[-2]
    query_category['images']=cont_dir
    query_im=Image.open(images)
    query_im.thumbnail((300,300))
    query_im.show()
    q2_im=object_detection.find_salient_objects(query_im,vis_diag=False)
    
    query_feat=np.array(cnn_f.create_feature(query_im))    
    q2_feat=np.array(cnn_f.create_feature(q2_im))

    cf=cnn_f.compare_feature(query_feat.reshape(1,-1),cnn_f.db_features)
    print('---------------------')
    print(cf.min())    
    result_indices = np.argsort(cf)[0,0:3]
    print(cont_dir)
    for i in range(1):
        image_file=cnn_f.db_files_list[result_indices[i]]
        print(db_categories[image_file])
        sim_im=Image.open(image_file.replace('picturio',onedrive_use))
        sim_im.show()
        image_file=image_file.replace('picturio',onedrive_use)

    print('---------------------')
    
    cf2=cnn_f.compare_feature(q2_feat.reshape(1,-1),cnn_f.db_features)
    print(cf2.min())  
       
    result_indices = np.argsort(cf2)[0,0:3]
    print(cont_dir)
    for i in range(1):
        image_file=cnn_f.db_files_list[result_indices[i]]
        print(db_categories[image_file])
        sim_im=Image.open(image_file.replace('picturio',onedrive_use))
        sim_im.show()
        image_file=image_file.replace('picturio',onedrive_use)

    
