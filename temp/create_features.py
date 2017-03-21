# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 19:39:49 2017

@author: SzMike
"""

# Copyright (c) Microsoft. All rights reserved.

# Licensed under the MIT license. See LICENSE.md file in the project root
# for full license information.
# ==============================================================================

from __future__ import print_function
import os
import csv
import numpy as np
from cntk import load_model
from cntk.ops import combine
from cntk.io import MinibatchSource, ImageDeserializer, StreamDef, StreamDefs

#####################################################
#####################################################
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
#####################################################
#####################################################


def create_mb_source(image_height, image_width, num_channels, map_file):
    transforms = [ImageDeserializer.scale(width=image_width, height=image_height, channels=num_channels, interpolations='linear')]
    return MinibatchSource(ImageDeserializer(map_file, StreamDefs(
        features=StreamDef(field='image', transforms=transforms),  # first column in map file is referred to as 'image'
        labels=StreamDef(field='label', shape=1000))))             # and second as 'label'. TODO: add option to ignore labels


def eval_and_write(model_file, node_name, output_file, minibatch_source, num_objects):
    # load model and pick desired node as output
    loaded_model  = load_model(model_file)
    node_in_graph = loaded_model.find_by_name(node_name)
    output_nodes  = combine([node_in_graph.owner])

    # evaluate model and get desired node output
    features_si = minibatch_source['features']
    with open(output_file, 'wb') as results_file:
        for i in range(0, num_objects):
            mb = minibatch_source.next_minibatch(1)
            output = output_nodes.eval(mb[features_si])

            # write results to file
            out_values = output[0,0].flatten()
            np.savetxt(results_file, out_values[np.newaxis], fmt="%.6f")
    return

if __name__ == '__main__':
    # define location of model and data and check existence
    base_folder = r'd:\Projects\WISH'
    #model_file  = os.path.join(base_folder,'models','IMAGENET','AlexNetBS.model')
    model_file  = os.path.join(base_folder,'models','IMAGENET','ResNet_18.model')
    map_file    = os.path.join(base_folder, 'output', 'images_test.csv')

    loaded_model  = load_model(model_file)

    imlist=[]
    with open(map_file) as f:
        reader=csv.DictReader(f,delimiter='\t', fieldnames=['image','label'])
        for rows in reader:
            imlist.append(rows['image'])
            
    n_images=len(imlist)

    # create minibatch source
    # ALEXNET
#    image_height = 227
#    image_width  = 227
    # RESNET
    image_height = 224
    image_width  = 224
    num_channels = 3
    minibatch_source = create_mb_source(image_height, image_width, num_channels, map_file)

    # use this to print all node names of the model (and knowledge of the model to pick the correct one)
    #print_all_node_names(loaded_model)

    # use this to get 1000 class predictions (not yet softmaxed!)
    node_name = "OutputNodes.z"
    # output_file = os.path.join(base_folder, "predOutput.txt")

    # use this to get 4096 features from the last fc layer
    #node_name = "z.x._._"
    output_file = os.path.join(base_folder, 'output', 'fcOutput.txt')

    # evaluate model and write out the desired layer output
    # TODO - len map file
    #eval_and_write(model_file, node_name, output_file, minibatch_source, num_objects=n_images)
    node_in_graph = loaded_model.find_by_name(node_name)
    
    output_nodes  = combine([node_in_graph.owner])
    features_si = minibatch_source['features']
    mb = minibatch_source.next_minibatch(1)
    output = output_nodes.eval(mb[features_si])

# write results to file
    predictions = output[0,0].flatten()
    
    
# 
    top_class = np.argmax(predictions)  

    top_count = 3
    result_indices = (-np.array(predictions)).argsort()[:top_count]

    #print("Label")
    #print(label)
    print("Top 3 predictions:")
    for j in range(top_count):
        print("\tLabel: {:10s}, confidence: {:.2f}%".format(labels[result_indices[j]], predictions[result_indices[j]]))
        
        
    # Minibatch current position
https://www.cntk.ai/pythondocs/cntk.io.html    
    transforms = [ImageDeserializer.scale(width=image_width, height=image_height, channels=num_channels, interpolations='linear')]
        
    q=ImageDeserializer(map_file, StreamDefs(
        features=StreamDef(field='image', transforms=transforms),  # first column in map file is referred to as 'image'
        labels=StreamDef(field='label', shape=1000)))