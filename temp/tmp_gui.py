# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 22:07:25 2017

@author: SzMike
"""

cnn_f=cnn_features()


query_im=Image.open(cnn_f.db_files_list[0])
query_im.thumbnail((300,300))

query_feat=np.array(cnn_f.create_feature(query_im))

cf=cnn_f.compare_feature(query_feat.reshape(1,-1),cnn_f.db_features)

result_indices = np.argsort(cf)[0,0:3]

