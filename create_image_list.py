# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 20:12:01 2017

@author: SzMike
"""

import __init__
import file_helper
import os
import csv
from cntk.ops import softmax
import skimage.io as io
from matplotlib import pyplot as plt


image_dir=r'd:\DATA\PRAKTIKER\TestImages'
output_dir=r'd:\Projects\WISH\output'
base_folder = r'd:\Projects\WISH'
labels_file = os.path.join(base_folder,'models','IMAGENET','synset_words.txt')

labels = np.loadtxt(labels_file, str, delimiter='\t')


image_list_indir=file_helper.imagelist_in_depth(image_dir,level=1)

image_label={}
for image in image_list_indir:
    image_label[image]='0'
    
out = open(os.path.join(output_dir,'images_test.csv'), 'wt',newline='')
w = csv.DictWriter(out, delimiter='\t', fieldnames=['image','label'])
for key, value in image_label.items():
    w.writerow({'image' : key, 'label' : value})
out.close()

"""
"""
# CALL createFeature

output_file = os.path.join(base_folder, 'output', 'fcOutput.txt')
features=np.loadtxt(output_file)

for i,feat in enumerate(features):
    feat=features[i]
    im=io.imread(image_list_indir[i])
    io.imshow(im)
    pred=feat-feat.min()
    pred=pred/pred.sum()
    top_class = np.argmax(pred)  

    top_count = 3
    result_indices = (-np.array(pred)).argsort()[:top_count]

    #print("Label")
    #print(label)
    print("Top 3 predictions:")
    for j in range(top_count):
        print("\tLabel: {:10s}, confidence: {:.2f}%".format(labels[result_indices[j]], pred[result_indices[j]] * 100))
        