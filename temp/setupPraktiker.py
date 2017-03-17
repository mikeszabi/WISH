# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 15:40:14 2016

@author: picturio
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 13:18:47 2016

@author: SzMike
"""

import csv
from collections import Counter
import random
import math
import os

dataDir=r'C:\Users\SzMike\OneDrive\WBC\DATA'
imagesFile=os.path.join(dataDir,'Training','detections.csv')

trainRatio=0.7


def keysWithValue(aDict, target):
    return sorted(key for key, value in aDict.items() if target == value)

reader =csv.DictReader(open(imagesFile, 'rb'), delimiter=';')
prods = {}

for row in reader:
    prods[row['image']]=row['category']


prodCount=Counter(prods.values())

# remove prods with less than 10 occurencies
i=0
testProds = {}
trainProds = {}


for cat, count in prodCount.items():
    catProds=keysWithValue(prods,cat)
    random.shuffle(catProds)
    splitInd=int(math.ceil(trainRatio*len(catProds)))
    trainItems=catProds[:splitInd]
    testItems=catProds[splitInd:]
    for item in testItems:
        testProds[item]=cat
    for item in trainItems:
        trainProds[item]=cat

out = open(os.path.join(dataDir,'prodCats1/images_train.csv'), 'wb')
w = csv.DictWriter(out, delimiter=';', fieldnames=['image','category'])
w.writeheader()
for key, value in trainProds.items():
    w.writerow({'image' : key, 'category' : value})
out.close()

out = open(os.path.join(dataDir,'prodCats1/images_test.csv'), 'wb')
w = csv.DictWriter(out, delimiter=';', fieldnames=['image','category'])
w.writeheader()
for key, value in testProds.items():
    w.writerow({'image' : key, 'category' : value})
out.close()

