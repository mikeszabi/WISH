# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 17:46:08 2017

@author: SzMike
"""
import sys
import time
import file_helper
import os
import json
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import cnn_feature_service
import object_detection
import matplotlib.gridspec as gridspec

%matplotlib qt5


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
match_cat={}
match_im={}
 
match=0
for q_im in image_list_indir:
    cont_dir=q_im.split('\\')[-2]
    query_category[q_im]=cont_dir
    query_im=Image.open(q_im)
    query_im.thumbnail((300,300))
    query_feat=np.array(cnn_f.create_feature(query_im)) 
    cf=cnn_f.compare_feature(query_feat.reshape(1,-1),cnn_f.db_features)
    print('---------------------')
    print(cf.min())    
    result_indices = np.argsort(cf)[0,0:3]
    print(cont_dir)
    m_cat=[]
    m_im=[]
    for i in range(3):
        image_file=cnn_f.db_files_list[result_indices[i]]
        print(db_categories[image_file])
        m_cat.append(db_categories[image_file])
        m_im.append(image_file)
        if query_category[q_im]==db_categories[image_file]:
            match+=1
            break
    match_cat[q_im]=m_cat
    match_im[q_im]=m_im         



for q_im in image_list_indir:
    fig = plt.figure(figsize=(4,1))
    fig.suptitle(q_im)
    query_im=Image.open(q_im)
    query_im.thumbnail((300,300))
   
    ax1=plt.subplot(1,4,1)
    ax1.imshow(query_im)
    ax1.set_title(query_category[q_im])
    ax1.axis('off')
    i=0
    for s_im in match_im[q_im]:
        i+=1
        sim_im=Image.open(s_im.replace('picturio',onedrive_use))
        sim_im.thumbnail((300,300))
        ax=plt.subplot(1,4,i+1)
        ax.imshow(sim_im)
        ax.set_title(db_categories[s_im])
        ax.axis('off')
   
    
#plt.close('all')    



