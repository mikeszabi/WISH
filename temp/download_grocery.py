# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 13:47:21 2017

@author: SzMike
"""


# Licensed under the MIT license. See LICENSE.md file in the project root
# for full license information.
# ==============================================================================

from __future__ import print_function
import zipfile
import os
import os.path
try: 
    from urllib.request import urlretrieve 
except ImportError: 
    from urllib import urlretrieve
    
def download_grocery_data():
    dataset_folder=r"d:\Projects\data"
    if not os.path.exists(os.path.join(dataset_folder, "grocery", "testImages")):
        filename = os.path.join(dataset_folder, "Grocery.zip")
        if not os.path.exists(filename):
            url = "https://www.cntk.ai/DataSets/Grocery/Grocery.zip"
            print('Downloading data from ' + url + '...')
            urlretrieve(url, filename)
            
        try:
            print('Extracting ' + filename + '...')
            with zipfile.ZipFile(filename) as myzip:
                myzip.extractall(dataset_folder)
        finally:
            os.remove(filename)
        print('Done.')
    else:
        print('Data already available at ' + dataset_folder + '/grocery')
    
if __name__ == "__main__":
    download_grocery_data()