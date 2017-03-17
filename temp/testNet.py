# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 18:56:43 2016

@author: picturio
"""

import numpy as np
import csv
import os
from PIL import Image

dataDir='d://Projects//data//PRAKTIKER//'
lookupfile=os.path.join(dataDir,'prodCats1/imcats.csv')
imcatsfile=os.path.join(dataDir,'prodCats1/images.csv')
testImage='154249_01_halogen-reflektor-mr16-20w-gu10'
testfilename=os.path.join(dataDir,'images300x300/'+testImage+'.jpg')
imgSize=32

def keysWithValue(aDict, target):
    return sorted(key for key, value in aDict.items() if target == value)

def createLookup(lookupfile):
    reader =csv.DictReader(open(lookupfile, 'rt', encoding='utf8'), delimiter=';')
    label_lookup = {}
    for row in reader:
        label_lookup[int(row['ID'])]=row['category']
        
    return label_lookup
    
def createImCats(imcatsfile):
    
    reader =csv.DictReader(open(imcatsfile, 'rt', encoding='utf8'), delimiter=';')
    prods = {}

    for row in reader:
        prods[row['image']]=row['category']

    return prods
        
def eval(pred, label_lookup, label, testfilename):
    
    image_mean   = 128.0
    im=Image.open(testfilename)
    im.show()
    im.thumbnail([imgSize, imgSize], Image.ANTIALIAS)
    image_data   = np.array(im, dtype=np.float32)
    image_data  -= image_mean
    image_data   = np.ascontiguousarray(np.transpose(image_data, (2, 0, 1)))
    ii=np.zeros(shape=(1,3,32,32),dtype=np.float32)
    ii[0,]=image_data
    result       = np.squeeze(pred.eval({pred.arguments[0]:[ii]}))
    
    # Return top 3 results:
    top_count = 3
    result_indices = (-np.array(result)).argsort()[:top_count]

    print("Label")
    print(label)
    print("Top 3 predictions:")
    for i in range(top_count):
        print("\tLabel: {:10s}, confidence: {:.2f}%".format(label_lookup[result_indices[i]], result[result_indices[i]] * 100))
            
label_lookup=createLookup(lookupfile)    
prods=createImCats(imcatsfile)
label=label_lookup[int(prods[testImage])]
eval(pred_resnet,label_lookup,label_lookup[int(prods[testImage])],testfilename)