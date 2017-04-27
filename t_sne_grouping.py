# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 15:46:39 2017

@author: SzMike
"""

import sys
import time
import file_helper
import os
import json
import numpy as np
from matplotlib import pyplot as plt
import cnn_feature_service
import matplotlib.gridspec as gridspec
from matplotlib.ticker import NullFormatter

from sklearn import manifold

%matplotlib qt5


onedrive_use='SzMike'

#base_folder = r'd:\Projects\WISH'
base_folder = os.path.curdir
feature_file=r'd:\Projects\WISH\output\features.json'

features=cnn_feature_service.load_db_features(feature_file)

feat_list=[np.asarray(feat) for feat in features.values()]

feat_array=np.asarray(feat_list)

model = manifold.TSNE(n_components=2, random_state=0)
model.fit_transform(feat_array) 

Y = model.fit_transform(feat_array)
fig=plt.figure()
plt.scatter(Y[:, 0], Y[:, 1], cmap=plt.cm.Spectral)
plt.axis('tight')

plt.show()

# create grid
# add photos to grid
# visualize