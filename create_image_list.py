# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 20:12:01 2017

@author: SzMike
"""

import __init__
import file_helper
import os
import csv

image_dir=r'e:\Pictures\TestSets\TestSequencies\Food'
output_dir=r'd:\Projects\WISH\output'

image_list_indir=file_helper.imagelist_in_depth(image_dir,level=1)

image_label={}
for image in image_list_indir:
    image_label[image]='0'
    
out = open(os.path.join(output_dir,'images_test.csv'), 'wt',newline='')
w = csv.DictWriter(out, delimiter='\t', fieldnames=['image','label'])
for key, value in image_label.items():
    w.writerow({'image' : key, 'label' : value})
out.close()

