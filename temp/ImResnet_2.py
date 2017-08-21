# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 11:33:06 2017

@author: picturio
"""

import cfg
from cntk import load_model

global visited
visited=set()

def dfs_walk(node): 
    if node in visited:
        return
    visited.add(node)
    print("visiting %s"%node)
    if hasattr(node, 'root_function'):
        node = node.root_function
        for child in node.inputs:
            dfs_walk(child)
    elif hasattr(node, 'is_output') and node.is_output:
        if hasattr(node,'owner'):
            try:
                dfs_walk(node.owner)
            except:
                return

def print_all_node_names(model):
    dfs_walk(model)

base_folder = os.path.curdir       
model_type='AlexNetBS'

param=cfg.param(model_type)

image_list_file, feature_file, model_file =\
            param.getDirs(base_folder=base_folder)

cnn_model=load_model(model_file)

print_all_node_names(cnn_model)
