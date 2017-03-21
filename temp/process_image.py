# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 14:20:38 2017

@author: SzMike
"""

from __future__ import print_function
import os
import csv
import numpy as np
from cntk import load_model
from cntk.ops import combine
#from cntk.io import MinibatchSource, ImageDeserializer, StreamDef, StreamDefs
from cntk.ops import softmax
import numpy as np


from skimage import io
from skimage.transform import resize
from skimage import img_as_ubyte
from matplotlib import pyplot as plt

image_dir=r'd:\DATA\PRAKTIKER\TestImages'
output_dir=r'd:\Projects\WISH\output'
base_folder = r'd:\Projects\WISH'
labels_file = os.path.join(base_folder,'models','IMAGENET','synset_words.txt')
model_file  = os.path.join(base_folder,'models','IMAGENET','AlexNetBS.model')

labels = np.loadtxt(labels_file, str, delimiter='\t')

# helpers to print all node names
def dfs_walk(node, visited):
    if node in visited:
        return
    visited.add(node)
    print("visiting %s"%node.name)
    if hasattr(node, 'root_function'):
        node = node.root_function
        for child in node.inputs:
            dfs_walk(child, visited)
    elif hasattr(node, 'is_output') and node.is_output:
        dfs_walk(node.owner, visited)

def print_all_node_names(model):
    dfs_walk(model, set())



pred = load_model(model_file) # ToDo: try Resnet 152
#print_all_node_names(pred)
node_name='z'
#node_name = "z.x._._"
node_in_graph = pred.find_by_name(node_name)
output_nodes  = combine([node_in_graph.owner])


for index in range(len(pred.outputs)):
    print("Index {} for output: {}.".format(index, pred.outputs[index].name))


pred_out = combine([pred.outputs[3].owner])  
pred_out = softmax(pred_out)

##

#feat={}
#included_extenstions = ['jpg', 'bmp', 'png', 'gif']
#for fn in os.listdir(image_path):
#    if (fn.endswith(ext) for ext in included_extenstions):
#        feat[fn.split('.')[0]]=10

imlist=[]
with open(os.path.join(output_dir,'images_test.csv')) as f:
    reader=csv.DictReader(f,delimiter='\t', fieldnames=['image','label'])
    for rows in reader:
        imlist.append(rows['image'])           

image_file=imlist[23]

## Get images and labels
##
imgSize=227
image_mean   = 128.0
#img=Image.open(image_file)
#get rid of alpha channel
#if img.format=='PNG':
#    bg = Image.new("RGB", img.size, (255,255,255))
#    bg.paste(img,img)
#else:
#    bg=img
#bg.resize((imgSize,imgSize),resample=Image.ANTIALIAS)
#bg.show()
#image_data   = np.array(bg, dtype=np.float32)
#image_data  -= image_mean
#bgr_image = image_data[..., [2, 1, 0]]
#pic = np.ascontiguousarray(np.rollaxis(bgr_image, 2))
im=io.imread(image_file)
io.imshow(im)
rgb_image=img_as_ubyte(resize(im,(imgSize,imgSize))).astype('float32')
rgb_image  -= image_mean
bgr_image = rgb_image[..., [2, 1, 0]]
pic = np.ascontiguousarray(np.rollaxis(bgr_image, 2))
ii=np.zeros(shape=(1,3,imgSize,imgSize),dtype=np.float32)
ii[0,]=pic

##
predictions = np.squeeze(output_nodes.eval({pred_out.arguments[0]:ii}))

top_class = np.argmax(predictions)  

top_count = 3
result_indices = (-np.array(predictions)).argsort()[:top_count]

#print("Label")
#print(label)
print("Top 3 predictions:")
for j in range(top_count):
    print("\tLabel: {:10s}, confidence: {:.2f}%".format(labels[result_indices[j]], predictions[result_indices[j]]))
    