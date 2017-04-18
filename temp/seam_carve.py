# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 13:52:06 2017

@author: SzMike
"""

from skimage import transform, util, filters, color
import numpy as np
from matplotlib import pyplot as plt
from skimage import morphology

%matplotlib qt5


from skimage import segmentation

img=np.array(query_im)
img = util.img_as_float(img)
eimg = filters.sobel(color.rgb2gray(img))


segments = felzenszwalb(img, scale=1.0, sigma=0.95, min_size=100)


out = transform.seam_carve(img, eimg, 'vertical', 132)


segments = segmentation.felzenszwalb(img, scale=5.0, sigma=5, min_size=100)

bound=segmentation.mark_boundaries(img,segments,color=(1,1,0))
plt.imshow(bound)

import BMS

sm=BMS.compute_saliency(img)

out = transform.seam_carve(img, sm, 'vertical', 132)


mask=sm>128

mask_dil=morphology.binary_dilation(mask,morphology.disk(11))
mask_dil = mask_dil[:,:,np.newaxis]
mask_dil = np.broadcast_arrays(img, mask_dil)[1]

img_mask=img.copy()
img_mask[mask_dil==0]=255

im = Image.fromarray(np.uint8(img_mask))