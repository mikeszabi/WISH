# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 11:56:54 2017

@author: SzMike
"""

import __init__
import file_helper
import os
import csv
from cntk.ops import softmax
import skimage.io as io
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec

#from mpl_toolkits.axes_grid1 import ImageGrid

import numpy as np
%matplotlib qt5
#base_folder = r'd:\Projects\WISH'
base_folder = os.path.curdir
feature_file=os.path.join(base_folder,'output','features.json')
labels_file = os.path.join(base_folder,'models','IMAGENET','synset_words.txt')

labels = np.loadtxt(labels_file, str, delimiter='\t')

features=[]
imlist=[]
with open(feature_file, 'r') as fp:
    cnn_features = json.load(fp)


num_rows = 2
num_cols = 5

fig = plt.figure(figsize=(20,10))
gs = gridspec.GridSpec(num_rows, num_cols, wspace=0.0)

ax = [plt.subplot(gs[i]) for i in range(num_rows*num_cols)]
gs.update(hspace=0)

i=-1
for key, value in cnn_features.items():
    i+=1

    im=io.imread(key)
    ax[i].imshow(im)
    
    
    im=io.imread(key)
    pred=np.asarray(value)
    top_class = np.argmax(pred)  
    
    outstr="{:10s}, {:.2f}%".format(labels[top_class], pred[top_class]*100)

    ax[i].text(0.1,0.1,outstr,transform=ax[i].transAxes)

    top_count = 3
    result_indices = (-np.array(pred)).argsort()[:top_count]


    #print("Label")
    #print(label)
    print("Top 3 predictions:")
    for j in range(top_count):
        outstr="Label: {:10s}, confidence: {:.2f}%".format(labels[result_indices[j]], pred[result_indices[j]]*100)
        print('\t'+outstr)

    ax[i].axis('off')
        