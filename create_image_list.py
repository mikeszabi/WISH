# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 20:12:01 2017

@author: SzMike
"""

import file_helper
import os
import json

#base_folder = r'd:\Projects\WISH'
base_folder = os.path.curdir

image_dir=r'c:\Users\picturio\OneDrive\WISH\PraktikerImages_All'
#image_dir=r'e:\WISH\data\classification'
image_list_file=os.path.join(base_folder,'input','image_list.json')


image_list_indir=file_helper.imagelist_in_depth(image_dir,level=1)

image_label={}
for image in image_list_indir:
    image_label[image]='0'
    
               
with open(image_list_file, 'w') as imagelistfile:
    json.dump(image_list_indir,imagelistfile)
    
