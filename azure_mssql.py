# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 08:58:30 2017

@author: picturio
"""
import os
import pandas as pd
import pymssql
import json
import codecs


base_folder = os.path.curdir

image_dir=r'C:\Users\picturio\OneDrive\WISH'
#image_dir=r'e:\WISH\data\classification'
image_list_file=os.path.join(base_folder,'input','image_list.json')
image_category_file=os.path.join(base_folder,'input','image_category.json')



server = "bzte7q7g05.database.windows.net"
user = "ImageSearchUser@bzte7q7g05"
pswd = "IS_D152AE3C-EF13-466F-8D1D-5C612645C3F5"
db_name = "ImageSearchProd"

conn = pymssql.connect(server, user, pswd, db_name)

query='SELECT category, blobUrl from dbo.Products'

prod_db = pd.read_sql(query, con=conn)

image_label={}
image_list_indir=[]
for row in prod_db.iterrows():
    image_file=image_dir+row[1]['blobUrl']
    if os.path.isfile(image_file):
        image_list_indir.append(image_file)
        image_label[image_file]=row[1]['category']
        
with open(image_list_file, 'w') as imagelistfile:
    json.dump(image_list_indir,imagelistfile)
    
with open(image_category_file, 'w', encoding='utf-16') as imagecatfile:
    json.dump(image_label,imagecatfile, ensure_ascii=False)
    

test_image_dir=r'C:\Users\picturio\OneDrive\WISH\TestImages_praktiker'
categories=prod_db['category'].unique()
for c in categories:
    newpath=os.path.join(test_image_dir,c)
    if not os.path.exists(newpath):
        os.makedirs(newpath)