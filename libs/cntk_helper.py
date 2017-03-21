# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 11:15:31 2017

@author: SzMike
"""

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