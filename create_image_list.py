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

onedrive_user='picturio' # picturio

image_dir=os.path.join(r'c:\Users',onedrive_user,'OneDrive\WISH\ProductImages')
#image_dir=os.path.join(r'c:\Users',onedrive_user,'OneDrive\WISH\TestImages_Praktiker')

#image_dir=r'd:\DATA\Alinari'

image_list_file=os.path.join(base_folder,'input','image_list.json')

image_list_indir=file_helper.imagelist_in_depth(image_dir,level=1)

image_label={}
for image in image_list_indir:
    image_label[image]='0'
    
               
with open(image_list_file, 'w') as imagelistfile:
    json.dump(image_list_indir,imagelistfile)
    
