# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 15:35:08 2017

@author: SzMike
"""

import BMS
import numpy as np
from skimage import morphology
from PIL import Image


def find_salient_objects(im,vis_diag=False):
    img=np.array(im)

    sm=BMS.compute_saliency(img)
    mask=sm>32

    mask_dil=morphology.binary_dilation(mask,morphology.disk(11))
    mask_dil = mask_dil[:,:,np.newaxis]
    mask_dil = np.broadcast_arrays(img, mask_dil)[1]

    img_mask=img.copy()
    img_mask[mask_dil==0]=255

    im = Image.fromarray(np.uint8(img_mask))
    
    if vis_diag:
        im.show()
        
    return im
               
