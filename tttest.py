# -*- coding: utf-8 -*-
"""
Created on Thu May 11 14:21:58 2017

@author: SzMike
"""

import os
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import selectivesearch
import BMS
import numpy as np
from skimage import morphology
from PIL import Image
import selectivesearch
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from PIL import Image
%matplotlib qt5

query_im=Image.open(r'c:\Users\SzMike\OneDrive\WISH\TestImages_Praktiker\Autófelszerelés, segély\20170414_103420.jpg')
query_im.thumbnail((300,300))
img = np.array(query_im)

simg, bb= selectivesearch.selective_search(img, scale=100.0, sigma=1.3, min_size=200)

ii=selectivesearch._generate_segments(img, scale=100.0, sigma=1.3, min_size=200)
plt.imshow(ii[:,:,3])

(h,w,d)=img.shape

l_bbox=[]

fig,ax2 = plt.subplots(1)
ax2.imshow(img)

for box in bb:
    rcoords=box['rect']
    
    if box['size']>100*100:
        ax2.add_patch(
            patches.Rectangle(
                (rcoords[0], rcoords[1]),
                rcoords[2]-rcoords[0],
                rcoords[3]-rcoords[1],
                fill=False,      # remove background
                linewidth=5,edgecolor=(np.random.rand(),np.random.rand(),np.random.rand()),facecolor='none'
            )
            )    
        l_bbox.append(box)
        

img=np.array(query_im)

sm=BMS.compute_saliency(img)
mask=sm>0

mask_dil=morphology.binary_dilation(mask,morphology.disk(1))
mask_dil = mask_dil[:,:,np.newaxis]
mask_dil = np.broadcast_arrays(img, mask_dil)[1]

img_mask=img.copy()
img_mask[mask_dil==0]=255

im = Image.fromarray(np.uint8(sm))
im.show()
        