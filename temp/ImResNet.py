# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 14:20:38 2017

@author: SzMike
"""

from __future__ import print_function
import os
import numpy as np
from cntk import load_model
from cntk.ops import combine
from cntk.io import MinibatchSource, ImageDeserializer, StreamDef, StreamDefs
import numpy as np
from PIL import Image
from cntk import load_model

image_path = r'd:\Projects\data\PRAKTIKER\images300x300'
save_path= r'd:\Projects\data\PRAKTIKER\features\ALEXNET'

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

pred = load_model('D:\Projects\models\IMAGENET\AlexNetBS.model') # ToDo: try Resnet 152
print_all_node_names(pred)
node_name = "z.x._._"
node_in_graph = pred.find_by_name(node_name)
output_nodes  = combine([node_in_graph.owner])


for index in range(len(pred.outputs)):
    print("Index {} for output: {}.".format(index, pred.outputs[index].name))


pred_out = combine([pred.outputs[3].owner])  

##

#feat={}
#included_extenstions = ['jpg', 'bmp', 'png', 'gif']
#for fn in os.listdir(image_path):
#    if (fn.endswith(ext) for ext in included_extenstions):
#        feat[fn.split('.')[0]]=10

              


## Get images and labels
labels_file = r'D:\Projects\models\IMAGENET\synset_words.txt'
labels = np.loadtxt(labels_file, str, delimiter='\t')
##
imgSize=227
image_mean   = 128.0
im=Image.open('d://Projects//data//PRAKTIKER//images300x300//283093_01_keleszto-tal-6l.jpg')
im.show()
im.thumbnail([imgSize, imgSize], Image.ANTIALIAS)
image_data   = np.array(im, dtype=np.float32)
image_data  -= image_mean
image_data   = np.ascontiguousarray(np.transpose(image_data, (2, 0, 1)))
ii=np.zeros(shape=(1,3,imgSize,imgSize),dtype=np.float32)
ii[0,]=image_data

##
featureOut = np.squeeze(output_nodes.eval({pred_out.arguments[0]:ii}))


predictions = np.squeeze(pred_out.eval({pred_out.arguments[0]:ii}))
top_class = np.argmax(predictions)  
print(labels[int(top_class)])