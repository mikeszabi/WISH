# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 13:58:13 2017

@author: picturio
"""
import os
from azure.storage.blob import BlockBlobService

LOCAL_DIRECT=r'C:\Users\picturio\OneDrive\WISH\PraktikerImages_FULL'

# GET IMAGES FROM AZURE BLOB
block_blob_service = BlockBlobService(account_name='imagesearchwe', account_key='IQonsNPL65GeD3sutuur8tBt/6H3l3wRV0WkPSgwC8LyPftmq2CLul7w0l8i41y8qENzyeZx1JIhjiahovLl8g==')

block_blob_service.get_blob_to_path('imagesearchprod', 'myblockblob', 'out-sunset.png')

containers = block_blob_service.list_containers()

for c in containers:
    print(c.name)
    
CONTAINER_NAME='imagesearchprod'
blobs = block_blob_service.list_blobs(CONTAINER_NAME)

for blob in blobs:
    local_file = os.path.join(LOCAL_DIRECT, blob.name.split('/')[-1])
    try:
        block_blob_service.get_blob_to_path(CONTAINER_NAME, blob.name, local_file)
    except:
        print ('something wrong happened when downloading the data'+blob.name)