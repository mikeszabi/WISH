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

model_type='AlexNetBS_2nd'

onedrive_user='SzMike'

#base_folder = r'd:\Projects\WISH'
base_folder = os.path.curdir

test_image_dir=r'c:\Users\\'+onedrive_user+'\OneDrive\WISH\TestImages_Praktiker'
#image_dir=r'e:\WISH\data\classification'
db_category_file=r'c:\Users\\'+onedrive_user+'\OneDrive\WISH\ProductImages\image_category.json'

cnn_f=cnn_feature_service.cnn_db_features(model_type=model_type,db_feature_file=r'd:\Projects\WISH\output\db_features_AlexNetBS_2nd_4096_praktiker.json')

with open(db_category_file, 'r', encoding='utf-16') as fp:
    temp_categories = json.load(fp)

db_categories={}
for items in temp_categories.keys():
    db_categories[os.path.basename(items)]=temp_categories[items]

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
        try:
            cat=db_categories[os.path.basename(image_file)]
            print(cat)
        except:
            cat='None'
            print('No category is assigned') 
            
        m_cat.append(cat)
        m_im.append(image_file)
        if query_category[q_im]==cat:
            match+=1
            break
    match_cat[q_im]=m_cat
    match_im[q_im]=m_im         

import unicodecsv as csv

out = open('eggs.csv', 'wb')
w = csv.DictWriter(out, delimiter=',', fieldnames=['imID','m_catID','a_catID_1','a_catID_2','a_catID_3'])
w.writeheader()
for key in match_cat.keys():
    val=match_cat[key]
    while len(val)<3:
        val.append('OK')
    w.writerow({'imID' : os.path.basename(key), 'm_catID' : query_category[key], \
                'a_catID_1' : val[0], 'a_catID_2' : val[1], 'a_catID_3' : val[2]})
out.close()

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
        sim_im=Image.open(s_im.replace('picturio',onedrive_user))
        sim_im.thumbnail((300,300))
        ax=plt.subplot(1,4,i+1)
        ax.imshow(sim_im)
        ax.set_title(db_categories[os.path.basename(s_im)])
        ax.axis('off')
   
    
#plt.close('all')    



