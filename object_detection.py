# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 15:35:08 2017

@author: SzMike
"""

import BMS
import numpy as np
from skimage import morphology
from PIL import Image
import selectivesearch
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import selectivesearch

def find_salient_objects(im,vis_diag=False):
    img=np.array(im)

    sm=BMS.compute_saliency(img)
    mask=sm>0

    mask_dil=morphology.binary_dilation(mask,morphology.disk(1))
    mask_dil = mask_dil[:,:,np.newaxis]
    mask_dil = np.broadcast_arrays(img, mask_dil)[1]

    img_mask=img.copy()
    img_mask[mask_dil==0]=255

    im = Image.fromarray(np.uint8(img_mask))
    
    if vis_diag:
        im.show()
        
    return im
               
def find_rois(im0,vis_diag=False):
    img_lbl, regions = selectivesearch.selective_search(
        im0, scale=500, sigma=0.9, min_size=10)

    candidates = set()
    for r in regions:
        # excluding same rectangle (with different segments)
        if r['rect'] in candidates:
            continue
        # excluding regions smaller than 2000 pixels
        if r['size'] < 2000:
            continue
        # distorted rects
        x, y, w, h = r['rect']
        if w / h > 1.2 or h / w > 1.2:
            continue
        candidates.add(r['rect'])

    # draw rectangles on the original image
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6, 6))
    ax.imshow(img)
    for x, y, w, h in candidates:
        #print x, y, w, h
        rect = mpatches.Rectangle(
            (x, y), w, h, fill=False, edgecolor='red', linewidth=1)
        ax.add_patch(rect)

    plt.show()
    
    os.system('e:\\IPOL\\ace_20121029\\bin\\ace -a 8 -m interp:12 .\image.bmp .\e_image.bmp')