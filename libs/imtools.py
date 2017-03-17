# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 22:13:16 2017

@author: SzMike
"""

import warnings
from skimage.transform import rescale
from skimage import img_as_ubyte

def imRescaleMaxDim(im, maxDim, boUpscale = False, interpolation = 1):
    scale = 1.0 * maxDim / max(im.shape[:2])
    if scale < 1  or boUpscale:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            im = img_as_ubyte(rescale(im, scale, order=interpolation))
    else:
        scale = 1.0
    return im, scale