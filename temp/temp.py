# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import skimage.io as io
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import selectivesearch
from skimage import segmentation

from skimage import img_as_ubyte, img_as_float
from skimage.transform import rescale
from cntk_helpers import *

#  %matplotlib qt5

image_file=r'd:\DATA\Temp\win_20160803_11_28_42_pro.jpg'

imgOrig=io.imread(image_file)

roi_maxImgDim = 200 
ss_scale = 100            # selective search ROIS: parameter controlling cluster size for segmentation
ss_sigma = 1.2            # selective search ROIs: width of gaussian kernal for segmentation
ss_minSize = 25   
roi_minDimRel = 0.01      # minium relative width/height of a ROI
roi_maxDimRel = 1.0       # maximum relative width/height of a ROI
roi_minNrPixelsRel = 0.02    # minium relative area covered by ROI
roi_maxNrPixelsRel = 1  # maximm relative area covered by ROI
roi_maxAspectRatio = 4.0  # maximum aspect Ratio of a ROI vertically and horizontally
roi_maxImgDim = 200       # ima
roi_minDim = roi_minDimRel * roi_maxImgDim
roi_maxDim = roi_maxDimRel * roi_maxImgDim
roi_minNrPixels = roi_minNrPixelsRel * roi_maxImgDim*roi_maxImgDim
roi_maxNrPixels = roi_maxNrPixelsRel * roi_maxImgDim*roi_maxImgDim

#scale = 1.0 * roi_maxImgDim / max(im.shape[:2])
#im_small = img_as_ubyte(rescale(im, scale, order=1))

im_small, scale = imresizeMaxDim(imgOrig, roi_maxImgDim, boUpscale=True, interpolation = cv2.INTER_AREA)

im_mask = segmentation.felzenszwalb(
        img_as_float(im_small), scale=ss_scale, sigma=ss_sigma,
        min_size=ss_minSize)
plt.imshow(segmentation.find_boundaries(im_mask))

img, ssRois = selectivesearch.selective_search(im_small, scale=ss_scale, sigma=ss_sigma, min_size=ss_minSize)
rects = []
for ssRoi in ssRois:
    x, y, w, h = ssRoi['rect']
    rects.append([x,y,x+w,y+h])
imgWidth, imgHeight = imArrayWidthHeight(img)

plt.imshow(segmentation.find_boundaries(img[:,:,3]))

rois = filterRois(rects, imgWidth, imgHeight, roi_minNrPixels, roi_maxNrPixels, roi_minDim, roi_maxDim, roi_maxAspectRatio)


fig=plt.figure('a image')
axs=fig.add_subplot(111)
axs.imshow(im_small)  
for roi in rois:
    axs.add_patch(patches.Rectangle(
        (roi[0], roi[1]),   # (x,y)
        roi[2]-roi[0],          # width
        roi[3]-roi[1],          # height
        fill=False
    ))
       