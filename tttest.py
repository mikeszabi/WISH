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
import file_helper

from PIL import Image
%matplotlib qt5

onedrive_user='SzMike'


test_image_dir=r'c:\Users\\'+onedrive_user+'\OneDrive\WISH\TestImages_Praktiker'
image_list_indir=file_helper.imagelist_in_depth(test_image_dir,level=1)
for i,q_im in enumerate(image_list_indir):
    print(str(i)+' : '+q_im)

image_file=image_list_indir[20]

query_im=Image.open(image_file)

query_im.thumbnail((300,300))
img = np.array(query_im)

sm=BMS.compute_saliency(img)


simg, bb= selectivesearch.selective_search(img, scale=200.0, sigma=1.2, min_size=100)

#ii=selectivesearch._generate_segments(img, scale=100.0, sigma=0.8, min_size=250)
f, axarr = plt.subplots(1,2)

axarr[0].imshow(simg[:,:,3])

(h,w,d)=img.shape

l_bbox=[]

axarr[1].imshow(img)

for box in bb:
    rcoords=box['rect']
    
    if rcoords[2]*rcoords[3]>50*50:
        axarr[1].add_patch(
            patches.Rectangle(
                (rcoords[0], rcoords[1]),
                rcoords[2],
                rcoords[3],
                fill=False,      # remove background
                linewidth=2,edgecolor=(np.random.rand(),np.random.rand(),np.random.rand()),facecolor='none'
            )
            )    
        l_bbox.append(box)
        


#sm=BMS.compute_saliency(img)
#mask=sm>0
#
#mask_dil=morphology.binary_dilation(mask,morphology.disk(1))
#mask_dil = mask_dil[:,:,np.newaxis]
#mask_dil = np.broadcast_arrays(img, mask_dil)[1]
#
#img_mask=img.copy()
#img_mask[mask_dil==0]=255

im = Image.fromarray(np.uint8(sm))
im.show()
        

ii=selectivesearch._generate_segments(img, scale=200.0, sigma=1.2, min_size=100)

lab_img=ii[:,:,3].copy()

for lab in np.unique(ii[:,:,3]):
    sal_lab=np.max(sm[ii[:,:,3]==lab])
    if sal_lab<64:
        print(sal_lab)
        lab_img[ii[:,:,3]==lab]=0
