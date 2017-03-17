# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 13:12:13 2017

@author: SzMike
"""

import numpy as np
from PIL import Image
from cntk.ops.functions import load_model
import cntk as ct
import csv


from cntk.ops.functions import load_model

def createLookup(lookupfile):
    fieldnames = ['ID', 'category']
    reader =csv.DictReader(open(lookupfile, 'rt', encoding='utf8'), delimiter='\t', fieldnames=fieldnames)
    label_lookup = {}
    for row in reader:
        try:
            label_lookup[int(row['ID'])]=row['category']
        except:
            print(row)
    return label_lookup

lookupfile='d://Projects//models//PRAKTIKER//categories_map_lev2.txt'
pred = load_model('d:\Projects\models\PRAKTIKER\ResNet152_Praktiker.dnn')

label_lookup=createLookup(lookupfile)    


imgSize=224
image_mean   = 128.0
im=Image.open('d://Projects//data//PRAKTIKER//images300x300//44086_01_pozdorjacsavar-3x20mm.jpg')
im.show()
im.thumbnail([imgSize, imgSize], Image.ANTIALIAS)
image_data   = np.array(im, dtype=np.float32)
image_data  -= image_mean
image_data   = np.ascontiguousarray(np.transpose(image_data, (2, 0, 1)))
ii=np.zeros(shape=(1,3,imgSize,imgSize),dtype=np.float32)
ii[0,]=image_data

# https://github.com/Microsoft/CNTK/wiki/Evaluate-a-saved-convolutional-network

for index in range(len(pred.outputs)):
    print("Index {} for output: {}.".format(index, pred.outputs[index].name))

pred_out = ct.combine([pred.outputs[2].owner])  
predictions = np.squeeze(pred_out.eval({pred_out.arguments[0]:ii}))
top_class = np.argmax(predictions)  

top_count = 3
result_indices = (-np.array(predictions)).argsort()[:top_count]

#print("Label")
#print(label)
print("Top 3 predictions:")
for i in range(top_count):
    print("\tLabel: {:10s}, confidence: {:.2f}%".format(label_lookup[result_indices[i]], predictions[result_indices[i]] * 100))
        
    
