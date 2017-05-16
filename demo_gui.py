# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 21:31:04 2017

@author: SzMike
"""

import tkinter as tk
import numpy as np
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

#import object_detection


import cnn_feature_service
user='SzMike' # picturio


class ImageViewer(tk.Frame):
    def __init__(self, master,cnn_f):
        tk.Frame.__init__(self, master, background="green")
        
        self.top_count = 6
        self.cnn_f=cnn_f

        browse_button = tk.Button(self, text="Browse", command=self.load_file, width=10)
        browse_button.grid(row=0, column=0, sticky=tk.W)
        find_button = tk.Button(self, text="Find Similar", command=self.find_similar, width=10)
        find_button.grid(row=0, column=1, sticky=tk.W)
       
        self.query_im = None
        self.query_img = None
        self.q2_im = None
        self.q2_img = None
        self.query_panel = None
        self.q2_panel = None
#        self.query_panel = tk.Label(self, image = self.query_img)
#        self.query_panel.grid(row=1,column=0)
        
        self.sim_im=[None] * self.top_count
        self.sim_img=[None] * self.top_count
        self.sim_panel=[None] * self.top_count
#        for i in range(self.top_count):
#            self.sim_im[i] = None
#            self.sim_img[i] = None
#            self.sim_panel[i] = tk.Label(self, image = self.sim_img[i])
#            self.sim_panel[i].grid(row=1,column=i+1)
        
    def load_file(self):
        query_path = askopenfilename(filetypes=(("ALL", "*.*"),\
                                           ("JPEG", "*.jpeg"),\
                                           ("JPG", "*.jpg"),\
                                           ("PNG", "*.png"),\
                                           ("BMP", "*.bmp")))
        self.query_im=Image.open(query_path)
        self.query_im.thumbnail((200,200))
        self.query_img = ImageTk.PhotoImage(self.query_im)
        
        self.query_panel = tk.Label(self, image = self.query_img)
        self.query_panel.grid(row=1,column=0)
        
#        self.q2_im=object_detection.find_salient_objects(self.query_im)
#        self.q2_img = ImageTk.PhotoImage(self.q2_im)
#        self.q2_panel = tk.Label(self, image = self.q2_img)
#
#        self.q2_panel.grid(row=2,column=0)

#        for i in range(self.top_count):
#            self.sim_im[i] = Image.open(query_path)
#            self.sim_im[i].thumbnail((100,100))
#            self.sim_img[i] = ImageTk.PhotoImage(self.sim_im[i])
#            self.sim_panel[i] = tk.Label(self, image = self.sim_img[i])
#            self.sim_panel[i].grid(row=1+i,column=1)
        
    def find_similar(self):
      
        print('...creating cnn features for query image')
        query_feat=np.array(self.cnn_f.create_feature(self.query_im))
        cf=self.cnn_f.compare_feature(query_feat.reshape(1,-1),cnn_f.db_features)
        
        result_indices = np.argsort(cf)[0,0:self.top_count]
        
        for i in range(self.top_count):
            image_file=cnn_f.db_files_list[result_indices[i]]
            image_file=image_file.replace('picturio',user)
            self.sim_im[i] = Image.open(image_file)
            self.sim_im[i].thumbnail((200,200))
            self.sim_img[i] = ImageTk.PhotoImage(self.sim_im[i])
            self.sim_panel[i] = tk.Label(self, image = self.sim_img[i], \
                          text=str(cf[0,result_indices[i]]),\
                                  compound=tk.BOTTOM)
            self.sim_panel[i].grid(row=1+i,column=1)

if __name__ == "__main__":
    root = tk.Tk()
    
    model_type='ResNet_152'
    db_feature_file=r'd:\Projects\WISH\output\db_features_Resnet152_1000_praktiker_full.json'
    
    cnn_f=cnn_feature_service.cnn_db_features(model_type=model_type,db_feature_file=db_feature_file)
    
    im_w=ImageViewer(root,cnn_f)
    im_w.pack(fill="both", expand=True)
    root.mainloop()