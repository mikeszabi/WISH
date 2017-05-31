# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 20:12:01 2017

@author: SzMike
"""

import file_helper
import os
import json

#base_folder = r'd:\DATA\Alinari\'
base_folder = os.path.curdir
image_list_file=os.path.join(base_folder,'input','image_list.json')

onedrive_user='SzMike' # picturio

image_dir=os.path.join(r'c:\Users',onedrive_user,'OneDrive\\WISH\\ProductImages\\1')
db_category_file=r'c:\Users\\'+onedrive_user+'\OneDrive\WISH\ProductImages\image_category.json'

with open(db_category_file, 'r', encoding='utf-16') as fp:
    db_categories = json.load(fp)

#
image_list_indir=file_helper.imagelist_in_depth(image_dir,level=1)

image_label={}
for image in db_categories.keys():
    image_fn=os.path.basename(image)
    if os.path.exists(os.path.join(image_dir,image_fn)):
        image_label[image]='0'
    
               
with open(image_list_file, 'w') as imagelistfile:
    json.dump(image_list_indir,imagelistfile)
    
