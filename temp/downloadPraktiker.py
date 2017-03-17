# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 15:20:11 2016

@author: picturio
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 09:15:10 2016

@author: SzMike
"""


import unicodecsv as csv
import os
from collections import OrderedDict
from collections import Counter
import json
from PIL import Image
import requests
import io

dataDir='d://Projects//data//PRAKTIKER//'
savePath=os.path.join(dataDir,'images64x64/')
thumbnailSize= 64, 64
jsonFile=os.path.join(dataDir,'crawl-full.json')


def url_to_image(url,fileName):
    global savePath,  thumbnailSize
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    response = requests.get(url)
    webImg=Image.open(io.StringIO(response.content))
    # get rid of alpha channel
    bg = Image.new("RGB", webImg.size, (255,255,255))
    bg.paste(webImg,webImg)
    bg.thumbnail(thumbnailSize, Image.ANTIALIAS)
    bg.save(os.path.join(savePath, fileName+'.png'))  
    #img = np.array(bg)
    #j=Image.fromarray(img)      
        
json_data=open(jsonFile,encoding='utf-8-sig').read()
data = json.loads(json_data, object_pairs_hook=OrderedDict)

# iterate over images
prods_all = {}
for i in range(len(data)):
    if len(data[i]['ImageUrls'])==1:
        fileName = data[i]['ImageUrls'][0].split('/')[-1].split('.')[0]
        if len(data[i]['Categories'])==3:
            try:
                #img=url_to_image(data[i]['ImageUrls'][0],fileName)
                prods_all[fileName] = data[i]['Categories'][1]
            except:
                print(data[i]['ImageUrls'][0])
                    

prodCount=Counter(prods_all.values())

# remove prods with less than 10 occurencies
prods = {}
for key, item in prods_all.items():
    if prodCount[item]>50:
        prods[key]=item
            
prodCount=Counter(prods.values())    

print(prodCount)    
prodCats = set(prods.values())

prodCat = {}
i=0
for cats in prodCats:
    prodCat[cats]=i
    i=i+1

#
out = open(os.path.join(dataDir,'prodCats1/imcats.csv'), 'wb')
w = csv.DictWriter(out, delimiter=';', fieldnames=['category','ID'])
w.writeheader()
for key, value in prodCat.items():
    w.writerow({'category' : key, 'ID' : value})
out.close()

out = open(os.path.join(dataDir,'prodCats1/images.csv'), 'wb')
w = csv.DictWriter(out, delimiter=';', fieldnames=['image','category'])
w.writeheader()
for key, value in prods.items():
    w.writerow({'image' : key, 'category' : prodCat[value]})
out.close()
